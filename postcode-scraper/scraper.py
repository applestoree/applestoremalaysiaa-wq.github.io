import json
import os
import re
import time
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://postcode.my/search/"
STATE = "Johor"
START_PAGE = 2
END_PAGE = 377
MAX_RETRIES = 3
TIMEOUT = 30
DELAY_SECONDS = 1.5
BACKOFF_SECONDS = 5

ROOT = Path(__file__).resolve().parent
CACHE_DIR = ROOT / "cache"
OUTPUT_DIR = ROOT / "output"
PROGRESS_FILE = ROOT / "progress.json"
ADDRESS_FILE = OUTPUT_DIR / "address.json"
RAW_RECORDS_FILE = OUTPUT_DIR / "raw-records.json"
VALIDATION_FILE = OUTPUT_DIR / "validation-report.json"

CACHE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; JohorAddressScraper/1.0)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def page_url(page: int) -> str:
    return BASE_URL + "?" + urlencode({"keyword": "", "state": STATE, "page": page})


def load_progress():
    if PROGRESS_FILE.exists():
        try:
            return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"completedPages": [], "failedPages": []}


def save_progress(completed, failed):
    payload = {
        "completedPages": sorted(set(completed)),
        "failedPages": sorted(set(failed)),
    }
    PROGRESS_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def looks_blocked(response_text: str, status_code: int) -> bool:
    if status_code in (403, 429):
        return True
    text = response_text.lower()
    markers = [
        "captcha", "cloudflare", "access denied", "unusual traffic",
        "verify you are human", "checking your browser", "too many requests",
    ]
    return any(marker in text for marker in markers)


def extract_rows(html: str):
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table")
    target = None
    header_map = None

    for table in tables:
        rows = table.find_all("tr")
        if not rows:
            continue
        for row in rows:
            cells = [c.get_text(" ", strip=True) for c in row.find_all(["th", "td"])]
            normalized = [re.sub(r"\s+", " ", c).strip().lower() for c in cells]
            wanted = {"location", "post office", "state", "postcode"}
            if wanted.issubset(set(normalized)):
                target = table
                header_map = {value: idx for idx, value in enumerate(normalized)}
                break
        if target is not None:
            break

    if target is None or header_map is None:
        raise ValueError("Expected postcode table header was not found")

    records = []
    rows = target.find_all("tr")
    for row in rows:
        cells = [c.get_text(" ", strip=True) for c in row.find_all("td")]
        if not cells:
            continue
        try:
            location = cells[header_map["location"]].strip()
            post_office = cells[header_map["post office"]].strip()
            state = cells[header_map["state"]].strip()
            postcode = cells[header_map["postcode"]].strip()
        except (KeyError, IndexError):
            continue
        if not any((location, post_office, state, postcode)):
            continue
        records.append({
            "location": location,
            "postOffice": post_office,
            "state": state,
            "postcode": postcode,
        })
    return records


def fetch_page(page: int):
    cache_file = CACHE_DIR / f"page-{page:03d}.html"
    if cache_file.exists() and cache_file.stat().st_size > 0:
        html = cache_file.read_text(encoding="utf-8", errors="replace")
        try:
            rows = extract_rows(html)
            if rows:
                return html, rows, True
        except Exception:
            pass

    url = page_url(page)
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            if looks_blocked(response.text, response.status_code):
                raise RuntimeError(f"Blocked/CAPTCHA detected: HTTP {response.status_code}")
            response.raise_for_status()
            rows = extract_rows(response.text)
            if not rows:
                raise ValueError("Page parsed successfully but contains no data rows")
            cache_file.write_text(response.text, encoding="utf-8")
            time.sleep(DELAY_SECONDS)
            return response.text, rows, False
        except Exception as exc:
            last_error = exc
            if attempt < MAX_RETRIES:
                time.sleep(BACKOFF_SECONDS * attempt)
    raise RuntimeError(f"Page {page} failed after {MAX_RETRIES} attempts: {last_error}")


def validate_records(records):
    errors = []
    postcode_re = re.compile(r"^[0-9]{5}$")
    for idx, r in enumerate(records):
        if r["state"] != STATE:
            errors.append({"index": idx, "reason": "invalid_state", "record": r})
        if not postcode_re.fullmatch(r["postcode"]):
            errors.append({"index": idx, "reason": "invalid_postcode", "record": r})
        for field in ("location", "postOffice", "state", "postcode"):
            if not r[field]:
                errors.append({"index": idx, "reason": f"empty_{field}", "record": r})
    return errors


def build_address(records):
    root = {"country": "Malaysia", "states": {STATE: {"cities": {}}}}
    cities = root["states"][STATE]["cities"]
    for r in records:
        city = r["postOffice"]
        postcode = r["postcode"]
        location = r["location"]
        cities.setdefault(city, {"postcodes": {}})
        cities[city]["postcodes"].setdefault(postcode, [])
        if location not in cities[city]["postcodes"][postcode]:
            cities[city]["postcodes"][postcode].append(location)
    return root


def main():
    progress = load_progress()
    completed = set(progress.get("completedPages", []))
    failed = set(progress.get("failedPages", []))
    all_records = []

    # The requested range is explicitly page 2 through page 377.
    for page in range(START_PAGE, END_PAGE + 1):
        try:
            _, rows, from_cache = fetch_page(page)
            all_records.extend(rows)
            completed.add(page)
            failed.discard(page)
            save_progress(completed, failed)
            print(f"page={page} records={len(rows)} cache={from_cache}")
        except Exception as exc:
            failed.add(page)
            save_progress(completed, failed)
            print(f"FAILED page={page}: {exc}")

    expected = set(range(START_PAGE, END_PAGE + 1))
    processed = expected.intersection(completed)
    failed = expected - processed

    # Never overwrite the GitHub target unless every requested page succeeded.
    if failed:
        report = {
            "requestedPages": END_PAGE - START_PAGE + 1,
            "startPage": START_PAGE,
            "endPage": END_PAGE,
            "processedPages": len(processed),
            "failedPages": sorted(failed),
            "status": "SCRAPING INCOMPLETE",
        }
        VALIDATION_FILE.write_text(json.dumps(report, indent=2), encoding="utf-8")
        raise SystemExit(f"SCRAPING INCOMPLETE: failed pages={sorted(failed)}")

    unique = {}
    for r in all_records:
        key = (r["location"], r["postOffice"], r["state"], r["postcode"])
        unique[key] = r
    unique_records = list(unique.values())

    validation_errors = validate_records(unique_records)
    cities = {r["postOffice"] for r in unique_records}
    postcodes = {r["postcode"] for r in unique_records}
    locations = {r["location"] for r in unique_records}

    report = {
        "requestedPages": END_PAGE - START_PAGE + 1,
        "startPage": START_PAGE,
        "endPage": END_PAGE,
        "processedPages": len(processed),
        "failedPages": [],
        "rawRecords": len(all_records),
        "uniqueRecords": len(unique_records),
        "states": len({r["state"] for r in unique_records}),
        "postOffices": len(cities),
        "postcodes": len(postcodes),
        "locations": len(locations),
        "validationErrors": validation_errors,
        "status": "SUCCESS" if not validation_errors else "VALIDATION FAILED",
    }
    VALIDATION_FILE.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    if validation_errors:
        raise SystemExit(f"VALIDATION FAILED: {len(validation_errors)} errors")

    RAW_RECORDS_FILE.write_text(json.dumps(unique_records, indent=2, ensure_ascii=False), encoding="utf-8")
    address = build_address(unique_records)
    ADDRESS_FILE.write_text(json.dumps(address, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Re-parse the generated JSON and perform structural checks before allowing CI to commit it.
    parsed = json.loads(ADDRESS_FILE.read_text(encoding="utf-8"))
    assert parsed["country"] == "Malaysia"
    assert set(parsed["states"]) == {STATE}
    print("========================================")
    print("JOHOR POSTCODE SCRAPER")
    print("========================================")
    print(f"Pages requested : {END_PAGE - START_PAGE + 1}")
    print(f"Pages processed : {len(processed)}")
    print("Pages failed    : 0")
    print(f"Raw records     : {len(all_records)}")
    print(f"Unique records  : {len(unique_records)}")
    print(f"States          : {len({r['state'] for r in unique_records})}")
    print(f"Post Offices    : {len(cities)}")
    print(f"Postcodes       : {len(postcodes)}")
    print(f"Locations       : {len(locations)}")
    print("========================================")


if __name__ == "__main__":
    main()

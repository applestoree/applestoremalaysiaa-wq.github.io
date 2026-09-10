# Dokumentasi — apple-produk-kelola-produk

## 1. Identitas

**Nama Edge Function**

`apple-produk-kelola-produk`

**Supabase Project**

`Applestoremalaysia`

**Base URL**

`https://jhpbtooefyzdndstlzva.supabase.co`

**Endpoint**

`https://jhpbtooefyzdndstlzva.supabase.co/functions/v1/apple-produk-kelola-produk`

**Database Table**

`public.apple_produk`

**Status**

Active

**Version**

1

**JWT Verification**

`false`

**Runtime**

Deno Edge Function

---

# 2. Tujuan

Edge Function ini merupakan API CRUD untuk mengelola data produk Apple pada tabel:

`public.apple_produk`

Function menyediakan operasi:

* GET seluruh produk
* GET satu produk berdasarkan `item_group_id`
* POST membuat produk
* PUT memperbarui produk
* PATCH memperbarui produk
* DELETE menghapus produk

Frontend harus menggunakan Edge Function ini sebagai API utama untuk operasi CRUD produk.

Frontend tidak perlu mengakses tabel `apple_produk` secara langsung untuk operasi CRUD yang disediakan oleh function.

---

# 3. Database Source of Truth

Tabel utama:

`public.apple_produk`

Primary Key:

`item_group_id`

Jumlah field yang tersedia pada tabel saat dokumentasi dibuat:

* `item_group_id`
* `title`
* `description`
* `availability`
* `condition`
* `brand`
* `link`
* `google_product_category`
* `product_type`
* `quantity_to_sell_on_facebook`
* `custom_label_0`
* `custom_label_1`
* `custom_label_2`
* `custom_label_3`
* `custom_label_4`
* `custom_label_5`
* `variant_color`
* `variant_size`
* `created_at`
* `updated_at`
* `main_features`
* `sub_features`
* `headline`
* `band`

---

# 4. Field Database

| Field                          | Type        | Nullable | Default    | Keterangan                      |
| ------------------------------ | ----------- | -------: | ---------- | ------------------------------- |
| `item_group_id`                | text        |       No | —          | Primary key / identifier produk |
| `title`                        | text        |       No | —          | Nama produk                     |
| `description`                  | text        |      Yes | —          | Deskripsi produk                |
| `availability`                 | text        |      Yes | `in stock` | Status ketersediaan             |
| `condition`                    | text        |      Yes | `new`      | Kondisi produk                  |
| `brand`                        | text        |      Yes | `Apple`    | Brand                           |
| `link`                         | text        |      Yes | —          | URL produk                      |
| `google_product_category`      | text        |      Yes | —          | Google product category         |
| `product_type`                 | text        |      Yes | —          | Kategori produk                 |
| `quantity_to_sell_on_facebook` | integer     |      Yes | `0`        | Quantity                        |
| `custom_label_0`               | text        |      Yes | `""`       | Custom label                    |
| `custom_label_1`               | text        |      Yes | `""`       | Custom label                    |
| `custom_label_2`               | text        |      Yes | `""`       | Custom label                    |
| `custom_label_3`               | text        |      Yes | `""`       | Custom label                    |
| `custom_label_4`               | text        |      Yes | `""`       | Custom label                    |
| `custom_label_5`               | text        |      Yes | `""`       | Custom label                    |
| `variant_color`                | jsonb       |       No | `[]`       | Array/object variant warna      |
| `variant_size`                 | jsonb       |       No | `[]`       | Array/object variant ukuran     |
| `main_features`                | jsonb       |      Yes | —          | Fitur utama                     |
| `sub_features`                 | jsonb       |      Yes | —          | Sub fitur                       |
| `headline`                     | text        |      Yes | —          | Headline produk                 |
| `band`                         | text        |      Yes | —          | Informasi band                  |
| `created_at`                   | timestamptz |       No | `now()`    | Waktu dibuat                    |
| `updated_at`                   | timestamptz |       No | `now()`    | Waktu diperbarui                |

---

# 5. Allowed Fields

Edge Function hanya menerima field berikut dari request body:

```text
item_group_id
title
description
availability
condition
brand
link
google_product_category
product_type
quantity_to_sell_on_facebook
custom_label_0
custom_label_1
custom_label_2
custom_label_3
custom_label_4
custom_label_5
variant_color
variant_size
main_features
sub_features
headline
band
```

Field lain yang dikirim dari frontend akan diabaikan oleh function.

---

# 6. GET — List Products

## Endpoint

```http
GET /functions/v1/apple-produk-kelola-produk
```

Digunakan untuk mengambil daftar produk.

## Default

Jika tidak diberikan parameter:

```text
limit = 100
offset = 0
```

Data diurutkan berdasarkan:

```text
created_at DESC
```

Artinya produk terbaru muncul terlebih dahulu.

## Response

```json
{
  "success": true,
  "count": 41,
  "limit": 100,
  "offset": 0,
  "data": []
}
```

### Field response

| Field     | Type    | Keterangan                 |
| --------- | ------- | -------------------------- |
| `success` | boolean | Status request             |
| `count`   | number  | Total jumlah record        |
| `limit`   | number  | Jumlah record yang diminta |
| `offset`  | number  | Posisi awal pagination     |
| `data`    | array   | Data produk                |

---

# 7. GET — Search Products

Endpoint mendukung parameter:

```text
search
```

Search dilakukan terhadap:

```text
title
item_group_id
product_type
brand
```

Contoh:

```http
GET /functions/v1/apple-produk-kelola-produk?search=iPhone
```

Search menggunakan pencarian case-insensitive.

---

# 8. GET — Filter Product Type

Parameter:

```text
product_type
```

Contoh:

```http
GET /functions/v1/apple-produk-kelola-produk?product_type=iPhone
```

Filter menggunakan exact match terhadap:

```text
product_type
```

---

# 9. GET — Filter Availability

Parameter:

```text
availability
```

Contoh:

```http
GET /functions/v1/apple-produk-kelola-produk?availability=in%20stock
```

Filter menggunakan exact match terhadap:

```text
availability
```

---

# 10. GET — Pagination

Parameter:

```text
limit
offset
```

Contoh:

```http
GET /functions/v1/apple-produk-kelola-produk?limit=20&offset=0
```

Contoh halaman berikutnya:

```http
GET /functions/v1/apple-produk-kelola-produk?limit=20&offset=20
```

### Batas limit

Nilai `limit`:

```text
minimum = 1
maximum = 500
default = 100
```

Nilai `offset`:

```text
minimum = 0
default = 0
```

---

# 11. GET — Search + Filter + Pagination

Parameter dapat digunakan bersamaan.

Contoh:

```http
GET /functions/v1/apple-produk-kelola-produk?search=iPhone&product_type=iPhone&availability=in%20stock&limit=20&offset=0
```

Parameter:

```text
search
product_type
availability
limit
offset
```

---

# 12. GET — Single Product

Untuk mengambil satu produk berdasarkan `item_group_id`:

```http
GET /functions/v1/apple-produk-kelola-produk/{item_group_id}
```

Contoh:

```http
GET /functions/v1/apple-produk-kelola-produk/iphone-17-256gb
```

## Response berhasil

```json
{
  "success": true,
  "data": {
    "item_group_id": "iphone-17-256gb",
    "title": "iPhone 17",
    "description": "...",
    "availability": "in stock",
    "condition": "new",
    "brand": "Apple",
    "product_type": "iPhone",
    "variant_color": [],
    "variant_size": [],
    "main_features": [],
    "sub_features": [],
    "headline": null,
    "band": null
  }
}
```

## Product tidak ditemukan

HTTP:

```text
404
```

Response:

```json
{
  "success": false,
  "error": "Product not found"
}
```

---

# 13. POST — Create Product

## Endpoint

```http
POST /functions/v1/apple-produk-kelola-produk
```

## Content-Type

```http
Content-Type: application/json
```

## Required Fields

Field yang wajib:

```text
item_group_id
title
```

Jika `item_group_id` tidak dikirim:

```json
{
  "success": false,
  "error": "item_group_id is required"
}
```

HTTP:

```text
400
```

Jika `title` tidak dikirim:

```json
{
  "success": false,
  "error": "title is required"
}
```

HTTP:

```text
400
```

---

# 14. POST — Request Body

Contoh struktur:

```json
{
  "item_group_id": "iphone-17-256gb",
  "title": "iPhone 17",
  "description": "Product description",
  "availability": "in stock",
  "condition": "new",
  "brand": "Apple",
  "link": "https://example.com/product",
  "google_product_category": "Electronics",
  "product_type": "iPhone",
  "quantity_to_sell_on_facebook": 100,
  "custom_label_0": "",
  "custom_label_1": "",
  "custom_label_2": "",
  "custom_label_3": "",
  "custom_label_4": "",
  "custom_label_5": "",
  "variant_color": [],
  "variant_size": [],
  "main_features": [],
  "sub_features": [],
  "headline": "",
  "band": ""
}
```

## Response berhasil

HTTP:

```text
201
```

```json
{
  "success": true,
  "message": "Product created successfully",
  "data": {}
}
```

---

# 15. PUT — Update Product

## Endpoint

```http
PUT /functions/v1/apple-produk-kelola-produk/{item_group_id}
```

Contoh:

```http
PUT /functions/v1/apple-produk-kelola-produk/iphone-17-256gb
```

`item_group_id` berasal dari URL.

Body digunakan untuk field yang ingin diperbarui.

---

# 16. PATCH — Update Product

PATCH menggunakan endpoint yang sama:

```http
PATCH /functions/v1/apple-produk-kelola-produk/{item_group_id}
```

Contoh:

```http
PATCH /functions/v1/apple-produk-kelola-produk/iphone-17-256gb
```

PUT dan PATCH diproses dengan logic update yang sama.

---

# 17. PUT/PATCH — Important Rule

`item_group_id` tidak dapat diubah melalui body.

Function secara eksplisit menghapus:

```text
item_group_id
```

dari payload update.

Karena itu:

```json
{
  "item_group_id": "new-id",
  "title": "New Title"
}
```

tidak akan mengubah primary key.

Identifier produk harus berasal dari URL:

```text
/{item_group_id}
```

---

# 18. PUT/PATCH — updated_at

Setiap update akan otomatis mengisi:

```text
updated_at
```

dengan timestamp saat request diproses.

Frontend tidak perlu mengirim `updated_at`.

---

# 19. PUT/PATCH — Response

Berhasil:

```json
{
  "success": true,
  "message": "Product updated successfully",
  "data": {}
}
```

Jika produk tidak ditemukan:

HTTP:

```text
404
```

```json
{
  "success": false,
  "error": "Product not found"
}
```

---

# 20. DELETE — Delete Product

## Endpoint

```http
DELETE /functions/v1/apple-produk-kelola-produk/{item_group_id}
```

Contoh:

```http
DELETE /functions/v1/apple-produk-kelola-produk/iphone-17-256gb
```

Penghapusan berdasarkan:

```text
item_group_id
```

---

# 21. DELETE — Response

Berhasil:

```json
{
  "success": true,
  "message": "Product deleted successfully",
  "data": {}
}
```

Jika produk tidak ditemukan:

```json
{
  "success": false,
  "error": "Product not found"
}
```

HTTP:

```text
404
```

---

# 22. OPTIONS — CORS

Function menangani:

```http
OPTIONS
```

Response:

```text
ok
```

CORS headers yang digunakan:

```text
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers:
authorization,
x-client-info,
apikey,
content-type

Access-Control-Allow-Methods:
GET,
POST,
PUT,
PATCH,
DELETE,
OPTIONS
```

Frontend browser dapat melakukan request cross-origin ke endpoint ini.

---

# 23. HTTP Status

| Status | Kondisi                                      |
| -----: | -------------------------------------------- |
|  `200` | Request berhasil                             |
|  `201` | Product berhasil dibuat                      |
|  `400` | Request/database error atau validation error |
|  `404` | Product tidak ditemukan                      |
|  `405` | HTTP method tidak didukung                   |
|  `500` | Internal server error                        |

---

# 24. Error Format

Format error standar:

```json
{
  "success": false,
  "error": "Error message"
}
```

Frontend harus menggunakan:

```text
success
error
```

untuk menentukan status operasi.

Jangan mengasumsikan request berhasil hanya berdasarkan HTTP response.

---

# 25. Frontend API Mapping

## Product List

```text
ProductList
    ↓
GET /apple-produk-kelola-produk
```

## Search

```text
Search
    ↓
GET /apple-produk-kelola-produk?search={value}
```

## Product Type Filter

```text
ProductTypeFilter
    ↓
GET /apple-produk-kelola-produk?product_type={value}
```

## Availability Filter

```text
AvailabilityFilter
    ↓
GET /apple-produk-kelola-produk?availability={value}
```

## Product Detail

```text
ProductDetail
    ↓
GET /apple-produk-kelola-produk/{item_group_id}
```

## Create

```text
ProductCreate
    ↓
POST /apple-produk-kelola-produk
```

## Edit

```text
ProductEdit
    ↓
PUT /apple-produk-kelola-produk/{item_group_id}
```

atau:

```text
PATCH /apple-produk-kelola-produk/{item_group_id}
```

## Delete

```text
ProductDelete
    ↓
DELETE /apple-produk-kelola-produk/{item_group_id}
```

---

# 26. Recommended API Helper

Frontend dapat menggunakan satu base URL:

```text
https://jhpbtooefyzdndstlzva.supabase.co/functions/v1/apple-produk-kelola-produk
```

Kemudian seluruh operasi dibangun dari base URL tersebut.

Contoh:

```javascript
const API_URL =
  "https://jhpbtooefyzdndstlzva.supabase.co/functions/v1/apple-produk-kelola-produk";
```

---

# 27. Product Data Contract

Frontend harus memperlakukan response product sebagai object dengan struktur berikut:

```json
{
  "item_group_id": "string",
  "title": "string",
  "description": "string|null",
  "availability": "string|null",
  "condition": "string|null",
  "brand": "string|null",
  "link": "string|null",
  "google_product_category": "string|null",
  "product_type": "string|null",
  "quantity_to_sell_on_facebook": 0,
  "custom_label_0": "string|null",
  "custom_label_1": "string|null",
  "custom_label_2": "string|null",
  "custom_label_3": "string|null",
  "custom_label_4": "string|null",
  "custom_label_5": "string|null",
  "variant_color": [],
  "variant_size": [],
  "main_features": [],
  "sub_features": [],
  "headline": "string|null",
  "band": "string|null",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

Nilai aktual `variant_color`, `variant_size`, `main_features`, dan `sub_features` berasal dari database dan harus diperlakukan sebagai JSON.

Frontend tidak boleh mengarang struktur JSON yang tidak diberikan oleh API.

---

# 28. Variant Fields

## variant_color

Database type:

```text
jsonb
```

Default:

```json
[]
```

Field ini digunakan untuk menyimpan data variant warna.

Frontend harus mempertahankan JSON asli ketika melakukan edit.

---

## variant_size

Database type:

```text
jsonb
```

Default:

```json
[]
```

Field ini digunakan untuk menyimpan data variant ukuran.

Frontend harus mempertahankan JSON asli ketika melakukan edit.

---

# 29. Feature Fields

## main_features

Database type:

```text
jsonb
```

Digunakan untuk data fitur utama.

## sub_features

Database type:

```text
jsonb
```

Digunakan untuk data sub fitur.

Frontend tidak boleh mengubah JSON menjadi string biasa kecuali memang diperlukan oleh UI dan dikembalikan lagi ke JSON sebelum submit.

---

# 30. Product Identifier

Identifier utama produk adalah:

```text
item_group_id
```

Identifier ini merupakan:

```text
Primary Key
```

Semua operasi single-product:

```text
GET
PUT
PATCH
DELETE
```

menggunakan:

```text
item_group_id
```

sebagai identifier.

---

# 31. Query Parameter Reference

| Parameter      | Type   | Default | Fungsi                                           |
| -------------- | ------ | ------- | ------------------------------------------------ |
| `search`       | string | —       | Search title, item_group_id, product_type, brand |
| `product_type` | string | —       | Filter exact product type                        |
| `availability` | string | —       | Filter exact availability                        |
| `limit`        | number | `100`   | Jumlah record                                    |
| `offset`       | number | `0`     | Pagination offset                                |

---

# 32. Combined Query Example

```text
/apple-produk-kelola-produk
?search=iPhone
&product_type=iPhone
&availability=in%20stock
&limit=20
&offset=0
```

Frontend harus melakukan URL encoding untuk value query parameter.

---

# 33. Method Rules

| Method    | URL                                | Fungsi         |
| --------- | ---------------------------------- | -------------- |
| `GET`     | `/apple-produk-kelola-produk`      | List           |
| `GET`     | `/apple-produk-kelola-produk/{id}` | Detail         |
| `POST`    | `/apple-produk-kelola-produk`      | Create         |
| `PUT`     | `/apple-produk-kelola-produk/{id}` | Update         |
| `PATCH`   | `/apple-produk-kelola-produk/{id}` | Update         |
| `DELETE`  | `/apple-produk-kelola-produk/{id}` | Delete         |
| `OPTIONS` | `/apple-produk-kelola-produk`      | CORS preflight |

---

# 34. Frontend Rules

Frontend yang menggunakan dokumentasi ini harus mengikuti aturan berikut:

1. Gunakan Edge Function `apple-produk-kelola-produk` sebagai API CRUD.
2. Gunakan `item_group_id` sebagai identifier produk.
3. Jangan menggunakan field yang tidak tersedia pada API.
4. Jangan mengubah nama field API.
5. Jangan mengarang field database baru.
6. Jangan mengubah struktur JSON variant tanpa kebutuhan.
7. Jangan mengirim `item_group_id` sebagai field yang dapat diedit.
8. Untuk update, gunakan `item_group_id` pada URL.
9. Gunakan response `success` sebagai indikator keberhasilan operasi.
10. Gunakan `error` untuk menampilkan error dari API.
11. Gunakan `data` sebagai sumber data product.
12. Gunakan `count`, `limit`, dan `offset` untuk pagination.
13. Gunakan `search`, `product_type`, dan `availability` untuk filtering.
14. Jangan menggunakan mock product data apabila API tersedia.
15. Jangan mengubah kontrak API tanpa perubahan pada Edge Function.

---

# 35. Important — API Security

Function saat ini memiliki konfigurasi:

```text
verify_jwt = false
```

Artinya gateway Edge Function tidak melakukan verifikasi JWT otomatis untuk function ini.

Source function juga menggunakan:

```text
SUPABASE_SERVICE_ROLE_KEY
```

untuk membuat Supabase client.

Client tersebut mempunyai hak akses server-side dan dapat melewati RLS.

Karena itu:

**`SUPABASE_SERVICE_ROLE_KEY` tidak boleh pernah dimasukkan ke frontend.**

Frontend hanya boleh memanggil URL Edge Function.

Jangan menyalin:

```text
SUPABASE_SERVICE_ROLE_KEY
```

ke:

```text
HTML
JavaScript
React
TypeScript
Vite environment yang dikirim ke browser
GitHub
```

---

# 36. Current Database Security Note

Tabel:

```text
public.apple_produk
```

memiliki:

```text
RLS enabled = true
```

Namun Edge Function menggunakan service-role client sehingga operasi database dari function tidak bergantung pada policy RLS tabel seperti client browser biasa.

Authorization pada level Edge Function perlu diperhatikan karena:

```text
verify_jwt = false
```

Dengan konfigurasi saat ini, endpoint CRUD dapat menerima request tanpa JWT yang diverifikasi oleh platform.

Jangan menganggap `verify_jwt=false` sebagai authentication.

Jika function nantinya digunakan untuk operasi admin-only, authorization harus ditambahkan secara eksplisit pada function atau melalui mekanisme autentikasi yang sesuai.

---

# 37. Do Not Expose Server Secrets

Environment variable yang digunakan function:

```text
SUPABASE_URL
SUPABASE_SERVICE_ROLE_KEY
```

`SUPABASE_SERVICE_ROLE_KEY` adalah server secret.

Dokumentasi frontend hanya boleh mengetahui:

```text
API endpoint
request format
response format
field mapping
query parameter
HTTP method
```

Tidak boleh mengetahui nilai secret.

---

# 38. Source of Truth

Untuk implementasi frontend:

```text
dokumentasi.md
        ↓
apple-produk-kelola-produk
        ↓
public.apple_produk
```

Jika terdapat perbedaan antara asumsi frontend dan dokumentasi ini, gunakan kontrak API yang sebenarnya.

Jika Edge Function berubah, dokumentasi ini harus diperbarui agar tetap sinkron.

---

# 39. Current Function Behavior Summary

```text
apple-produk-kelola-produk
│
├── GET /
│   ├── search
│   ├── product_type
│   ├── availability
│   ├── limit
│   ├── offset
│   └── return list + count
│
├── GET /{item_group_id}
│   └── return single product
│
├── POST /
│   ├── require item_group_id
│   ├── require title
│   └── create product
│
├── PUT /{item_group_id}
│   └── update product
│
├── PATCH /{item_group_id}
│   └── update product
│
├── DELETE /{item_group_id}
│   └── delete product
│
└── OPTIONS
    └── CORS
```

---

# 40. Canonical Endpoint

Gunakan endpoint berikut sebagai endpoint utama:

```text
https://jhpbtooefyzdndstlzva.supabase.co/functions/v1/apple-produk-kelola-produk
```

Jangan membuat endpoint alternatif atau mengubah path function pada frontend tanpa perubahan backend.

---

# 41. Version

Dokumentasi ini mendeskripsikan implementasi aktual:

```text
Function:
apple-produk-kelola-produk

Version:
1
```

Dokumentasi harus dianggap sebagai **external API contract** untuk frontend dan AI yang mengimplementasikan aplikasi product management.

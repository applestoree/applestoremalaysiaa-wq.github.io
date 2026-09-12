-- Apple Store Malaysia
-- Migration: create public.apple_produk
-- Source: current Supabase schema for public.apple_produk

create table if not exists public.apple_produk (
  item_group_id text primary key,
  title text not null,
  description text,
  availability text default 'in stock',
  condition text default 'new',
  brand text default 'Apple',
  link text,
  google_product_category text,
  product_type text,
  quantity_to_sell_on_facebook integer default 0,
  custom_label_0 text default '',
  custom_label_1 text default '',
  custom_label_2 text default '',
  custom_label_3 text default '',
  custom_label_4 text default '',
  custom_label_5 text default '',
  variant_color jsonb default '[]'::jsonb,
  variant_size jsonb default '[]'::jsonb,
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  main_features jsonb,
  sub_features jsonb,
  headline text,
  rating jsonb default '{"count": 0, "average": 0}'::jsonb,
  reviews jsonb default '{"count": 0}'::jsonb
);

-- Keep the table protected when exposed through the Supabase Data API.
alter table public.apple_produk enable row level security;

-- Public product catalog: read-only for anonymous clients.
drop policy if exists anon_select_apple_produk on public.apple_produk;
create policy anon_select_apple_produk
  on public.apple_produk
  for select
  to anon
  using (true);

grant select on table public.apple_produk to anon;
grant select on table public.apple_produk to authenticated;

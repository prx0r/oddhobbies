-- Commerce core — multi-store product graph
-- Canonical DB for oddhobbies · ochema · stonedoorway (and future stores)
-- SQLite dialect. One file, many stores. Git tracks packs/docs, not this runtime DB.

PRAGMA foreign_keys = ON;

-- ============================================================
-- BRANDS + STORES
-- ============================================================
CREATE TABLE IF NOT EXISTS brands (
  id            TEXT PRIMARY KEY,              -- pogpet_oddhobb | ochema | stonedoorway
  name          TEXT NOT NULL,                 -- display brand
  tagline       TEXT,
  thesis        TEXT,                          -- one-line positioning
  country       TEXT DEFAULT 'GB',
  notes         TEXT,
  status        TEXT DEFAULT 'active',         -- active | draft | retired
  created_at    TEXT DEFAULT (datetime('now')),
  updated_at    TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS stores (
  id            TEXT PRIMARY KEY,              -- pogpet | ochema | stonedoorway
  brand_id      TEXT NOT NULL REFERENCES brands(id),
  store_name    TEXT NOT NULL,                 -- customer-facing
  currency      TEXT NOT NULL DEFAULT 'USD',   -- store currency (channel display)
  base_country  TEXT DEFAULT 'GB',
  status        TEXT DEFAULT 'draft',          -- draft | live | paused
  default_section TEXT,                        -- optional
  pack_path     TEXT,                          -- stores/<id>
  r2_prefix     TEXT,                          -- commerce/stores/<id>
  created_at    TEXT DEFAULT (datetime('now')),
  updated_at    TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_stores_brand ON stores(brand_id);

CREATE TABLE IF NOT EXISTS store_config (
  store_id      TEXT NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
  key           TEXT NOT NULL,
  value_json    TEXT NOT NULL,
  PRIMARY KEY (store_id, key)
);

-- Channel endpoints for a store (Etsy, Shopify, Pinterest, ads accounts)
CREATE TABLE IF NOT EXISTS channels (
  id            TEXT PRIMARY KEY,              -- etsy:pogpet | shopify:oddhobb | pinterest:ochema
  store_id      TEXT NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
  channel       TEXT NOT NULL,                 -- etsy | shopify | pinterest | meta | google | etsy_api
  shop_name     TEXT,
  external_id   TEXT,                          -- shop id / store id on platform
  domain        TEXT,
  currency      TEXT,
  auth_ref      TEXT,                          -- vault/env key NAME only
  status        TEXT DEFAULT 'draft',          -- draft | active | blocked
  notes         TEXT,
  UNIQUE (store_id, channel, shop_name)
);
CREATE INDEX IF NOT EXISTS idx_channels_store ON channels(store_id);

-- ============================================================
-- SUPPLIERS (shared across stores)
-- ============================================================
CREATE TABLE IF NOT EXISTS suppliers (
  id            TEXT PRIMARY KEY,              -- MAKR3D, PRINTIE, PRODIGI...
  name          TEXT NOT NULL,
  role          TEXT,
  url           TEXT,
  location      TEXT,
  region_focus  TEXT,
  company_ref   TEXT,
  monthly_fee   REAL DEFAULT 0,
  moq           INTEGER DEFAULT 1,
  white_label   INTEGER DEFAULT 1,
  etsy_integration TEXT,
  shopify_integration TEXT,
  api_base      TEXT,
  api_key_ref   TEXT,
  dispatch_days_note TEXT,
  branding_note TEXT,
  caveats       TEXT,
  status        TEXT DEFAULT 'documented',
  notes         TEXT,
  created_at    TEXT DEFAULT (datetime('now')),
  updated_at    TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS supplier_locations (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  supplier_id     TEXT NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
  city            TEXT,
  country_iso     TEXT,
  facility_note   TEXT,
  is_primary      INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS supplier_materials (
  supplier_id  TEXT NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
  material     TEXT NOT NULL,
  PRIMARY KEY (supplier_id, material)
);

CREATE TABLE IF NOT EXISTS supplier_cost_tiers (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  supplier_id     TEXT NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
  tier_code       TEXT NOT NULL,
  tier_name       TEXT,
  currency        TEXT NOT NULL DEFAULT 'GBP',
  amount          REAL NOT NULL,
  amount_usd_est  REAL,
  includes        TEXT,
  source          TEXT,
  source_note     TEXT,
  verified_on     TEXT,
  UNIQUE (supplier_id, tier_code)
);

CREATE TABLE IF NOT EXISTS supplier_lead_times (
  id                 INTEGER PRIMARY KEY AUTOINCREMENT,
  supplier_id        TEXT NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
  destination_region TEXT NOT NULL,
  production_days_min INTEGER,
  production_days_max INTEGER,
  transit_days_min   INTEGER,
  transit_days_max   INTEGER,
  total_days_min     INTEGER,
  total_days_max     INTEGER,
  customs_buyer_pays INTEGER DEFAULT 0,
  shipping_cost_note TEXT,
  source             TEXT,
  UNIQUE (supplier_id, destination_region)
);

-- ============================================================
-- PRODUCTS (store-scoped source of truth)
-- ============================================================
CREATE TABLE IF NOT EXISTS products (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  store_id        TEXT NOT NULL REFERENCES stores(id),
  sku             TEXT NOT NULL,               -- unique within store
  title           TEXT NOT NULL,
  short_name      TEXT,
  section         TEXT,                        -- store section taxonomy
  make            TEXT,                        -- 3d_print | flat_print | digital | kit | media
  material        TEXT,
  size_class      TEXT,
  dimensions_json TEXT,
  personalisation_json TEXT,
  description     TEXT,
  demand_evidence TEXT,
  ip_notes        TEXT,
  status          TEXT DEFAULT 'draft',        -- draft | draft_live | live | killed | later
  priority        TEXT,                        -- P0 | P1 | P2
  agent_sku       TEXT,                        -- consumer-facing code
  created_at      TEXT DEFAULT (datetime('now')),
  updated_at      TEXT DEFAULT (datetime('now')),
  UNIQUE (store_id, sku)
);
CREATE INDEX IF NOT EXISTS idx_products_store ON products(store_id);
CREATE INDEX IF NOT EXISTS idx_products_status ON products(status);
CREATE INDEX IF NOT EXISTS idx_products_section ON products(store_id, section);

CREATE TABLE IF NOT EXISTS product_suppliers (
  product_id   INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  supplier_id  TEXT NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
  role         TEXT NOT NULL DEFAULT 'primary',
  supplier_sku TEXT,
  notes        TEXT,
  PRIMARY KEY (product_id, supplier_id, role)
);

CREATE TABLE IF NOT EXISTS product_costs (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id      INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  supplier_id     TEXT NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
  tier_code       TEXT,
  currency        TEXT NOT NULL DEFAULT 'USD',
  unit_cost       REAL NOT NULL,
  cost_includes   TEXT,
  source          TEXT DEFAULT 'estimate',
  source_note     TEXT,
  effective_from  TEXT DEFAULT (date('now')),
  effective_to    TEXT,
  is_current      INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS product_retail_prices (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id  INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  channel     TEXT NOT NULL DEFAULT 'etsy',
  currency    TEXT DEFAULT 'USD',
  price       REAL NOT NULL,
  tier_code   TEXT,
  qty_min     INTEGER,
  qty_max     INTEGER,
  is_current  INTEGER DEFAULT 1,
  UNIQUE (product_id, channel, tier_code, qty_min)
);

CREATE TABLE IF NOT EXISTS product_files (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id  INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  file_type   TEXT NOT NULL,
  path_or_ref TEXT,
  status      TEXT DEFAULT 'needed',
  notes       TEXT
);

CREATE TABLE IF NOT EXISTS product_shipping (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id     INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  supplier_id    TEXT NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
  hub_region     TEXT,
  destination    TEXT NOT NULL,
  transit_days_min INTEGER,
  transit_days_max INTEGER,
  total_days_min INTEGER,
  total_days_max INTEGER,
  cost_to_user   TEXT,
  customs_note   TEXT,
  UNIQUE (product_id, supplier_id, destination)
);

-- ============================================================
-- LISTINGS (channel copies)
-- ============================================================
CREATE TABLE IF NOT EXISTS listings (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id      INTEGER REFERENCES products(id) ON DELETE SET NULL,
  store_id        TEXT NOT NULL REFERENCES stores(id),
  channel_id      TEXT REFERENCES channels(id),
  channel         TEXT NOT NULL,
  external_id     TEXT,
  external_sku    TEXT,
  title           TEXT,
  state           TEXT DEFAULT 'draft',
  channel_price   REAL,
  channel_currency TEXT,
  quantity        INTEGER,
  taxonomy_id     INTEGER,
  shipping_profile_id TEXT,
  readiness_state_id TEXT,
  tags            TEXT,
  materials       TEXT,
  personalisation_json TEXT,
  description_excerpt TEXT,
  production_partner_ids TEXT,
  is_personalizable INTEGER DEFAULT 0,
  UNIQUE (store_id, channel, external_id)
);
CREATE INDEX IF NOT EXISTS idx_listings_store ON listings(store_id);
CREATE INDEX IF NOT EXISTS idx_listings_product ON listings(product_id);

CREATE TABLE IF NOT EXISTS listing_addons (
  listing_id      INTEGER NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
  addon_sku       TEXT NOT NULL,
  addon_price     REAL NOT NULL,
  usual_price     REAL,
  supplier_id     TEXT REFERENCES suppliers(id),
  notes           TEXT,
  PRIMARY KEY (listing_id, addon_sku)
);

CREATE TABLE IF NOT EXISTS shop_policies (
  store_id             TEXT NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
  channel_id           TEXT REFERENCES channels(id),
  free_shipping        INTEGER DEFAULT 1,
  free_shipping_threshold REAL,
  threshold_enforcement TEXT,
  addon_prices_json    TEXT,
  notes                TEXT,
  PRIMARY KEY (store_id)
);

-- ============================================================
-- ASSETS (R2 + local; agent-readable labels)
-- ============================================================
CREATE TABLE IF NOT EXISTS assets (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  store_id        TEXT NOT NULL REFERENCES stores(id),
  asset_key       TEXT NOT NULL UNIQUE,         -- pogpet/XMAS-3D-ORNAMENT/hero-v1
  product_id      INTEGER REFERENCES products(id) ON DELETE SET NULL,
  sku             TEXT,
  asset_type      TEXT NOT NULL,                -- hero | lifestyle | detail | mockup | pin | pack
  role            TEXT,
  product_family  TEXT,
  scene           TEXT,
  composition     TEXT,
  mood            TEXT,
  visibility      TEXT,
  has_person      INTEGER,
  has_pet         INTEGER,
  colour_tags     TEXT,
  aspect          TEXT,
  channel_fit     TEXT,                         -- etsy|pinterest|shopify|instagram|agent
  suitability_json TEXT,
  mime            TEXT,
  width           INTEGER,
  height          INTEGER,
  storage         TEXT NOT NULL,                -- local | r2 | url
  path_or_url     TEXT NOT NULL,
  alt_text        TEXT,
  agent_blurb     TEXT,
  agent_keywords  TEXT,
  pinterest_copy  TEXT,
  shopify_alt     TEXT,
  license_note    TEXT,
  source          TEXT,
  confidence      TEXT,
  needs_review    INTEGER DEFAULT 0,
  created_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_assets_store ON assets(store_id);
CREATE INDEX IF NOT EXISTS idx_assets_product ON assets(product_id);
CREATE INDEX IF NOT EXISTS idx_assets_sku ON assets(store_id, sku);

-- ============================================================
-- AGENT CATALOG (consumer-facing projection — no costs/secrets)
-- ============================================================
CREATE TABLE IF NOT EXISTS agent_catalog (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  store_id       TEXT NOT NULL REFERENCES stores(id),
  product_id     INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  agent_sku      TEXT NOT NULL,
  display_name   TEXT NOT NULL,
  summary        TEXT NOT NULL,
  how_it_works   TEXT,
  personalisation_schema_json TEXT,
  price_tier     TEXT,
  gift_occasions TEXT,
  fulfilment_blurb TEXT,
  is_orderable   INTEGER DEFAULT 0,
  is_customisable INTEGER DEFAULT 1,
  created_at     TEXT DEFAULT (datetime('now')),
  UNIQUE (store_id, agent_sku)
);

CREATE TABLE IF NOT EXISTS personalisation_questions (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id    INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  question_key  TEXT NOT NULL,
  question_text TEXT NOT NULL,
  question_type TEXT NOT NULL,
  required      INTEGER DEFAULT 0,
  max_chars     INTEGER DEFAULT 1024,
  max_files     INTEGER DEFAULT 2,
  instructions  TEXT,
  etsy_ready    INTEGER DEFAULT 1,
  UNIQUE (product_id, question_key)
);

CREATE TABLE IF NOT EXISTS pins (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  store_id        TEXT NOT NULL REFERENCES stores(id),
  product_id      INTEGER REFERENCES products(id) ON DELETE SET NULL,
  asset_id        INTEGER REFERENCES assets(id) ON DELETE SET NULL,
  board           TEXT,
  title           TEXT,
  description     TEXT,
  destination_url TEXT,
  status          TEXT DEFAULT 'draft',
  scheduled_for   TEXT
);

-- ============================================================
-- ADS (run ads from product graph)
-- ============================================================
CREATE TABLE IF NOT EXISTS ad_campaigns (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  store_id      TEXT NOT NULL REFERENCES stores(id),
  channel_id    TEXT REFERENCES channels(id),
  channel       TEXT NOT NULL,                  -- pinterest | meta | google | etsy_ads
  name          TEXT NOT NULL,
  objective     TEXT,                           -- traffic | conversions | catalog
  status        TEXT DEFAULT 'draft',           -- draft | active | paused | ended
  budget_daily  REAL,
  budget_total  REAL,
  currency      TEXT,
  target_audience TEXT,
  notes         TEXT,
  created_at    TEXT DEFAULT (datetime('now')),
  updated_at    TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS ad_creatives (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  campaign_id   INTEGER NOT NULL REFERENCES ad_campaigns(id) ON DELETE CASCADE,
  store_id      TEXT NOT NULL REFERENCES stores(id),
  product_id    INTEGER REFERENCES products(id) ON DELETE SET NULL,
  asset_id      INTEGER REFERENCES assets(id) ON DELETE SET NULL,
  listing_id    INTEGER REFERENCES listings(id) ON DELETE SET NULL,
  name          TEXT,
  headline      TEXT,
  body          TEXT,
  destination_url TEXT,
  status        TEXT DEFAULT 'draft',
  notes         TEXT,
  created_at    TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS ad_spend_ledger (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  campaign_id   INTEGER REFERENCES ad_campaigns(id) ON DELETE SET NULL,
  store_id      TEXT NOT NULL REFERENCES stores(id),
  spend_date    TEXT NOT NULL,
  channel       TEXT,
  amount        REAL NOT NULL,
  currency      TEXT,
  impressions   INTEGER,
  clicks        INTEGER,
  conversions   INTEGER,
  revenue_attributed REAL,
  source        TEXT,                           -- manual | api | estimate
  notes         TEXT,
  UNIQUE (campaign_id, spend_date, channel)
);

-- ============================================================
-- SALES (track revenue per store/product)
-- ============================================================
CREATE TABLE IF NOT EXISTS orders (
  id                INTEGER PRIMARY KEY AUTOINCREMENT,
  store_id          TEXT NOT NULL REFERENCES stores(id),
  channel_id        TEXT REFERENCES channels(id),
  channel           TEXT NOT NULL,
  external_order_id TEXT,
  buyer_ref         TEXT,                       -- anon/minimal — never full PII in agent views
  currency          TEXT,
  total             REAL,
  status            TEXT DEFAULT 'placed',      -- placed | paid | fulfilled | refunded | unknown
  placed_at         TEXT,
  paid_at           TEXT,
  fulfilled_at      TEXT,
  refunded_at       TEXT,
  fulfilment_note   TEXT,
  source            TEXT DEFAULT 'manual',      -- manual | api | import
  created_at        TEXT DEFAULT (datetime('now')),
  updated_at        TEXT DEFAULT (datetime('now')),
  UNIQUE (store_id, channel, external_order_id)
);
CREATE INDEX IF NOT EXISTS idx_orders_store ON orders(store_id);

CREATE TABLE IF NOT EXISTS order_lines (
  id                INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id          INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  product_id        INTEGER REFERENCES products(id) ON DELETE SET NULL,
  sku               TEXT,
  qty               INTEGER NOT NULL DEFAULT 1,
  unit_price        REAL,
  line_total        REAL,
  fulfilment_supplier_id TEXT REFERENCES suppliers(id),
  fulfilment_status TEXT,                       -- pending | ordered | shipped | done | unknown
  notes             TEXT
);
CREATE INDEX IF NOT EXISTS idx_order_lines_order ON order_lines(order_id);

CREATE TABLE IF NOT EXISTS payouts (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id      INTEGER REFERENCES orders(id) ON DELETE SET NULL,
  store_id      TEXT NOT NULL REFERENCES stores(id),
  channel       TEXT,
  gross         REAL,
  channel_fee   REAL,
  net           REAL,
  supplier_cost REAL,
  margin        REAL,
  currency      TEXT,
  status        TEXT DEFAULT 'pending',
  paid_at       TEXT,
  notes         TEXT
);

-- ============================================================
-- OPS (store-scoped)
-- ============================================================
CREATE TABLE IF NOT EXISTS open_quotes (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  store_id     TEXT REFERENCES stores(id),
  supplier_id  TEXT REFERENCES suppliers(id),
  product_id   INTEGER REFERENCES products(id),
  item         TEXT NOT NULL,
  priority     TEXT DEFAULT 'P1',
  status       TEXT DEFAULT 'open',
  result_json  TEXT,
  requested_on TEXT DEFAULT (date('now')),
  completed_on TEXT
);

CREATE TABLE IF NOT EXISTS decisions (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  store_id    TEXT REFERENCES stores(id),
  topic       TEXT NOT NULL,
  decision    TEXT NOT NULL,
  rationale   TEXT,
  decided_on  TEXT DEFAULT (date('now')),
  source_doc  TEXT
);

CREATE TABLE IF NOT EXISTS graph_exports (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  store_id    TEXT NOT NULL REFERENCES stores(id),
  path        TEXT NOT NULL,
  node_count  INTEGER,
  edge_count  INTEGER,
  generated_at TEXT DEFAULT (datetime('now'))
);

-- ============================================================
-- VIEWS
-- ============================================================
CREATE VIEW IF NOT EXISTS v_stores AS
SELECT
  s.id AS id,
  s.id AS store_id,
  s.store_name,
  s.brand_id,
  b.name AS brand_name,
  s.currency,
  s.status,
  s.pack_path,
  s.r2_prefix,
  (SELECT COUNT(*) FROM products p WHERE p.store_id = s.id) AS product_count,
  (SELECT COUNT(*) FROM listings l WHERE l.store_id = s.id) AS listing_count,
  (SELECT COUNT(*) FROM assets a WHERE a.store_id = s.id) AS asset_count,
  (SELECT COUNT(*) FROM orders o WHERE o.store_id = s.id) AS order_count
FROM stores s
JOIN brands b ON b.id = s.brand_id;

CREATE VIEW IF NOT EXISTS v_products_current AS
SELECT
  p.id, p.store_id, p.sku, p.title, p.section, p.make, p.material, p.size_class,
  p.status, p.priority, p.demand_evidence, p.agent_sku,
  ps.supplier_id AS primary_supplier,
  ps.supplier_sku AS supplier_sku,
  pc.unit_cost AS current_unit_cost,
  pc.currency AS cost_currency,
  pc.cost_includes,
  pc.source AS cost_source,
  rp.price AS retail_price,
  rp.channel AS retail_channel
FROM products p
LEFT JOIN product_suppliers ps
  ON ps.product_id = p.id AND ps.role = 'primary'
LEFT JOIN product_costs pc
  ON pc.product_id = p.id AND pc.is_current = 1
 AND pc.supplier_id = ps.supplier_id
LEFT JOIN product_retail_prices rp
  ON rp.product_id = p.id AND rp.is_current = 1 AND rp.channel = 'etsy'
 AND rp.tier_code IS NULL
WHERE p.status IN ('draft','live','draft_live');

CREATE VIEW IF NOT EXISTS v_supplier_directory AS
SELECT
  s.id, s.name, s.role, s.location, s.region_focus,
  s.etsy_integration, s.shopify_integration,
  s.moq, s.monthly_fee, s.white_label,
  s.dispatch_days_note, s.status,
  (SELECT group_concat(tier_code || '=' || currency || amount, ', ')
     FROM supplier_cost_tiers t WHERE t.supplier_id = s.id) AS cost_tiers,
  (SELECT group_concat(destination_region || ': ' ||
      coalesce(total_days_min,'') || '-' || coalesce(total_days_max,'') || 'd', '; ')
     FROM supplier_lead_times l WHERE l.supplier_id = s.id) AS lead_times
FROM suppliers s;

CREATE VIEW IF NOT EXISTS v_product_fulfilment_matrix AS
SELECT
  p.store_id, p.sku, p.title, p.section,
  ps.supplier_id, ps.role AS supplier_role, ps.supplier_sku,
  pc.unit_cost, pc.currency AS cost_ccy, pc.cost_includes, pc.source AS cost_src,
  sl.destination, sl.total_days_min, sl.total_days_max,
  sl.cost_to_user, sl.customs_note
FROM products p
JOIN product_suppliers ps ON ps.product_id = p.id
LEFT JOIN product_costs pc
  ON pc.product_id = p.id AND pc.supplier_id = ps.supplier_id AND pc.is_current = 1
LEFT JOIN product_shipping sl
  ON sl.product_id = p.id AND sl.supplier_id = ps.supplier_id
WHERE p.status IN ('draft','live','draft_live')
ORDER BY p.store_id, p.section, p.sku, ps.role;

CREATE VIEW IF NOT EXISTS v_open_quotes AS
SELECT o.id, o.store_id, o.priority, o.item, o.status,
       s.name AS supplier, p.sku, p.title
FROM open_quotes o
LEFT JOIN suppliers s ON s.id = o.supplier_id
LEFT JOIN products p ON p.id = o.product_id
WHERE o.status = 'open'
ORDER BY o.priority, o.id;

CREATE VIEW IF NOT EXISTS v_agent_catalog AS
SELECT
  ac.id,
  ac.store_id,
  s.store_name,
  ac.agent_sku,
  ac.display_name,
  ac.summary,
  ac.how_it_works,
  ac.price_tier,
  ac.gift_occasions,
  ac.fulfilment_blurb,
  ac.is_orderable,
  ac.is_customisable,
  p.sku AS product_sku,
  p.section,
  rp.price AS display_price,
  rp.currency AS display_currency
FROM agent_catalog ac
JOIN products p ON p.id = ac.product_id
JOIN stores s ON s.id = ac.store_id
LEFT JOIN product_retail_prices rp
  ON rp.product_id = p.id AND rp.is_current = 1 AND rp.channel = 'etsy'
 AND rp.tier_code IS NULL;

CREATE VIEW IF NOT EXISTS v_sales_by_store AS
SELECT
  o.store_id,
  s.store_name,
  o.channel,
  o.status,
  COUNT(DISTINCT o.id) AS orders,
  SUM(o.total) AS revenue,
  o.currency
FROM orders o
JOIN stores s ON s.id = o.store_id
GROUP BY o.store_id, s.store_name, o.channel, o.status, o.currency;

CREATE VIEW IF NOT EXISTS v_sales_by_product AS
SELECT
  p.store_id,
  ol.sku,
  p.title,
  COUNT(ol.id) AS units,
  SUM(ol.line_total) AS revenue,
  SUM(COALESCE(pc.unit_cost, 0) * ol.qty) AS est_cost,
  SUM(ol.line_total) - SUM(COALESCE(pc.unit_cost, 0) * ol.qty) AS est_margin
FROM order_lines ol
JOIN products p ON p.id = ol.product_id
LEFT JOIN product_costs pc ON pc.product_id = p.id AND pc.is_current = 1
GROUP BY p.store_id, ol.sku, p.title;

CREATE VIEW IF NOT EXISTS v_asset_catalog AS
SELECT
  a.id, a.store_id, a.asset_key, a.sku, p.sku AS product_sku,
  a.asset_type, a.role, a.product_family, a.scene, a.mood,
  a.channel_fit, a.suitability_json, a.storage, a.path_or_url,
  a.alt_text, a.agent_blurb, a.agent_keywords, a.source, a.confidence,
  a.width, a.height, a.aspect
FROM assets a
LEFT JOIN products p ON p.id = a.product_id;

CREATE VIEW IF NOT EXISTS v_ad_readiness AS
SELECT
  p.store_id,
  p.sku,
  p.title,
  p.status,
  rp.price AS retail_price,
  rp.currency AS retail_currency,
  (SELECT COUNT(*) FROM assets a WHERE a.product_id = p.id) AS asset_count,
  (SELECT COUNT(*) FROM ad_creatives c WHERE c.product_id = p.id) AS creative_count,
  (SELECT l.external_id FROM listings l WHERE l.product_id = p.id AND l.state = 'active' LIMIT 1) AS live_listing_id
FROM products p
LEFT JOIN product_retail_prices rp
  ON rp.product_id = p.id AND rp.is_current = 1 AND rp.channel = 'etsy'
 AND rp.tier_code IS NULL
WHERE p.status IN ('draft','live','draft_live');

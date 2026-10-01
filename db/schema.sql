-- OddHobbies / PogPet canonical product-supplier DB
-- SQLite dialect. One DB for Etsy, Shopify, future channels.
-- Read via MCP or any SQL client.

PRAGMA foreign_keys = ON;

-- ============================================================
-- SUPPLIERS
-- ============================================================
CREATE TABLE IF NOT EXISTS suppliers (
  id            TEXT PRIMARY KEY,              -- MAKR3D, PRINTIE, PRODIGI...
  name          TEXT NOT NULL,
  role          TEXT,                          -- primary_3d_uk_world, flat_print...
  url           TEXT,
  location      TEXT,                          -- "Huddersfield, UK"
  region_focus  TEXT,                          -- UK, US, EU, GLOBAL
  company_ref   TEXT,
  monthly_fee   REAL DEFAULT 0,
  moq           INTEGER DEFAULT 1,
  white_label   INTEGER DEFAULT 1,             -- 0/1
  etsy_integration TEXT,                       -- native, yes, none
  shopify_integration TEXT,
  api_base      TEXT,
  api_key_ref   TEXT,                          -- vault/env key NAME only, never raw secrets
  dispatch_days_note TEXT,
  branding_note TEXT,
  caveats       TEXT,
  status        TEXT DEFAULT 'documented',     -- connected | documented | rejected
  notes         TEXT,
  created_at    TEXT DEFAULT (datetime('now')),
  updated_at    TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS supplier_locations (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  supplier_id     TEXT NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
  city            TEXT,
  country_iso     TEXT,                        -- GB, US, LV, DE...
  facility_note   TEXT,
  is_primary      INTEGER DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_supplier_locations_supplier ON supplier_locations(supplier_id);

CREATE TABLE IF NOT EXISTS supplier_materials (
  supplier_id  TEXT NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
  material     TEXT NOT NULL,                  -- PLA, PETG, paper, metal...
  PRIMARY KEY (supplier_id, material)
);

-- Size-class or SKU cost tiers (Makr3D small/mid/large, Prodigi SKUs...)
CREATE TABLE IF NOT EXISTS supplier_cost_tiers (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  supplier_id     TEXT NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
  tier_code       TEXT NOT NULL,               -- small, medium, large, PET-MET-BONE...
  tier_name       TEXT,
  currency        TEXT NOT NULL DEFAULT 'GBP',
  amount          REAL NOT NULL,
  amount_usd_est  REAL,                        -- FX estimate if not USD
  includes        TEXT,                        -- "fulfilment only" / "print+ship"
  source          TEXT,                        -- verified | quote | estimate
  source_note     TEXT,
  verified_on     TEXT,
  UNIQUE (supplier_id, tier_code)
);
CREATE INDEX IF NOT EXISTS idx_cost_tiers_supplier ON supplier_cost_tiers(supplier_id);

-- Lead time / shipping by destination from a supplier hub
CREATE TABLE IF NOT EXISTS supplier_lead_times (
  id                 INTEGER PRIMARY KEY AUTOINCREMENT,
  supplier_id        TEXT NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
  destination_region TEXT NOT NULL,            -- UK, US, EU, AU, ROW
  production_days_min INTEGER,
  production_days_max INTEGER,
  transit_days_min   INTEGER,
  transit_days_max   INTEGER,
  total_days_min     INTEGER,
  total_days_max     INTEGER,
  customs_buyer_pays INTEGER DEFAULT 0,
  shipping_cost_note TEXT,                     -- absorbed | bundled | Q
  source             TEXT,
  UNIQUE (supplier_id, destination_region)
);
CREATE INDEX IF NOT EXISTS idx_lead_supplier ON supplier_lead_times(supplier_id);

-- ============================================================
-- PRODUCTS
-- ============================================================
CREATE TABLE IF NOT EXISTS products (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  sku             TEXT NOT NULL UNIQUE,        -- XMAS-3D-TILE-RACK
  title           TEXT NOT NULL,
  short_name      TEXT,
  section         TEXT,                        -- Game Night | Weddings & Couples | Stocking
  make            TEXT,                        -- 3d_print | flat_print | custom_audio...
  material        TEXT,
  size_class      TEXT,                        -- small | mid | large
  dimensions_json TEXT,                        -- {"mm":[...] } flexible
  personalisation_json TEXT,                   -- ["name","colour"]
  description     TEXT,
  demand_evidence TEXT,
  ip_notes        TEXT,
  status          TEXT DEFAULT 'draft',        -- draft | live | killed | later
  priority        TEXT,                        -- P0 | P1 | P2
  created_at      TEXT DEFAULT (datetime('now')),
  updated_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_products_section ON products(section);
CREATE INDEX IF NOT EXISTS idx_products_status ON products(status);

-- Product <-> Supplier (role: primary, alt, us_lab, ...)
CREATE TABLE IF NOT EXISTS product_suppliers (
  product_id   INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  supplier_id  TEXT NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
  role         TEXT NOT NULL DEFAULT 'primary', -- primary | alt | us_lab | uk_lab | media
  supplier_sku TEXT,                            -- Prodigi PET-MET-BONE
  notes        TEXT,
  PRIMARY KEY (product_id, supplier_id, role)
);
CREATE INDEX IF NOT EXISTS idx_ps_supplier ON product_suppliers(supplier_id);
CREATE INDEX IF NOT EXISTS idx_ps_product ON product_suppliers(product_id);

-- Point-in-time unit costs (what we think fulfilment costs now)
CREATE TABLE IF NOT EXISTS product_costs (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id      INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  supplier_id     TEXT NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
  tier_code       TEXT,                         -- links to supplier_cost_tiers.tier_code
  currency        TEXT NOT NULL DEFAULT 'USD',
  unit_cost       REAL NOT NULL,
  cost_includes   TEXT,                         -- print only | print+ship | all-in
  source          TEXT DEFAULT 'estimate',      -- verified | quote | estimate
  source_note     TEXT,
  effective_from  TEXT DEFAULT (date('now')),
  effective_to    TEXT,                         -- NULL = current
  is_current      INTEGER DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_pc_product ON product_costs(product_id);
CREATE INDEX IF NOT EXISTS idx_pc_current ON product_costs(is_current);

CREATE TABLE IF NOT EXISTS product_retail_prices (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id  INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  channel     TEXT NOT NULL DEFAULT 'etsy',     -- etsy | shopify | wholesale
  currency    TEXT DEFAULT 'USD',
  price       REAL NOT NULL,
  tier_code   TEXT,                             -- e.g. tile rack volume tier
  qty_min     INTEGER,
  qty_max     INTEGER,
  is_current  INTEGER DEFAULT 1,
  UNIQUE (product_id, channel, tier_code, qty_min)
);

CREATE TABLE IF NOT EXISTS product_files (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id  INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  file_type   TEXT NOT NULL,                    -- STL | 3MF | art | SOP | template
  path_or_ref TEXT,
  status      TEXT DEFAULT 'needed',            -- needed | draft | ready
  notes       TEXT
);

CREATE TABLE IF NOT EXISTS product_shipping (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id     INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  supplier_id    TEXT NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
  hub_region     TEXT,                          -- UK | US | EU
  destination    TEXT NOT NULL,                 -- UK | US | EU | AU | ROW
  transit_days_min INTEGER,
  transit_days_max INTEGER,
  total_days_min INTEGER,
  total_days_max INTEGER,
  cost_to_user   TEXT,                          -- free_listing | bundled | buyer
  customs_note   TEXT,
  UNIQUE (product_id, supplier_id, destination)
);

-- ============================================================
-- CHANNEL LISTINGS (Etsy, Shopify, ...)
-- ============================================================
CREATE TABLE IF NOT EXISTS shops (
  id            TEXT PRIMARY KEY,               -- etsy:67863887
  channel       TEXT NOT NULL,                  -- etsy | shopify
  shop_name     TEXT NOT NULL,
  external_id   TEXT,                           -- etsy shop_id
  currency      TEXT DEFAULT 'USD',
  url           TEXT,
  notes         TEXT
);

CREATE TABLE IF NOT EXISTS listings (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id      INTEGER REFERENCES products(id) ON DELETE SET NULL,
  shop_id         TEXT NOT NULL REFERENCES shops(id),
  channel         TEXT NOT NULL,
  external_id     TEXT,                         -- etsy listing_id
  external_sku    TEXT,
  title           TEXT,
  state           TEXT DEFAULT 'draft',         -- draft | active | inactive | cut
  channel_price   REAL,
  channel_currency TEXT,
  quantity        INTEGER,
  taxonomy_id     INTEGER,
  shipping_profile_id TEXT,
  readiness_state_id TEXT,
  tags            TEXT,                         -- comma-separated or JSON
  materials       TEXT,
  personalisation_json TEXT,
  description_excerpt TEXT,
  production_partner_ids TEXT,                  -- JSON array
  is_personalizable INTEGER DEFAULT 0,
  UNIQUE (shop_id, external_id)
);
CREATE INDEX IF NOT EXISTS idx_listings_product ON listings(product_id);
CREATE INDEX IF NOT EXISTS idx_listings_state ON listings(state);
CREATE INDEX IF NOT EXISTS idx_listings_shop ON listings(shop_id);

CREATE TABLE IF NOT EXISTS listing_addons (
  listing_id      INTEGER NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
  addon_sku       TEXT NOT NULL,                -- ADDON-STICKER
  addon_price     REAL NOT NULL,
  usual_price     REAL,
  supplier_id     TEXT REFERENCES suppliers(id),
  notes           TEXT,
  PRIMARY KEY (listing_id, addon_sku)
);

CREATE TABLE IF NOT EXISTS shop_policies (
  shop_id              TEXT NOT NULL REFERENCES shops(id) ON DELETE CASCADE,
  free_shipping        INTEGER DEFAULT 1,
  free_shipping_threshold_usd REAL,
  threshold_enforcement TEXT,                   -- copy_only | shop_manager_guarantee
  addon_sticker_usd    REAL,
  addon_postcard_usd   REAL,
  xmas_order_by_note   TEXT,
  notes                TEXT,
  PRIMARY KEY (shop_id)
);

-- ============================================================
-- OPS / OPEN WORK
-- ============================================================
CREATE TABLE IF NOT EXISTS open_quotes (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  supplier_id  TEXT REFERENCES suppliers(id),
  product_id   INTEGER REFERENCES products(id),
  item         TEXT NOT NULL,
  priority     TEXT DEFAULT 'P1',               -- P0 | P1 | P2
  status       TEXT DEFAULT 'open',             -- open | done | blocked
  result_json  TEXT,                            -- fill when quote lands
  requested_on TEXT DEFAULT (date('now')),
  completed_on TEXT
);

CREATE TABLE IF NOT EXISTS decisions (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  topic       TEXT NOT NULL,                    -- supplier_pick | kill | pricing
  decision    TEXT NOT NULL,
  rationale   TEXT,
  decided_on  TEXT DEFAULT (date('now')),
  source_doc  TEXT
);

-- ============================================================
-- VIEWS — handy for MCP / tools
-- ============================================================
CREATE VIEW IF NOT EXISTS v_products_current AS
SELECT
  p.id, p.sku, p.title, p.section, p.make, p.material, p.size_class,
  p.status, p.priority, p.demand_evidence,
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
  p.sku, p.title, p.section,
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
ORDER BY p.section, p.sku, ps.role;

CREATE VIEW IF NOT EXISTS v_open_quotes AS
SELECT o.id, o.priority, o.item, o.status,
       s.name AS supplier, p.sku, p.title
FROM open_quotes o
LEFT JOIN suppliers s ON s.id = o.supplier_id
LEFT JOIN products p ON p.id = o.product_id
WHERE o.status = 'open'
ORDER BY o.priority, o.id;

CREATE VIEW IF NOT EXISTS v_etsy_drafts AS
SELECT
  l.external_id AS etsy_listing_id,
  l.state,
  p.sku,
  p.section,
  l.title,
  l.channel_price,
  l.taxonomy_id,
  l.shipping_profile_id,
  l.readiness_state_id,
  l.quantity,
  ps.supplier_id AS primary_supplier
FROM listings l
LEFT JOIN products p ON p.id = l.product_id
LEFT JOIN product_suppliers ps
  ON ps.product_id = p.id AND ps.role = 'primary'
WHERE l.channel = 'etsy' AND l.state = 'draft'
ORDER BY p.section, p.sku;

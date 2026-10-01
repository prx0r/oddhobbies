-- Consumer / agent-facing layers (additive to schema.sql)
-- Re-run seed after applying, or: sqlite3 oddhobbies.db < schema_consume.sql

PRAGMA foreign_keys = ON;

-- Digital + physical assets we own (NOT scraped from Etsy)
-- Source of truth for Pinterest, Shopify, ChatGPT/MCP, listing photos
CREATE TABLE IF NOT EXISTS assets (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  asset_key       TEXT NOT NULL UNIQUE,          -- tile-rack-hero-v1
  product_id      INTEGER REFERENCES products(id) ON DELETE SET NULL,
  asset_type      TEXT NOT NULL,                 -- hero | lifestyle | mockup | pin | video_still | pack
  channel_fit     TEXT,                          -- etsy|pinterest|shopify|instagram|agent
  mime            TEXT,                          -- image/png
  width           INTEGER,
  height          INTEGER,
  storage         TEXT NOT NULL,                 -- local | r2 | url
  path_or_url     TEXT NOT NULL,
  alt_text        TEXT,
  pinterest_copy  TEXT,                          -- ready pin title/desc
  shopify_alt     TEXT,
  license_note    TEXT,
  created_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_assets_product ON assets(product_id);
CREATE INDEX IF NOT EXISTS idx_assets_type ON assets(asset_type);

-- Consumer MCP catalog (what an AI agent may expose to buyers)
-- Distinct from internal ops MCP tools
CREATE TABLE IF NOT EXISTS agent_catalog (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id     INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  agent_sku      TEXT NOT NULL UNIQUE,           -- consumer-facing code
  display_name   TEXT NOT NULL,
  summary        TEXT NOT NULL,                  -- 1-2 sentence pitch
  how_it_works   TEXT,                           -- numbered steps text
  personalisation_schema_json TEXT,              -- JSON schema for customisation questions
  price_tier     TEXT,                           -- impulse | treat | gift
  gift_occasions TEXT,                           -- christmas, anniversary, wedding
  fulfilment_blurb TEXT,                         -- "3D printed in UK, 5-8 days"
  is_orderable   INTEGER DEFAULT 0,              -- 0 until live+images+partners
  is_customisable INTEGER DEFAULT 1,
  created_at     TEXT DEFAULT (datetime('now'))
);

-- Personalisation questions the agent can ask (maps to Etsy personalization later)
CREATE TABLE IF NOT EXISTS personalisation_questions (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id    INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  question_key  TEXT NOT NULL,                   -- names, photos, style_notes
  question_text TEXT NOT NULL,                   -- <=45 chars for Etsy
  question_type TEXT NOT NULL,                   -- text_input | labeled_upload | dropdown
  required      INTEGER DEFAULT 0,
  max_chars     INTEGER DEFAULT 1024,
  max_files     INTEGER DEFAULT 2,
  instructions  TEXT,
  etsy_ready    INTEGER DEFAULT 1,
  UNIQUE (product_id, question_key)
);

-- Social / Pinterest pins
CREATE TABLE IF NOT EXISTS pins (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id   INTEGER REFERENCES products(id) ON DELETE SET NULL,
  asset_id     INTEGER REFERENCES assets(id) ON DELETE SET NULL,
  board        TEXT,                             -- game-night, weddings, xmas
  title        TEXT,
  description  TEXT,
  destination_url TEXT,
  status       TEXT DEFAULT 'draft',             -- draft | scheduled | published
  scheduled_for TEXT
);

-- Agent sessions / customisation quotes (future consumer MCP)
CREATE TABLE IF NOT EXISTS agent_requests (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id     INTEGER REFERENCES products(id),
  agent_sku      TEXT,
  channel        TEXT,                           -- chatgpt | website | etsy
  inputs_json    TEXT,                           -- buyer customisation payload
  quote_json     TEXT,
  status         TEXT DEFAULT 'received',        # received | quoted | ordered | cancelled
  created_at     TEXT DEFAULT (datetime('now'))
);

CREATE VIEW IF NOT EXISTS v_agent_catalog AS
SELECT
  a.agent_sku,
  a.display_name,
  a.summary,
  a.price_tier,
  a.gift_occasions,
  a.fulfilment_blurb,
  a.is_orderable,
  a.is_customisable,
  p.sku,
  p.section,
  p.material,
  rp.price AS retail_price,
  ps.supplier_id AS primary_supplier,
  (SELECT group_concat(question_text, ' | ')
     FROM personalisation_questions q
    WHERE q.product_id = p.id) AS agent_questions,
  (SELECT group_concat(asset_type || ':' || path_or_url, '; ')
     FROM assets s WHERE s.product_id = p.id) AS asset_refs
FROM agent_catalog a
JOIN products p ON p.id = a.product_id
LEFT JOIN product_retail_prices rp
  ON rp.product_id = p.id AND rp.is_current = 1 AND rp.channel='etsy'
 AND rp.tier_code IS NULL
LEFT JOIN product_suppliers ps
  ON ps.product_id = p.id AND ps.role = 'primary';

CREATE VIEW IF NOT EXISTS v_pinterest_ready AS
SELECT
  p.sku, p.title AS product_title, p.section,
  ass.asset_key, ass.path_or_url, ass.alt_text, ass.width, ass.height,
  pin.board, pin.title AS pin_title, pin.description AS pin_description,
  pin.destination_url
FROM assets ass
JOIN products p ON p.id = ass.product_id
LEFT JOIN pins pin ON pin.asset_id = ass.id
WHERE ass.channel_fit LIKE '%pinterest%'
   OR pin.id IS NOT NULL
ORDER BY p.section, p.sku;

-- Channel listing templates (Etsy / Shopify / Pinterest / agent)
-- One canonical product → channel-specific payload generators

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS channel_templates (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  template_key  TEXT NOT NULL UNIQUE,     -- etsy_standard | shopify_product | pinterest_pin | agent_catalog
  channel       TEXT NOT NULL,            -- etsy | shopify | pinterest | agent
  version       TEXT NOT NULL DEFAULT '1',
  title         TEXT NOT NULL,
  description   TEXT,
  -- field rules as JSON for generators/agents
  fields_json   TEXT NOT NULL,
  -- slot checklist (photo/pin creative)
  slots_json    TEXT,
  validation_json TEXT,
  source_note   TEXT,                     -- GitHub/Etsy handbook refs
  is_active     INTEGER DEFAULT 1,
  created_at    TEXT DEFAULT (datetime('now')),
  UNIQUE (channel, version)
);

-- Instantiated listing payloads per product per channel
CREATE TABLE IF NOT EXISTS channel_payloads (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id    INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  template_id   INTEGER NOT NULL REFERENCES channel_templates(id),
  channel       TEXT NOT NULL,
  status        TEXT DEFAULT 'draft',     -- draft | ready | published
  payload_json  TEXT NOT NULL,            -- filled template
  external_id   TEXT,                     -- etsy listing_id / shopify product id / pin id
  generated_at  TEXT DEFAULT (datetime('now')),
  UNIQUE (product_id, channel, template_id)
);

CREATE VIEW IF NOT EXISTS v_channel_templates AS
SELECT id, template_key, channel, version, title, description, is_active
FROM channel_templates WHERE is_active = 1;

CREATE VIEW IF NOT EXISTS v_channel_payloads AS
SELECT
  p.sku,
  p.title AS product_title,
  p.section,
  cp.channel,
  cp.status,
  ct.template_key,
  cp.external_id,
  cp.payload_json,
  cp.generated_at
FROM channel_payloads cp
JOIN products p ON p.id = cp.product_id
JOIN channel_templates ct ON ct.id = cp.template_id;

-- Asset labelling for agents (cannot "see" images)
-- Apply after schema_consume.sql

PRAGMA foreign_keys = ON;

-- Controlled vocabularies (agent-safe)
CREATE TABLE IF NOT EXISTS asset_vocab (
  vocab     TEXT NOT NULL,   -- role | scene | product_family | channel_fit | quality | composition
  value     TEXT NOT NULL,
  description TEXT,
  PRIMARY KEY (vocab, value)
);

-- Structured labels on assets (JSON blob for flexible extras + typed cols for queries)
ALTER TABLE assets ADD COLUMN role TEXT;                 -- hero | lifestyle | detail | size_chart | mockup | pin | process | packaging
ALTER TABLE assets ADD COLUMN product_family TEXT;       -- pet_chibi | brick_figure | game_night | album | flat_print
ALTER TABLE assets ADD COLUMN scene TEXT;                -- xmas_tree | desk | hand_hold | couple | flat_lay | studio_white
ALTER TABLE assets ADD COLUMN composition TEXT;          -- single_product | person_plus_product | product_in_hand | environment
ALTER TABLE assets ADD COLUMN mood TEXT;                 -- festive | playful | premium | cosy | clean
ALTER TABLE assets ADD COLUMN visibility TEXT;           -- face_clear | product_clear | product_partial | abstract
ALTER TABLE assets ADD COLUMN has_person INTEGER;        -- 0/1
ALTER TABLE assets ADD COLUMN has_pet INTEGER;           -- 0/1
ALTER TABLE assets ADD COLUMN colour_tags TEXT;          -- comma: gold,red,cream
ALTER TABLE assets ADD COLUMN aspect TEXT;               -- 1:1 | 4:5 | 2:3 | 16:9
ALTER TABLE assets ADD COLUMN suitability_json TEXT;     -- {"etsy_hero":true,"pinterest":true,"shopify_gallery":false}
ALTER TABLE assets ADD COLUMN agent_blurb TEXT;          -- 1 sentence an agent can use without seeing image
ALTER TABLE assets ADD COLUMN agent_keywords TEXT;       -- search terms
ALTER TABLE assets ADD COLUMN source TEXT;               -- etsy_import | local_mock | generated | photo_shoot
ALTER TABLE assets ADD COLUMN confidence TEXT;           -- high | medium | low (how sure labels are)
ALTER TABLE assets ADD COLUMN needs_review INTEGER DEFAULT 0;

-- Embeddings later (optional)
CREATE TABLE IF NOT EXISTS asset_embeddings (
  asset_id    INTEGER PRIMARY KEY REFERENCES assets(id) ON DELETE CASCADE,
  model       TEXT NOT NULL,
  dim         INTEGER NOT NULL,
  vector_json TEXT NOT NULL,
  created_at  TEXT DEFAULT (datetime('now'))
);

-- Agent search view — no image required
CREATE VIEW IF NOT EXISTS v_asset_catalog AS
SELECT
  a.id,
  a.asset_key,
  a.role,
  a.product_family,
  a.product_id,
  p.sku,
  p.section,
  a.scene,
  a.composition,
  a.mood,
  a.visibility,
  a.has_person,
  a.has_pet,
  a.colour_tags,
  a.aspect,
  a.agent_blurb,
  a.agent_keywords,
  a.alt_text,
  a.pinterest_copy,
  a.source,
  a.confidence,
  a.needs_review,
  a.storage,
  a.path_or_url,
  a.channel_fit,
  COALESCE(a.suitability_json, '{}') AS suitability
FROM assets a
LEFT JOIN products p ON p.id = a.product_id;

-- How to pick an image for a job
CREATE VIEW IF NOT EXISTS v_asset_pick AS
SELECT
  a.asset_key,
  p.sku,
  a.product_family,
  a.role,
  a.scene,
  a.composition,
  a.agent_blurb,
  a.path_or_url,
  CASE
    WHEN a.role = 'hero' AND a.visibility = 'product_clear' AND a.composition IN ('single_product','product_in_hand') THEN 100
    WHEN a.role = 'lifestyle' AND a.has_person = 1 THEN 80
    WHEN a.role = 'mockup' THEN 60
    WHEN a.role = 'pin' THEN 55
    ELSE 40
  END AS etsy_score,
  CASE
    WHEN a.aspect IN ('2:3','4:5') OR a.role = 'pin' THEN 90
    WHEN a.mood IN ('festive','playful','cosy') THEN 70
    ELSE 40
  END AS pinterest_score
FROM assets a
LEFT JOIN products p ON p.id = a.product_id
WHERE a.needs_review = 0;

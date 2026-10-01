# Asset labelling for agents

> Agents can’t “see” images well. They pick assets from **structured labels + blurbs**.  
> Humans still curate; agents search and route.

---

## Principle

```
file in R2  +  labels in SQLite  +  agent_blurb  =  agent-usable assets
```

An agent never opens a JPG to answer “which image for Etsy hero on the ornament?”

---

## Label fields (on `assets`)

| Field | Values | Use |
|-------|--------|-----|
| `role` | hero, lifestyle, detail, size_chart, mockup, pin, process, packaging | Job type |
| `product_family` | brick_figure, pet_chibi, ornament, game_night, album, flat_print | Which product line |
| `scene` | xmas_tree, desk, hand_hold, couple, flat_lay, studio_white, bokeh_lights | Context |
| `composition` | single_product, person_plus_product, product_in_hand, environment | Framing |
| `mood` | festive, playful, premium, cosy, clean | Brand feel |
| `visibility` | face_clear, product_clear, product_partial, abstract | What reads |
| `has_person` / `has_pet` | 0/1 | Filters |
| `colour_tags` | comma list | Palette match |
| `aspect` | 1:1, 4:5, 2:3, 16:9 | Channel crop |
| `suitability_json` | `{etsy_hero, pinterest, shopify_gallery, weddings_section…}` | Channel flags |
| **`agent_blurb`** | 1 sentence | **Primary text for agents** |
| `agent_keywords` | search terms | LIKE search |
| `source` | etsy_import, local_mock, generated, photo_shoot | Provenance |
| `confidence` | high, medium, low | Trust labels |
| `needs_review` | 0/1 | Human QA |

Vocab table: `asset_vocab` (controlled lists).

---

## MCP / SQL for agents

### Best image for a job
```sql
SELECT * FROM v_asset_pick
WHERE sku = 'XMAS-3D-ORNAMENT'
ORDER BY etsy_score DESC LIMIT 1;
```

```sql
SELECT * FROM v_asset_pick
WHERE product_family = 'brick_figure'
  AND composition IN ('product_in_hand','person_plus_product')
ORDER BY pinterest_score DESC LIMIT 5;
```

### Browse without images
```sql
SELECT asset_key, role, scene, agent_blurb, path_or_url
FROM v_asset_catalog
WHERE product_family = 'ornament' AND mood = 'festive';
```

```sql
SELECT * FROM v_asset_catalog
WHERE agent_keywords LIKE '%christmas%' AND has_pet = 1;
```

### Suggested MCP tools (consumer + ops)
| Tool | Args | Returns |
|------|------|---------|
| `assets_search` | `q`, `role?`, `product_family?`, `scene?`, `channel?` | labeled assets + blurbs |
| `assets_pick` | `sku`, `channel` (etsy\|pinterest\|shopify) | top N by score |
| `assets_get` | `asset_key` | full label row |
| `assets_bulk_meta` | `sku` | all assets for a product |

---

## Scoring heuristic (in `v_asset_pick`)

**Etsy hero**
- role=hero + visibility=product_clear + composition single/in-hand → 100
- lifestyle + person → 80
- mockup → 60

**Pinterest**
- aspect 2:3 or 4:5 or role=pin → 90
- mood festive/playful/cosy → 70

Agents **prefer high scores**; humans can override with `needs_review`.

---

## Workflow: add a new image

1. Save file to R2 `products/<SKU>/<role>-<n>.jpg`
2. Insert `assets` row (path = `r2://...`)
3. Fill labels + `agent_blurb` (template below)
4. Set `suitability_json` for channels
5. Agent/MCP can pick it; Etsy upload uses same path

### Blurb template
> **[What it is]** + **[context]** + **[why useful]**  
> *“Golden puppy ornament on Christmas tree with red ribbon — festive hero for Xmas pet ornament listing.”*

### Keywords template
`product, scene, gift occasion, material, audience`

---

## Seeded labels (existing 40)

| Bucket | Role | Family | Blurb gist |
|--------|------|--------|------------|
| Brick figure photos | lifestyle | brick_figure | Person holding brick figure, Xmas tree — scale/gift |
| Couple photos | lifestyle | brick_figure | Couple + brick couple — weddings/anniversary |
| Xmas ornament photos | lifestyle | ornament | Puppy ornament on tree — Xmas hero |
| Local previews | mockup | various | Price/spec cards — internal, not Etsy hero |

Run:
```bash
python3 /root/oddhobbies/db/seed_asset_labels.py
```

---

## Multi-VPS / R2

| Layer | Location |
|-------|----------|
| Bytes | R2 `powpowpow/oddhobbies/assets/...` |
| Labels | SQLite `assets` on primary VPS |
| Blurbs | Same row (no separate CMS needed) |
| Future CLIP/embeddings | `asset_embeddings` table |

Agent on VPS B: **API to primary** `assets_search` — don’t copy the whole DB.

---

## Rules

1. **Every public asset needs** `role` + `agent_blurb` + `agent_keywords`
2. **Mockups/price cards** → `suitability.etsy_hero=false` (agents won’t pick them as hero)
3. **Photos with people** → `has_person=1`, lifestyle role
4. **Xmas line** → `mood=festive`, scene xmas_tree/bokeh when true
5. **Confidence low** → `needs_review=1` until human confirms
6. Labels describe **what is in the frame**, not marketing fluff only

---

## Next

1. Add `assets_search` / `assets_pick` to ops MCP  
2. Label Game Night mockups when generated  
3. Optional: embedding model for “similar image” search  

# Consumer Agent MCP + Asset Pipeline

> Internal ops DB (`oddhobbies.db`) is the **source of truth**.  
> Consumer ChatGPT/plugin/MCP is a **read-mostly projection** of the same DB.  
> Pinterest / Shopify assets come from **our files**, not scraped Etsy images.

---

## Hard answer: can we pull images from Etsy right now?

**No.**

| Check | Result |
|-------|--------|
| Flagship drafts (tile rack, line reader, pegs, albums, pet tags) | **0 images** |
| Active PogPet drafts (brick figure etc.) | **0 images via API** |
| `GET /listings/{id}/images` | Empty / 404 on shop-scoped path |
| Why | We never uploaded listing photos — still blocked on images |

Etsy is **not** an asset library for us yet.  
**Assets must be generated or produced locally**, then:
1. Stored in `assets` table + R2/local
2. Uploaded to Etsy via `uploadListingImage`
3. Shared to Pinterest / Shopify from the same file

---

## Two MCP surfaces (same DB)

| | **Ops MCP** (now) | **Consumer Agent MCP** (later) |
|--|-------------------|--------------------------------|
| Audience | Us / agents building the store | ChatGPT plugin, Muse, website agent |
| Tools | `db_get_product`, `db_sql`, quotes | `shop_browse`, `shop_customise`, `shop_quote`, `shop_order` |
| Data | costs, lead times, listings | display name, summary, questions, price tier |
| Writes | costs, quotes, decisions | agent_requests only |
| Exposure | Full internal graph | `v_agent_catalog` only |

### Consumer tool sketch
```
shop.list_products({section?, gift_for?, budget?})
shop.get_product({agent_sku})
shop.customise({agent_sku, answers})   # validates personalisation schema
shop.quote({agent_sku, answers})       # price + lead time blurb
shop.place_order(...)                  # later → Etsy order / cart
```

### Personalisation rules already learned
- Etsy question text **≤45 chars**
- `max_allowed_characters` **1–1024**
- Max **2 files** per question
- Store schema in `personalisation_questions` → push to Etsy when live

---

## Schema additions (`schema_consume.sql`)

| Table | Purpose |
|-------|---------|
| `assets` | Our images: hero, lifestyle, Pinterest pin, Shopify alt |
| `agent_catalog` | Consumer SKU, pitch, occasions, orderable flag |
| `personalisation_questions` | Agent-facing customisation form |
| `pins` | Pinterest boards + copy + destination |
| `agent_requests` | Future customisation/quote log |

Views: `v_agent_catalog`, `v_pinterest_ready`

Apply:
```bash
sqlite3 /root/oddhobbies/db/oddhobbies.db < /root/oddhobbies/db/schema_consume.sql
```

---

## Asset pipeline (what we actually do)

```
STL / design
   → mockup / render / photo (Makr3D sample OR product_previews)
   → 10-slot Etsy set
   → Pinterest crops (2:3)
   → Shopify gallery
   → assets row + R2 path
```

### Where files can come from today
| Source | Path | Notes |
|--------|------|-------|
| PogPet previews | `/root/bwick/engine/product_previews/` | figure, ornament, wrap, sticker mocks |
| Generated cards | `/root/bwick/engine/generated_cards/` | album/card art direction |
| Product cards | `/root/bwick/engine/pogpet_cards/` | Xmas card templates |
| OddHobbies assets | `/root/oddhobbies/assets/` | mostly empty — generate here |
| Grimoirer | `/root/grimoirer/assets/` | occult line later |

**Next asset work:** render Game Night mockups (tile rack, pegs, line reader) into `oddhobbies/assets/game-night/` — even AI mockups beat zero images.

---

## Pinterest / Shopify sharing model

| Channel | Pull from | Copy source |
|---------|-----------|-------------|
| Pinterest | `assets` where `channel_fit` has pinterest | `pins.title/description` |
| Shopify | `assets` product gallery | `products.title` + summary |
| Etsy | upload from same `assets` path | `listings.title/tags` |
| ChatGPT agent | `v_agent_catalog` only | `agent_catalog.summary` |

**Rule:** one canonical image file → many channels. Never re-download from Etsy.

---

## Seed agent catalog (after schema applied)

Suggested agent SKUs (consumer-facing, not internal):

| agent_sku | product | orderable now? |
|-----------|---------|----------------|
| `tile-rack` | Tile Rack | 0 — need images + STL |
| `mahjong-line-reader` | Line Reader | 0 |
| `cribbage-pegs` | Pegs | 0 |
| `first-player-token` | Token | 0 |
| `cribbage-board` | Board | 0 |
| `memory-album` | Memory Album | 0 — need SOP + sample |
| `wedding-video-album` | Wedding album | 0 |
| `metal-pet-tag` | Pet tag | 0 — Prodigi live, need art |

`is_orderable=1` only when: images live + production partner + stock policy set.

---

## Implementation order

1. Apply `schema_consume.sql`  
2. Generate first asset batch → insert `assets` rows  
3. Fill `agent_catalog` + `personalisation_questions`  
4. Build consumer MCP as **second server** (`consumer_mcp.py`) reading only agent views  
5. Upload images to Etsy → flip `is_orderable`  
6. Pinterest scheduler reads `v_pinterest_ready`  
7. Shopify product sync from same assets + summaries  

---

## Files
- `db/schema.sql` — internal ops  
- `db/schema_consume.sql` — consumer/assets/pins  
- `db/mcp_server.py` — ops MCP  
- `db/README.md` — ops docs  
- this file — consumer + assets  

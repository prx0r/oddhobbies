# Channel templates (Etsy / Shopify / Pinterest / Agent)

> One canonical product → **template payloads** per channel.  
> Structures adapted from open-source projects + official platform shapes.

---

## GitHub patterns we borrowed

| Channel | Repo / source | What we took |
|---------|----------------|--------------|
| **Etsy** | [silennsong/etsy-listing-helper](https://github.com/silennsong/etsy-listing-helper) | Title ≤140, **13 tags ≤20 chars**, description blocks, materials, photo alt |
| **Etsy** | [eisenheiim/Contentsy](https://github.com/eisenheiim/Contentsy) | Draft publish via API, category playbooks |
| **Etsy** | [DynamicEndpoints/etsy-mcp](https://github.com/DynamicEndpoints/etsy-mcp) | create_listing parameter contract |
| **Etsy** | [TitAndAnium/etsy_listing_master](https://github.com/TitAndAnium/etsy_listing_master) | Tag structure, description sections |
| **Etsy** | [seerxo](https://github.com/semihbugrasezer/seerxo) | 13-tag rules, A/B titles |
| **Shopify** | [Shopify/shopify_transporter](https://github.com/Shopify/shopify_transporter) | Official **product CSV headers** |
| **Shopify** | [shopifypartners/product-csvs](https://github.com/shopifypartners/product-csvs) | Sample product CSV shape |
| **Shopify** | [doeixd/parse-shopify-csv](https://github.com/doeixd/parse-shopify-csv) | Variant/metafield hierarchy |
| **Shopify** | [gauranshahuja/shopify-listing-ai](https://github.com/gauranshahuja/shopify-listing-ai) | SEO body + taxonomy validation + draft gate |
| **Pinterest** | [vijaxx/pinforge](https://github.com/vijaxx/pinforge) | Pin creative pipeline + SEO pin copy |
| **Pinterest** | [arndvs/cast](https://github.com/arndvs/cast) | Multi-ratio creative brief (1x1 / 9x16 / …) |
| **Pinterest** | [pinterest/api-description](https://github.com/pinterest/api-description) | Pins/boards/ads API shapes |
| **Multi** | [boudydegeer/quicklist-ai](https://github.com/boudydegeer/quicklist-ai) | One product → many marketplaces |
| **Multi** | [pkp666/product-ai-listing-studio](https://github.com/pkp666/product-ai-listing-studio) | Platform field mapping |

---

## Templates in DB (`channel_templates`)

| template_key | Channel | Version |
|--------------|---------|---------|
| `etsy_standard_v1` | etsy | 1 |
| `shopify_product_v1` | shopify | 1 |
| `pinterest_pin_v1` | pinterest | 1 |
| `agent_catalog_v1` | agent | 1 |

Filled instances live in `channel_payloads` (product × template).

---

## Etsy template rules (hard)

| Field | Rule |
|-------|------|
| Title | ≤ **140** chars |
| Tags | **13**, each ≤ **20** chars, lowercase, no dupes |
| Description | Hook first **~160** chars; then HOW IT WORKS / WHAT YOU GET / IP / fulfilment |
| who_made | `collective` (production partners) |
| when_made | `made_to_order` |
| taxonomy_id | product-specific (1552 toys, 1554 board games, …) |
| shipping_profile_id | `316299492609` |
| readiness_state_id | `1518572416146` |
| Personalisation Q text | ≤ **45** chars |
| Personalisation max chars | **1–1024** |
| Max files | **2** |
| Brand marks | Never LEGO / Scrabble / Rummikub / Catan / MTG |

**10 photo slots:** hero · personalisation · in_use_hand · detail · packaging · size · lifestyle · occasion · variants · bundle

---

## Shopify template (CSV / Admin)

Canonical columns (from official transporter CSV):

```
Handle, Title, Body (HTML), Vendor, Type, Tags, Published,
Option1 Name, Option1 Value,
Variant SKU, Variant Grams, Variant Inventory Qty,
Variant Inventory Policy, Variant Fulfillment Service, Variant Price,
Variant Requires Shipping, Image Src, Image Position, Image Alt Text,
SEO Title, SEO Description, Status
```

| Rule | Value |
|------|-------|
| Vendor | `OddHobbies` |
| Handle | slug from SKU (`xmas-3d-tile-rack`) |
| Published / Status | `FALSE` / `draft` until go-live |
| Fulfilment service | `manual` (or makr3d later) |
| SEO title | ≤70 chars |
| SEO description | ≤160 chars |

---

## Pinterest template

| Field | Rule |
|-------|------|
| Title | ≤100 chars: `{product} \| {occasion} \| {benefit}` |
| Description | ≤500 chars + CTA + URL |
| Aspect | **2:3** primary (1000×1500 min) |
| Also | 1:1 and 9:16 variants |
| Boards | game-night, christmas-gifts, weddings-couples, pet-gifts |
| Slots | hero_pin, lifestyle_pin, detail_pin, xmas_gift_pin |
| Assets | `assets_pick(sku, channel=pinterest)` |

---

## Agent template

**Expose:** agent_sku, display_name, summary, price_tier, gift_occasions, fulfilment_blurb, is_orderable  

**Never expose:** unit_cost, supplier notes, API keys, open quotes, production partner IDs  

---

## How agents / tools use this

```sql
SELECT * FROM v_channel_templates;

SELECT p.sku, cp.channel, cp.payload_json
FROM channel_payloads cp
JOIN products p ON p.id = cp.product_id
WHERE p.sku = 'XMAS-3D-TILE-RACK';
```

### MCP (add later)
| Tool | Args | Returns |
|------|------|---------|
| `channel_list_templates` | `channel?` | template contracts |
| `channel_get_payload` | `sku`, `channel` | filled payload |
| `channel_generate` | `sku`, `channel` | regenerate from product+assets |
| `channel_export_csv` | `channel=shopify` | CSV rows for import |

---

## Seed

```bash
python3 /root/oddhobbies/db/seed_channel_templates.py
```

Creates templates + payloads for all draft products (etsy / shopify / pinterest / agent).

---

## Extending

1. Add row to `channel_templates.fields_json` (or new `template_key` + version)  
2. Add generator in `seed_channel_templates.py` or a small Python module  
3. Re-seed payloads  
4. Agents always read **templates + payloads**, never invent platform rules  

Files:
- `db/schema_channel_templates.sql`
- `db/seed_channel_templates.py`
- this doc  

# Agent playbook — commerce core

How a future agent navigates this repo, sets up a store, populates listings,
runs ads, and connects to the rest of the system.

---

## 0. Read in this order

1. `AGENTS.md` — rules + map  
2. `docs/commerce/COMMERCE-GRAPH.md` — architecture  
3. `stores/README.md` — pack schema  
4. `stores/<store_id>/store.json` — brand truth  
5. MCP tools or `db/sql` views  

---

## 1. Discover stores

```bash
python3 db/seed_store.py --reset   # if DB missing/stale
# then MCP:
store_list
```

Or SQL:

```sql
SELECT store_id, store_name, brand_name, currency, status,
       product_count, listing_count, asset_count, order_count
FROM v_stores;
```

---

## 2. Read products for a store

```text
store_products { "store_id": "ochema" }
store_product  { "store_id": "ochema", "sku": "OCHEMA-KOS-DIGITAL" }
```

Ops view includes costs. Consumer agents use catalog tools only.

---

## 3. Set up a new store

1. Copy `stores/stonedoorway/` → `stores/<new_store>/`
2. Replace `store.json` (thesis, sections, style lock, channels)
3. Delete placeholder listing; add real packs
4. `python3 db/seed_store.py --store <new_store>`
5. `python3 db/export_graph.py --store <new_store>`
6. Add channel credentials as vault key **names** in `store.json` `auth_ref`
7. Push only when credentials work

Checklist:

- [ ] store.json complete (not TODO)
- [ ] ≥1 listing pack with IP-safe title/tags
- [ ] agent_sku set
- [ ] style lock written (images must match)
- [ ] seed + graph export green
- [ ] no secrets in packs

---

## 4. Populate listings (channel push)

### Shopify (works today for pogpet)

```bash
python3 shop/push_listings.py --store pogpet --channel shopify --dry-run
python3 shop/push_listings.py --store pogpet --channel shopify --sku OCHEMA-...
```

Writes `shopify_product_id` back into the pack JSON.

### Etsy

Blocked until OAuth. Packs already carry `etsy_listing_id` when drafts exist.
Do not invent tokens. See laptop OAuth flow; store refresh in vault as
`ETSY_REFRESH_TOKEN` when minted.

---

## 5. Assets (R2 + agent labels)

1. Generate images to match `store.json` `style_lock`
2. Save under local `assets/` or upload via R2 pattern:
   `commerce/stores/<store_id>/assets/<SKU>/<slot>.<ext>`
3. Insert/relabel in `assets` table (or seed from pack `assets_now`)
4. Agents read labels:

```text
assets_search { "store_id": "pogpet", "sku": "XMAS-3D-ORNAMENT", "role": "hero" }
assets_pick   { "store_id": "pogpet", "sku": "XMAS-3D-ORNAMENT", "channel": "etsy" }
```

**Never** scrape Etsy as our asset library. One canonical file → many channels.

---

## 6. Run ads

```text
ads_readiness { "store_id": "pogpet" }
ads_campaign_upsert {
  "store_id": "pogpet",
  "name": "Xmas Game Night — Pinterest",
  "channel": "pinterest",
  "objective": "conversions",
  "budget_daily": 5,
  "currency": "USD"
}
ads_creative_add {
  "campaign_id": 1,
  "sku": "XMAS-3D-TILE-RACK",
  "headline": "Personalised tile rack for game night",
  "body": "Magnetic rack, engraved name, gift-ready.",
  "destination_url": "https://www.etsy.com/shop/pogpet"
}
```

Creative source = `assets` + listing copy. Destination = live listing URL.
Log spend in `ad_spend_ledger` when ads are live.

---

## 7. Track sales

```text
sales_record {
  "store_id": "pogpet",
  "channel": "etsy",
  "external_order_id": "etsy-123",
  "currency": "USD",
  "lines": [{"sku": "XMAS-3D-ORNAMENT", "qty": 1, "unit_price": 14.99}]
}
sales_summary { "store_id": "pogpet" }
```

Later: channel order APIs write the same tables. Margin view:
`SELECT * FROM v_sales_by_product WHERE store_id='pogpet';`

---

## 8. Connect influence / social

| Need | Do |
|------|-----|
| Catalog for content agents | `store_agent_catalog` or `graph/<store_id>.json` |
| Brand voice / style | `store.json` style_lock + thesis |
| Order ops | influence task queue — human confirm on send/publish |
| Pins | `pins` table + `v_pinterest_ready` patterns (when enabled) |

**Boundary:** influence does not own product truth. It consumes the store graph
and writes tasks/receipts.

---

## 9. Consumer agents (ChatGPT / Muse / site)

```text
store_agent_catalog { "store_id": "ochema" }
store_product_public { "store_id": "ochema", "agent_sku": "kos-digital" }
```

Safe to expose: display name, summary, price tier, occasions, fulfilment blurb,
public assets.  
Never expose: unit cost, supplier API keys, vault paths, internal decisions.

---

## 10. Graph export (system links)

```bash
python3 db/export_graph.py --store pogpet
# → graph/pogpet.json  { nodes, edges, products, listings, assets, sales_summary, ad_readiness }
```

Edge vocabulary: `operates`, `channel`, `sells`, `listed_as`, `has_image`,
`exposed_as`.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `commerce.db` missing | `python3 db/seed_store.py --reset` |
| Unknown store_id | Check `stores/<id>/store.json` + `store_list` |
| Shopify 401 | Re-fetch `SHOPIFY_ACCESS_TOKEN`; see `shop/SHOPIFY-API.md` |
| Etsy 401 | OAuth not on this VPS — laptop re-auth |
| Wrong section/currency | Fix pack `section` / `store.json` then re-seed |
| IP mark in title | Edit pack; never push until clean |
| Assets missing for ads | Generate + label before campaign creatives |

---

## What not to do

- Do not create a second product DB per brand
- Do not hard-code store paths in new scripts — take `--store`
- Do not put secrets in packs or `graph/*.json`
- Do not mark `is_orderable=1` until images + fulfilment + policy exist
- Do not expand stonedoorway without a written thesis

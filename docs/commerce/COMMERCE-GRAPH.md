# Commerce graph — source of truth

> **What this repo is:** the objective multi-store product backend.
> oddhobbies · ochema · stonedoorway share **one engine**, not three forks.
> Future agents: start at `AGENTS.md` → this file → `stores/README.md`.

---

## One sentence

A single **store graph** (SQLite + packs + R2) that is the source of truth for
products across every brand — listings can be populated, assets read by agents,
ads and sales hang off the same product IDs, and other systems (influence,
consumer MCP, dashboards) connect by `store_id`.

---

## Layout

```
oddhobbies/
  AGENTS.md                 operator map (this system)
  stores/                   authoring packs per store
    pogpet/                 OddHobb (live pilot)
    ochema/                 Grimoirer grimoire/spell packs
    stonedoorway/           placeholder until thesis
  db/
    commerce.db             runtime multi-store DB (gitignored)
    schema_commerce.sql     canonical DDL
    seed_store.py           packs → commerce.db
    commerce_mcp.py         ops + consumer MCP tools
    export_graph.py         graph/<store_id>.json for other systems
  graph/                    machine-readable store graphs
  shop/
    push_listings.py        packs → Shopify (store-scoped)
  docs/commerce/            architecture + agent playbook
  assets/                   local copies; canonical paths are R2
```

Legacy: `db/oddhobbies.db` + `shop/listings/` is the **old single-store pilot**.
Authoring now lives under `stores/`. Do not add new SKUs to `shop/listings/`.

---

## Object model

```
brand ──< store ──< product ──< listing (channel copy)
                   │        ├──< asset (R2 + labels)
                   │        ├──< agent_catalog (consumer projection)
                   │        ├──< personalisation_questions
                   │        ├──< ad_creatives
                   │        └──< order_lines → orders → payouts
                   └──< channels (etsy / shopify / …)
```

**Hard keys**

| Object | Key | Example |
|--------|-----|---------|
| Brand | `brand_id` | `pogpet_oddhobb`, `grimoirer`, `stonedoorway` |
| Store | `store_id` | `oddhobb`, `grimoirer`, `stonedoorway` |
| Product | `(store_id, sku)` | `pogpet / XMAS-3D-ORNAMENT` |
| Agent SKU | `(store_id, agent_sku)` | `ochema / kos-digital` |
| Asset | `asset_key` | `pogpet/XMAS-3D-ORNAMENT/hero-v1` |
| Channel | `channel_id` | `shopify:oddhobb` |

---

## Canonical paths

| Layer | Path |
|-------|------|
| Store pack | `stores/<store_id>/store.json` |
| Listing packs | `stores/<store_id>/listings/<SKU>.json` |
| Runtime DB | `db/commerce.db` |
| Graph export | `graph/<store_id>.json` |
| R2 assets | `s3://powpowpow-warehouse/powpowpow/commerce/stores/<store_id>/assets/<SKU>/...` |
| Ops MCP | `python3 db/commerce_mcp.py` |

DB `assets.path_or_url` should use:
`r2://powpowpow-warehouse/powpowpow/commerce/stores/<store_id>/assets/...`

---

## Agent surfaces

| Surface | Audience | Tools / views |
|---------|----------|----------------|
| **Ops MCP** | us / building agents | `store_list`, `store_products`, `store_product`, `sales_*`, `ads_*`, `db_sql` |
| **Consumer MCP** | buyers / ChatGPT / Muse | `store_agent_catalog`, `store_product_public` — **no costs, no vault** |
| **Graph JSON** | influence, dashboards, research | `graph/<store_id>.json` nodes+edges |
| **Push scripts** | launch agents | `shop/push_listings.py --store <id>` |

---

## Connect other systems

### influence (ops / social / content)
- Read: `store_agent_catalog` / `graph/<id>.json` for catalog + brand voice
- Write: content tasks, order-queue tasks — **human-gated sends**
- Contract: `store_id` + product `agent_sku` / `sku`; never fork product truth

### Company graph / brand identity
- Brands and stores already carry thesis + channels + auth_ref **names**
- Export graph nodes: `brand`, `store`, `channel`, `product`, `agent_sku`, `asset`
- Credential material stays in agent-vault — never in packs or graph JSON

### Ads
1. `ads_readiness --store_id <id>` — needs price + assets (+ live listing when possible)
2. `ads_campaign_upsert` — draft campaign
3. `ads_creative_add` — bind product + asset + copy + destination
4. Spend later via `ad_spend_ledger` (manual → API)

### Sales
1. Manual: `sales_record` MCP tool or SQL into `orders` / `order_lines`
2. Channel sync later: Etsy/Shopify order APIs → same tables
3. Margin: `v_sales_by_product` uses current unit cost

---

## Extension rules

1. **One store = one pack dir + one `store_id` in DB.**
2. **Suppliers are shared** — never duplicate Makr3D rows per brand.
3. **Packs are not secrets** — vault key *names* only (`auth_ref`).
4. **Consumer views never leak** unit costs, supplier API keys, or raw order PII.
5. **Push is create-or-record** — write external IDs back into packs; later upgrade to update-by-id.
6. **IP scan before push** — no brand marks in titles/tags.
7. **Currency** comes from `store.json` `channel_currencies` — check before Shopify push.
8. **stonedoorway** stays empty until thesis exists.

---

## Build / ops commands

```bash
# seed all stores into commerce.db
python3 db/seed_store.py --reset

# seed one store
python3 db/seed_store.py --store ochema

# export graphs for other systems
python3 db/export_graph.py

# list live Shopify products (pogpet)
python3 shop/push_listings.py --store pogpet --channel shopify --list

# dry-run push
python3 shop/push_listings.py --store pogpet --channel shopify --dry-run

# ops MCP (stdio)
python3 db/commerce_mcp.py
```

---

## Status (2026-10-02)

| Store | Packs | Channels | Notes |
|-------|-------|----------|-------|
| **pogpet** | 15 SKUs | Shopify OddHobb live drafts · Etsy OAuth blocked | Pilot migrated into stores/ |
| **ochema** | 5 SKUs (digital + kits) | Etsy draft (no creds yet) | From grimoirer research |
| **stonedoorway** | template only | none | Thesis required |

Sales/ads tables exist and are empty — ready for first orders/campaigns.

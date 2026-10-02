# AGENTS.md — Commerce core (3 stores)

> **Definitive stores: `oddhobb` · `grimoirer` · `stonedoorway`.**
> No PogPet store. No Ochemy store. Read this first.

---

## What this is

Multi-store product graph: packs + SQLite + R2 + MCP + channel push + ads/sales tables.

| Layer | Where |
|-------|--------|
| Source of truth | `db/commerce.db` |
| Packs | `stores/<store_id>/` |
| MCP | `db/commerce_mcp.py` |
| Graph export | `graph/<store_id>.json` |
| Push | `shop/push_listings.py --store <id>` |

---

## Stores

| store_id | Brand | Domain | Email | Socials | Status |
|----------|-------|--------|-------|---------|--------|
| **oddhobb** | OddHobb | oddhobb.com | hello@oddhobb.com | @oddhobb | 15 packs · Shopify drafts live |
| **grimoirer** | Grimoirer | grimoirer.com | hello@grimoirer.com | @grimoirerhq | 4 packs · site/email live |
| **stonedoorway** | StoneDoorway | stonedoorway.com | hello@stonedoorway.com | @stonedoorway | thesis required |

Cloudflare zones active for all three domains · MX + hello@/orders@ routing live.

---

## How to work

```bash
python3 db/seed_store.py --reset
python3 db/export_graph.py
python3 db/commerce_mcp.py
python3 shop/push_listings.py --store oddhobb --channel shopify --dry-run
```

MCP tools: `store_list`, `store_get`, `store_products`, `store_agent_catalog`, `store_product_public`, `assets_*`, `sales_*`, `ads_*`, `graph_export`, `db_sql`.

**Consumer agents:** `store_agent_catalog` + `store_product_public` only.

---

## Rules

1. Only three store_ids exist  
2. Packs are git; `commerce.db` is not  
3. `store_id` on every pack, asset path, MCP filter  
4. No brand marks in titles/tags  
5. Secrets in vault only  
6. StoneDoorway: no SKUs/ads until thesis  
7. Grimoirer voice: scholarly, no spell guarantees  
8. OddHobb voice: warm gift / brick figures  

---

## Docs map

| Doc | Purpose |
|-----|---------|
| `docs/commerce/COMMERCE-GRAPH.md` | Architecture |
| `docs/commerce/BRAND-STACK.md` | CF + cmail + stevejobless map |
| `docs/commerce/SOCIALS.md` | Handle matrix |
| `docs/commerce/AGENT-PLAYBOOK.md` | Operator loop |
| `stores/*/IDENTITY.md` | Per-store identity |
| `stores/*/SOCIALS.md` | Per-store socials |

---

## Status (2026-10-02)

| Item | State |
|------|-------|
| 3-store rename | ✅ oddhobb · grimoirer · stonedoorway |
| CF domains + email | ✅ all three |
| Commerce schema/MCP/graph | ✅ |
| oddhobb packs | 15 · Shopify drafts |
| grimoirer packs | 4 · GRIMOIRER-* SKUs |
| stonedoorway | empty until thesis |
| Social claims | X/YT available — human signup |
| Photos / ads | next blockers |

**Spine:** `/root/bgraph` · site map: `docs/commerce/SITE-LINK.md`

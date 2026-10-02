# OddHobbies commerce core

> **Three stores: OddHobb · Grimoirer · StoneDoorway**
> Source of truth for products, listings, assets, ads, sales.

**Start:** [`AGENTS.md`](AGENTS.md) → [`docs/commerce/BRAND-STACK.md`](docs/commerce/BRAND-STACK.md) → [`stores/README.md`](stores/README.md)

## Stores

| store_id | Brand | Domain | Email |
|----------|-------|--------|-------|
| oddhobb | OddHobb | oddhobb.com | hello@oddhobb.com |
| grimoirer | Grimoirer | grimoirer.com | hello@grimoirer.com |
| stonedoorway | StoneDoorway | stonedoorway.com | hello@stonedoorway.com |

## Quick start

```bash
python3 db/seed_store.py --reset
python3 db/export_graph.py
python3 db/commerce_mcp.py
python3 shop/push_listings.py --store oddhobb --channel shopify --dry-run
```

## Layout

```
stores/{oddhobb,grimoirer,stonedoorway}/
db/          schema, seeder, MCP, graph export
graph/       store graphs
shop/        channel scripts
docs/commerce/  architecture + identity + socials
```

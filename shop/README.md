# Shop ops (channel push)

> Multi-store truth lives in `stores/` + `db/commerce.db`.
> This directory holds channel scripts and legacy single-store notes.

## Canonical paths

| What | Where |
|------|--------|
| Store packs | `../stores/<store_id>/` |
| Commerce DB | `../db/commerce.db` |
| Ops MCP | `../db/commerce_mcp.py` |
| Graph export | `../graph/<store_id>.json` |
| Agent playbook | `../docs/commerce/AGENT-PLAYBOOK.md` |

## Push listings

```bash
python3 shop/push_listings.py --store pogpet --channel shopify --list
python3 shop/push_listings.py --store pogpet --channel shopify --dry-run
python3 shop/push_listings.py --store pogpet --channel shopify --sku XMAS-3D-ORNAMENT
```

Legacy `shopify_push.py` still reads `shop/listings/` — prefer `push_listings.py`.

## Channels

| Store | Channel | Status |
|-------|---------|--------|
| pogpet | Shopify OddHobb `byg8sv-p6.myshopify.com` | Drafts live · token in vault/env |
| pogpet | Etsy PogPet `67863887` | OAuth blocked (laptop) |
| ochema | Etsy Ochema | Not created yet |

## Blockers

1. Product photos (style-locked per store)
2. Etsy OAuth re-auth
3. Production partner dashboards
4. Shopify update-by-id (create-only today)

See `../AGENTS.md` and `../docs/commerce/` for the full system map.

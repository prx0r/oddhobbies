# OddHobbies system docs

> Canonical map of this box’s commerce system.  
> **Start:** [`AGENTS.md`](../AGENTS.md)

---

## Docs index

| Doc | Read when |
|-----|-----------|
| [AGENTS.md](../AGENTS.md) | Any work on this system |
| [shop/README.md](shop/README.md) | Store state + listing packs |
| [shop/STORE-STRUCTURE.md](shop/STORE-STRUCTURE.md) | Sections / product lines |
| [shop/STORE-DESIGN.md](shop/STORE-DESIGN.md) | Brand look |
| [shop/LAUNCH-READY.md](shop/LAUNCH-READY.md) | Priority SKUs |
| [shop/listings/PROMPT-PACK.md](shop/listings/PROMPT-PACK.md) | ChatGPT image prompts |
| [shop/IMAGE-PROMPTS.md](shop/IMAGE-PROMPTS.md) | Prompt system + supplier specs |
| [shop/SHOPIFY-API.md](shop/SHOPIFY-API.md) | Token + push products |
| [shop/SHOPIFY-SETUP.md](shop/SHOPIFY-SETUP.md) | Create store / CSV |
| [shop/ETSY-OAUTH.md](shop/ETSY-OAUTH.md) | Etsy re-auth |
| [shop/FLAGSHIP-COSTS.md](shop/FLAGSHIP-COSTS.md) | Margins |
| [shop/US-3D-SUPPLIER.md](shop/US-3D-SUPPLIER.md) | Printie vs Makr3D |
| [shop/PRODIGI-XMAS-OPS.md](shop/PRODIGI-XMAS-OPS.md) | Prodigi SKUs / add-ons |
| [data/PRODUCT-SUPPLIER-DB.md](data/PRODUCT-SUPPLIER-DB.md) | Supplier costs |
| [db/README.md](db/README.md) | SQLite + MCP |
| [db/CHANNEL-TEMPLATES.md](db/CHANNEL-TEMPLATES.md) | Etsy/Shopify/Pinterest |
| [db/ASSET-LABELS.md](db/ASSET-LABELS.md) | Image labelling |
| [db/CONSUMER-MCP.md](db/CONSUMER-MCP.md) | Agent-facing catalog |
| [db/MULTI-VPS-ASSETS.md](db/MULTI-VPS-ASSETS.md) | R2 + multi-VPS |

---

## Quick commands

```bash
# Shopify products
python3 /root/oddhobbies/shop/shopify_push.py --list
python3 /root/oddhobbies/shop/shopify_push.py

# Rebuild DB
python3 /root/oddhobbies/db/seed.py
python3 /root/oddhobbies/db/seed_channel_templates.py
python3 /root/oddhobbies/db/seed_asset_labels.py

# Assets → R2
python3 /root/oddhobbies/db/r2_upload.py

# Ops MCP
python3 /root/oddhobbies/db/mcp_server.py
```

---

## Channels

| | Etsy | Shopify |
|--|------|---------|
| Brand | PogPet | OddHobb |
| Domain | etsy.com/shop/pogpet | byg8sv-p6.myshopify.com |
| API | OAuth (re-auth needed) | client_credentials (working) |
| Products | Drafts in DB | 15 drafts live |

---

## Agents

Internal agents: use MCP tools + this docs map.  
Consumer agents (later): `v_agent_catalog` only — no costs, no tokens.

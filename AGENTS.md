# AGENTS.md — OddHobbies / PogPet commerce system

> **You are the operator.** This box runs the multi-storefront product system.  
> Read this first. Then the files it points to.

---

## What this is

A **product + listing + asset system** for handmade/gift storefronts:

| Layer | What | Where |
|-------|------|-------|
| **Product truth** | SQLite DB (suppliers, costs, listings, assets) | `db/oddhobbies.db` |
| **Listing packs** | Title/tags/desc/personalisation per SKU | `shop/listings/*.json` |
| **Store design** | Sections, brand, prompts | `shop/*.md` |
| **Assets** | Product images (Etsy pulls + mocks) | `assets/` + Cloudflare R2 |
| **Fulfilment** | Makr3D / Printie / Prodigi / Kunaki | `data/product-supplier-db.json` |
| **Channels** | Etsy (discovery) + Shopify (own domain) | API scripts in `shop/` |

**Brand target:** couples brick figurine lifestyle — cream studio, Xmas energy, warm gift feel.  
**Whole store is Christmas** — do **not** create an Xmas shop section.

---

## Storefronts

| Channel | Identity | Status |
|---------|----------|--------|
| **Etsy** | PogPet · shop `67863887` | Drafts created earlier; API **OAuth expired** — re-auth on laptop when needed |
| **Shopify** | OddHobb · `byg8sv-p6.myshopify.com` | **15 draft products pushed** · currency **GBP** · API via client-credentials |

### Shopify API (working)
```
Domain: https://byg8sv-p6.myshopify.com
Auth:   client_credentials → shpat_ (expires ~24h)
Client: vault SHOPIFY_CLIENT_ID / SHOPIFY_CLIENT_SECRET
Script: shop/shopify_push.py
Env:    ~/.config/oddhobbies/shopify.env  (or agent-vault oracle)
```

Refresh token before write:
```bash
# script uses vault/env token; re-exchange if 401:
# grant_type=client_credentials + client_id + client_secret
python3 shop/shopify_push.py --list
python3 shop/shopify_push.py --sku ALBUM-MEMORY-CD
```

### Etsy API (blocked until re-auth)
- Shop 67863887 · keystring in vault historically  
- Need **browser OAuth** for `listings_w/d` + `shops_w`  
- Guide: `shop/ETSY-OAUTH.md`  
- Token lives on primary VPS / laptop callback — not on this VPS for 127.0.0.1 flows  

---

## Directory map

```
oddhobbies/
  AGENTS.md                 ← this file
  shop/                     ← storefront ops
    README.md               start here for store state
    STORE-STRUCTURE.md      sections (NO Christmas section)
    STORE-DESIGN.md         visual system
    LAUNCH-READY.md         priority table
    listings/               per-SKU JSON packs + PROMPT-PACK
    IMAGE-PROMPTS.md        ChatGPT image prompt system
    shopify_push.py         push packs → Shopify drafts
    SHOPIFY-SETUP.md        store create + CSV
    SHOPIFY-API.md          token + push
    ETSY-OAUTH.md           re-auth later
    FLAGSHIP-COSTS.md       margins + product lines
    US-3D-SUPPLIER.md       Printie vs Makr3D
    PRODIGI-XMAS-OPS.md     Prodigi add-ons
  db/                       ← canonical system
    oddhobbies.db           SQLite (gitignored — rebuild)
    schema*.sql             schemas
    seed*.py                rebuild from JSON
    mcp_server.py           ops MCP (stdio)
    r2_upload.py            assets → R2
    CHANNEL-TEMPLATES.md    Etsy/Shopify/Pinterest contracts
    CONSUMER-MCP.md         agent-facing design
    ASSET-LABELS.md         image labels for agents
    MULTI-VPS-ASSETS.md     R2 + single-writer DB
  data/
    product-supplier-db.json  supplier costs/specs
    PRODUCT-SUPPLIER-DB.md
  assets/
    etsy/                  photos pulled from Etsy API
    local/                 mockups / generated cards
    (R2: powpowpow/oddhobbies/assets/...)
```

---

## Product lines (current)

| Line | Examples | Supplier |
|------|----------|----------|
| **Brick figures** | Couple, solo, ornament | Makr3D / Printie |
| **3D game gifts** | Tile rack, mahjong, cribbage, tray, token, ornament | Makr3D / Printie |
| **CD albums** | Memory album, wedding video album | Kunaki / DiskCrafters |
| **Flat print** | Pet tags, Top Trumps, notebooks, coasters, cards | Prodigi |
| **Add-ons** | Stickers $3.99, postcards $2.99 | Prodigi |

**Keychains** (pet + brick) are in DB; not yet on Shopify (need listing packs + push).

---

## How to work here

### 1. Read state
```bash
cat oddhobbies/shop/README.md
ls oddhobbies/shop/listings/
python3 oddhobbies/db/mcp_server.py   # or sqlite3 oddhobbies.db
```

### 2. Change a product
1. Edit `shop/listings/<SKU>.json` (or DB `products` + `listings`)  
2. Rebuild DB if needed: `python3 oddhobbies/db/seed.py` (+ asset/channel seeds)  
3. Push Shopify: `python3 oddhobbies/shop/shopify_push.py --sku <SKU>`  
4. Etsy: only after OAuth works  

### 3. Add an image
1. Generate via `shop/listings/PROMPT-PACK.md` (ChatGPT)  
2. Save `assets/generated/<SKU>/`  
3. `python3 oddhobbies/db/r2_upload.py`  
4. Label in DB (`assets` table) → `assets_pick`  

### 4. New SKU checklist
- [ ] Product in DB + supplier cost  
- [ ] Listing pack JSON  
- [ ] Channel payload (Etsy + Shopify templates)  
- [ ] Image prompts  
- [ ] Etsy draft (when API works) + Shopify push  
- [ ] Photo slots filled  

---

## MCP (ops)

Register (if needed):
```json
{"mcpServers": {"oddhobbies-db": {"command": "python3", "args": ["/root/oddhobbies/db/mcp_server.py"]}}}
```

| Tool | Use |
|------|-----|
| `db_list_products` | What’s live/draft |
| `db_get_product` | Full graph: cost, shipping, listings |
| `assets_search` / `assets_pick` | Images without opening files |
| `channel_get_payload` | Etsy/Shopify draft payloads |
| `db_sql` | Read-only SQL (LIMIT 500) |

**Consumer agents later:** `v_agent_catalog` only — never unit costs/API keys.

---

## Secrets

| Secret | Where |
|--------|-------|
| Shopify client id/secret + domain | `agent-vault` oracle + `~/.config/oddhobbies/shopify.env` |
| Shopify access token (`shpat_`) | Minted via client_credentials (~24h); vault may hold last one |
| R2 keys | `agent-vault` (`R2_S3_*`, `CLOUDFLARE_R2_*`) |
| Etsy OAuth | Not on this VPS for laptop flows — see `shop/ETSY-OAUTH.md` |
| Prodigi API | Vault / docs — never commit |

**Never commit:** `.env`, tokens, `oddhobbies.db` runtime if secrets, raw client secrets in git.

---

## R2 assets

```
s3://powpowpow-warehouse/powpowpow/oddhobbies/assets/
  etsy/ACTIVE-BRICK-FIGURE/…
  etsy/ACTIVE-XMAS-ORNAMENT/…
  local/…
```
DB `assets.path_or_url` = `r2://powpowpow-warehouse/powpowpow/oddhobbies/assets/...`

---

## Rules

1. **SQLite single-writer** on this primary box — other VPSs read via API/MCP  
2. **Git = code + packs + docs** — not runtime DB binary (gitignored)  
3. **One canonical product** → channel payloads (Etsy/Shopify/Pinterest)  
4. **No brand marks** in titles/tags (LEGO, Scrabble, Catan, MTG)  
5. **Christmas is the whole store** — sections: Featured, Couples, Game Night, Physical Media, Add-Ons  
6. **Prodigi ≠ 3D** — 3D = Makr3D/Printie; albums = Kunaki; flat = Prodigi  
7. **Token expiry** — Shopify ~24h; Etsy access ~1h, refresh ~90d  
8. **Owner pushes git** — commit when asked; don’t push secrets  

---

## Related repos (same brand family)

| Repo | Role |
|------|------|
| `/root/oddhobbies` | This system (primary) |
| `/root/suppliers` | Shared supplier directory |
| `/root/bwick` | Figg/PogPet engine, Prodigi docs, brick figures |
| `/root/grimoirer` | Ochema occult brand (sister) |

---

## Status snapshot (2026-10-02)

| Item | State |
|------|-------|
| Shopify OddHobb | 15 draft products live via API |
| Etsy PogPet | Drafts exist; OAuth needs laptop re-auth |
| Product DB + MCP | Built |
| Image prompt pack | Ready for ChatGPT |
| Assets | 12 Etsy photos + local mocks in R2 |
| Keychains | In DB; not on Shopify yet |
| Bundles | Spec only — not built |
| Live product photos | **Main blocker** |

---

## When stuck

| Problem | Go to |
|---------|-------|
| Shopify 401 | Re-exchange client_credentials (`shop/SHOPIFY-API.md`) |
| Etsy 401 / scope | `shop/ETSY-OAUTH.md` — browser re-auth |
| Wrong product data | `data/product-supplier-db.json` + `db_get_product` |
| Image style | `shop/IMAGE-PROMPTS.md` + couple-brick brand target |
| Supplier cost | `db/v_supplier_directory` / MCP `db_list_suppliers` |

# Site ↔ commerce ↔ bgraph — live OddHobb structure

> Site engine: **`/root/pogpet`** (github.com/prx0r/pogpet)  
> Live brand: **oddhobb** · hosts oddhobb.com (+ pog.pet alias)  
> Pattern for all brands: **same app, brand config map** (see pogpet `docs/multi-brand.md`)

---

## One sentence

`pogpet` is the **consumer site + fulfilment pipeline** (photo→mesh→print, chat, Prodigi).  
`oddhobbies` is **product truth** (packs, costs, listings, orders).  
`bgraph` is **identity graph** (branches, content methods).  
They share `store_id` and brand hosts.

---

## Stack

```
                    BROWSER
                       │
              oddhobb.com  (Cloudflare tunnel → pogpet)
              grimoirer.com / stonedoorway.com (same app later)
                       │
              pogpet bridge :8797
              ┌────────┴────────┐
              │  site/ + studio │  consumer UI
              │  premesh/       │  image normaliser
              └────────┬────────┘
                       │ /backend proxy (token)
              pogpet Flask :8798
              photos → meshes → products → stage → print
              R2 via rclone (r2:figgsite or commerce bucket)
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
   oddhobbies      Shopify         Etsy
   commerce.db     byg8sv-p6 /     PogPet drafts
   packs+orders    feed sync       (OAuth later)
   graph export    sync-catalog
        │
        ▼
   bgraph organiser
   branches + methods
```

---

## store_id contract (all systems)

| store_id | Site host | Commerce packs | Shopify | R2 content prefix |
|----------|-----------|----------------|---------|-------------------|
| **oddhobb** | oddhobb.com · pog.pet | `oddhobbies/stores/oddhobb` | OddHobb drafts / feed | `content/stores/oddhobb` |
| **grimoirer** | grimoirer.com | `oddhobbies/stores/grimoirer` | later | `content/stores/grimoirer` |
| **stonedoorway** | stonedoorway.com | scaffold only | later | `content/stores/stonedoorway` |

Site `BRANDS` map keys are **domains**; each entry must carry `store_id` matching commerce + bgraph.

---

## Shared assets (how sites reuse product media)

| Source | Used by | Path |
|--------|---------|------|
| Commerce assets | listings, ads, content | `r2://…/commerce/stores/<id>/assets/…` |
| pogpet product renders | Shopify feed, site cards | `/img/` public mirrors + R2 `figgsite` |
| premesh stages | mesh pipeline | content-addressed under site zone |
| bgraph content (later) | YT/IG/TikTok | `content/stores/<id>/<branch>/…` |

**Rule:** one canonical product image set per store_id. Site renders and Shopify feed pull the same public URLs when possible; commerce DB holds labels + product links.

---

## Shopify link (already built in pogpet)

| Piece | Location |
|-------|----------|
| Catalog sync script | `pogpet/shopify-app/scripts/sync-catalog.mjs` |
| Auth notes | `pogpet/docs/shopify-auth.md` |
| Feed | `GET /backend/api/feeds/shopify.json` |
| Mapping | handle = product id · vendor OddHobb · price as feed |

**oddhobbies push_listings.py** is the *pack-based* path (15 SKUs).  
**pogpet sync-catalog** is the *mesh/personalised product* path.  
Both write Shopify — different catalogs until we unify SKUs.

### Unify later (recommended)

1. commerce `listings.external_id` + `shopify_handle`  
2. pogpet feed includes commerce `sku`  
3. One upsert script: packs → Shopify **and** mesh products → Shopify  
4. Orders: Shopify webhooks → commerce.db `orders`  

---

## Etsy link

- Discovery drafts live in oddhobbies listings packs (Etsy IDs).  
- pogpet also has listing-pack concepts for cards.  
- Single write path later: commerce packs → Etsy API after OAuth.  
- Site never owns Etsy truth.

---

## Multi-brand on the site

pogpet already supports:

```
BRANDS = {
  "oddhobb.com": {...},
  "ochema.co": {...},
  # add:
  "grimoirer.com": {...},
  "stonedoorway.com": {...},
}
```

`GET /api/brand` resolves by Host. Same app, new domain = tunnel CNAME + BRANDS entry.

**Definitive brands:** oddhobb · grimoirer · stonedoorway  
(ochema.co remains a zone/alias for Grimoirer if kept — prefer **grimoirer.com** as primary host.)

---

## What runs where

| Concern | Owner |
|---------|--------|
| Mesh / personalisation / Prodigi print | pogpet backend |
| Product packs, costs, listings, orders graph | oddhobbies |
| Identity branches + content methods | bgraph |
| Domains, email, R2 keys | Cloudflare + vault |
| Shopify catalog | pogpet feed sync + oddhobbies packs (to unify) |
| Etsy drafts | oddhobbies packs (after OAuth) |

---

## Next link steps

1. Add `store_id` + grimoirer/stonedoorway to pogpet `BRANDS`  
2. Tunnel CNAME for grimoirer.com / stonedoorway.com → figgsite tunnel  
3. Document feed ↔ pack SKU mapping table  
4. Optional: commerce export JSON → pogpet `/api/feeds/commerce.json`  
5. Orders webhooks → commerce.db  

See also: `/root/bgraph` (organiser), `/root/pogpet/docs/multi-brand.md`

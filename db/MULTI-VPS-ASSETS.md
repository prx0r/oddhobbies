# Multi-VPS + Cloudflare asset/DB architecture

> Date: 2026-10-01  
> Question: Cloudflare? How to work across multiple VPSs?  
> Answer: **R2 for assets + single source of truth for DB + git for code. Not “put SQLite on CF”.**

---

## Short answer

| Thing | Where | Why |
|-------|-------|-----|
| **Code + schema + seed** | Git (`oddhobbies`, `suppliers`) | Diffs, history, every VPS pulls same protocol |
| **Canonical product/supplier DB** | **One primary host** (this box or a small VPS) | SQLite needs single writer |
| **DB replica / read** | Other VPSs via **HTTP API** or read-only copy | Don’t multi-write SQLite |
| **Images / STLs / listings assets** | **Cloudflare R2** | Global CDN, S3 API, cheap egress, public URLs for Etsy/Pinterest/Shopify |
| **Secrets** | agent-vault (already) | Never in git or on every VPS as plaintext forever |
| **Consumer MCP / ops MCP** | Run next to DB primary; expose via tunnel or API | Tools query one DB |

**Don’t:** sync SQLite file over rsync between VPSs as the primary workflow (race conditions, corruption).  
**Do:** one writer + R2 assets + git protocol + optional API for other boxes.

---

## Recommended layout

```
┌─────────────────┐     git pull      ┌─────────────────┐
│  VPS A (this)   │◄──────────────────│  VPS B / C      │
│  PRIMARY        │                   │  workers        │
│  oddhobbies.db  │                   │  read API /     │
│  MCP servers    │                   │  render jobs    │
│  seed.py        │                   │  no SQLite write│
└────────┬────────┘                   └────────┬────────┘
         │ R2 put (assets)                     │ R2 get
         │ API (optional reads)                │
         ▼                                     ▼
┌─────────────────────────────────────────────────────┐
│  Cloudflare R2 bucket (e.g. oddhobbies-assets)     │
│  etsy/…  products/…  stl/…  pins/…  shopify/…      │
└─────────────────────────────────────────────────────┘
         │ public/custom domain URL (optional CDN)
         ▼
   Etsy · Pinterest · Shopify · ChatGPT MCP
```

### Roles

| VPS | Job |
|-----|-----|
| **Primary** | `oddhobbies.db`, ops MCP, consumer MCP, seed, Etsy API writes |
| **Render VPS** | Mockups, STL prep, image variants → upload R2 → notify primary |
| **Optional edge** | Shopify storefront, public site — pull assets from R2 only |

---

## Cloudflare: what to use

### R2 — **yes, do this**
| Use | Detail |
|-----|--------|
| Bucket | `oddhobbies-assets` (or `pogpet-assets`) |
| Layout | `products/<sku>/hero.jpg`, `etsy/<listing_id>/`, `stl/<sku>/`, `pins/<sku>/` |
| Access | S3 API via vault keys (`CLOUDFLARE_R2_*`) |
| Public URL | R2.dev or custom domain → for Pinterest/Shopify/Etsy upload source |
| Cost | Storage pennies; **egress free** (unlike S3) |

Vault already has: `CLOUDFLARE_ACCOUNT_ID`, `R2_BUCKET`, `CLOUDFLARE_R2_*`, `R2_S3_*`.

### Cloudflare — **not required for the DB**
| Product | Use? | Notes |
|---------|------|-------|
| R2 | ✅ assets | Primary CF win |
| Workers | optional | Thin API: “get product json for agent” |
| D1 (SQLite on CF) | ⚠️ later maybe | Nice for **public catalog**, not for ops writes + MCP + Etsy tools |
| Pages/Workers Sites | optional | Marketing / Pinterest landing |
| Tunnel | ✅ if MCP remote | Expose local MCP without opening SSH on every box |

**Verdict:** Use **R2 now**. Keep **SQLite on one VPS** until multi-writer pain is real. If consumer catalog needs global read later, **mirror** products into D1/R2 JSON — don’t move the ops DB first.

---

## How to edit across VPSs (workflow)

### 1. Code / docs / schema
```bash
# every VPS
git pull origin main
python3 db/seed.py   # only on primary, or read-only clone on others
```

### 2. DB edits
| Edit type | Where | How |
|-----------|-------|-----|
| Costs, quotes, decisions | **Primary only** | MCP `db_sql` / seed / small CLI |
| Product metadata | Primary | `products` table |
| Never | Other VPS | Direct SQLite file writes |

If VPS B needs a write: **HTTP to primary** (`POST /internal/products/...`) or open PR in git for seed JSON then primary reseeds.

### 3. Asset edits
```
VPS B renders mockup
  → aws s3 cp / rclone to R2 products/XMAS-3D-TILE-RACK/hero.jpg
  → INSERT assets row on primary (API or git JSON + seed)
  → Primary uploads to Etsy when ready
```

Canonical rule: **file lives in R2; DB stores path/URL; git stores schema/seed.**

### 4. Secrets
```
agent-vault get on the box that needs the call
→ never commit tokens
→ Etsy write only on primary
```

---

## Sync options (pick one)

| Option | Complexity | Best for |
|--------|------------|----------|
| **A. Git + R2 + single DB writer** (recommended) | Low | Now, 2–5 VPSs |
| B. Primary HTTP API + Workers/D1 catalog mirror | Medium | Public agent catalog at scale |
| C. Litestream / turso replica of SQLite | Medium | Read replicas of ops DB |
| D. Postgres on primary + pgbouncer | Higher | Multi-writer product ops later |

**Start with A.** Move to B when ChatGPT plugin needs 99.9% read without your VPS.

---

## R2 bucket layout (proposed)

```
oddhobbies-assets/
  products/
    XMAS-3D-TILE-RACK/
      hero.jpg
      lifestyle.jpg
      pin-1080x1920.jpg
      shopify-2048.jpg
      stl/tile-rack-v1.3mf
    XMAS-3D-ORNAMENT/
      hero.jpg
      ...
  etsy/
    4584650499/   # brick figure photos (already on disk)
    4584658252/
  pins/
    christmas/
    game-night/
    weddings/
  albums/
    memory-album/cover-mock.png
```

DB `assets.path_or_url` becomes:
`r2://oddhobbies-assets/products/XMAS-3D-TILE-RACK/hero.jpg`  
or CDN URL `https://pub-xxx.r2.dev/...`

---

## Day-1 plan (concrete)

1. **Create R2 bucket** + lifecycle (optional: delete old drafts)  
2. **Upload** `oddhobbies/assets/etsy/**` + `local/**` to R2 under layout above  
3. **Update** `assets` rows: `storage='r2'`, `path_or_url=r2://...`  
4. **Keep** `oddhobbies.db` on this VPS as primary  
5. **Git ignore** large binaries; store paths in DB/JSON  
6. **Optional:** Cloudflare Tunnel for consumer MCP later  
7. **Optional:** tiny `GET /products.json` on primary for Shopify/Pinterest scripts  

---

## What not to do

- Don’t put the **ops SQLite** on R2/D1 as the working file  
- Don’t rsync `.db` between VPSs as the main edit loop  
- Don’t store Etsy/Prodigi/API keys in the DB  
- Don’t treat Etsy CDN URLs as canonical (they can break; we already mirrored)  
- Don’t design 200 mm Meshy dogs as core SKUs — stick to **80 mm pet / 75 mm brick** for farm cost bands  

---

## Fit with your product doctrine

| SKU family | Asset needs | Fulfilment |
|------------|-------------|------------|
| Chibi pets 60/80/120 mm | hero, lifestyle, size chart, pin | Makr3D / Printie / 3DV |
| Bricks 75 mm + ornament 70 mm | before/after photo, lifestyle Xmas | same + loop spec |
| Game Night 3D | table context, engraving close-up | Makr3D / Printie |
| Albums | cover mock, tracklist graphic | Kunaki/DiskCr + Prodigi book |

R2 holds all of that per SKU; DB links product ↔ assets ↔ listings ↔ suppliers.

---

## Decision

| Question | Answer |
|----------|--------|
| Cloudflare? | **Yes for R2 assets.** Not for ops SQLite yet. |
| Multi-VPS editing? | **Git (code) + R2 (files) + one DB writer (primary).** |
| Best next action? | Upload existing assets to R2; point `assets` table at R2 paths. |

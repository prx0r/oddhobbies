# Product + Supplier Database

> Canonical store for costs, specs, materials, shipping, lead times.  
> Machine file: **`data/product-supplier-db.json`**  
> Sources: `/root/suppliers`, `bwick/docs/prodigi/*`, live Prodigi API, web research 2026-10-01.

---

## Schema (what we track)

| Field | Meaning |
|-------|---------|
| `sku` | Internal product code |
| `listing_id` | Etsy draft/active ID |
| `section` | Game Night / Weddings & Couples / Stocking |
| `price_usd` | Retail |
| `supplier_primary` / `supplier_alt*` | Fulfilment path(s) |
| `make` | `3d_print` \| `flat_print` \| `custom_audio` \| … |
| `material` | PLA, metal, paper, ceramic, … |
| `dimensions` | size class + mm where known |
| `unit_cost` | per-unit fulfilment (not design time) |
| `shipping.hub` | Where it ships from |
| `shipping.cost_to_user` | Free listing / bundled / Q |
| `lead_time.*_total_days` | production + transit by region |
| `demand_evidence` | Why we believe it sells |
| `files_needed` | STL / art / SOP still missing |
| `status` | draft_live \| needs_quote \| needs_stl \| … |

---

## Supplier directory (specifics)

### 3D print

| ID | Location | Etsy | MOQ | Fee | White-label | Dispatch | Shipper of record | Notes |
|----|----------|------|-----|-----|-------------|----------|-------------------|-------|
| **MAKR3D** | Huddersfield **UK** | ✅ native | 1 | £0 | ✅ | 1–2 days | ✅ | Bambu farm; instant slicer quotes; API+webhooks |
| **PRINTIE** | **US** | ✅ | 1 | $0 | ✅ packaging | Q | Q | Flat fee **includes shipping**; best US pick |
| **3D_VIKINGS** | Riga **Latvia** | ✅ | 1 | €0 | ✅ | 1–3 days prod | Q | Instant quote + ship/tax; **not US** |
| **EDYN_LABS** | US-oriented | Etsy focus | quote | Q | planned | Q | Q | Quote review before production |

**Makr3D cost tiers (ex-VAT GBP → USD est.)**

| Class | GBP | USD est. |
|-------|-----|----------|
| Small desk toy | £1.29 | ~$1.75 |
| Medium fidget | £2.50 | ~$3.37 |
| Large articulated | £7.60 | ~$10.30 |

*Always get per-file quote — magnets/engraving/multi-part change cost.*

**Lead times (Makr3D → user)**

| Destination | Production | Transit | Total est. | Customs |
|-------------|------------|---------|------------|---------|
| UK | 1–2d | 1–3d | **2–5d** | n/a |
| EU | 1–2d | 3–7d | **4–9d** | check UK-origin |
| US | 1–2d | 5–14d | **6–16d** | buyer may pay |
| AU | 1–2d | 7–14d | **8–16d** | possible |

**Lead times (Printie → US)** — target domestic; confirm after account.

---

### Flat print / cards / albums

| ID | Location | Key SKUs / products | Cost anchors | Lead (prod+ship) |
|----|----------|---------------------|--------------|------------------|
| **PRODIGI** | UK/US/EU/AU labs | pet tags, bandanas, postcards, stickers, wrap, jigsaw, photo book, calendar, notebooks, coasters, decks (pin) | Postcard £0.40; pet tag ~£5+£4.30 ship; stickers from £0.80; wrap from £3 | UK 2–5d · US 3–7d · EU 3–8d · AU 5–12d |
| **PRINTFUL** | US/EU/MX/JP | apparel, mugs, calendars | Tee ~$10+$4–5 ship | 6–13d US |
| **PRINTSEEKERS** | EU | wall art, framed | Q | ~3–9d |
| **GELATO** | 30+ countries local | prints, mugs, books | Q | 2–5d local |

**Prodigi API-verified live (2026-10-01)**

| SKU | What | Cost |
|-----|------|------|
| `PET-MET-BONE` | Bone metal tag 2.8×3.8cm | ~£11.16 all-in (quote) |
| `PET-MET-ROUND` | Round metal tag 3.2×3.9cm | ~£11.16 all-in |
| `PET-BANDANA-*` | Bandanas S/M/L | ~£12.36–13.56 all-in |
| `CLASSIC-POST-GLOS-6X4` | Postcard 6×4 | £0.40 wholesale |

**Still pin in Prodigi dashboard (Q):** greeting card (old `GLOBAL-CFGA-5X7` **EntityNotFound**), stickers `STICK*`, wrap `WRAP*`, jigsaw, photo book, calendar, coasters, notebook, playing cards.

---

### Physical media (albums)

| ID | Location | Cost | Lead | White-label |
|----|----------|------|------|-------------|
| **KUNAKI** | Sparks **NV USA** | CD jewel **$2.00**; vinyl 12" display **$11**; playable vinyl **$36–50** | US 4–8d total · intl 8–22d | ❌ own return address; no custom inserts |
| **DISKCR** | Manchester **UK** | Jewel from **£7.99**; digipak etc. | UK Q · intl +3–10d | ✅ they handle support/refunds |
| **WALRUS** | global | revenue split; cassette yes | 2–4 business days | ✅ |
| **ELASTICSTAGE** | UK | premium vinyl | Q | ✅ |

---

### Card decks (Top Trumps / playing cards)

| ID | Location | Cost | Notes |
|----|----------|------|-------|
| **PRODIGI** | multi | Q | Pin playing-card SKU first |
| **PERSONALISED_PLAYING_CARDS_UK** | Cambs UK | Trumps 40 from **£12.99** | Same-day if by 11am; no MOQ |
| **MAKE_PLAYING_CARDS** | global POD | quote | API/CSV; tuck+foil |
| **MYTRADINGCARDS** | Fremont CA | $5.50 single → $0.70@300+ | Manual only; bulk runs |

---

## Product rows (seed)

### Game Night — 3D print (MAKR3D / PRINTIE)

| SKU | Listing | Retail | Est cost UK | UK total | US total | Material | Personalisation |
|-----|---------|--------|-------------|----------|----------|----------|-----------------|
| Line Reader | 4586657665 | $11.99 | ~$1.75 | 2–5d | 6–16d | PLA+ | name, colour |
| First Player | 4586658541 | $8.99 | ~$1.75 | 2–5d | 6–16d | PLA | motif, name |
| Cribbage Pegs | 4586671942 | $14.99 | ~$1.75–3.37 | 2–5d | 6–16d | PLA+ | name, year |
| Tile Rack | 4586662106 | $12.99 | ~$3.37 | 2–5d | 6–16d | PLA+ | name, magnet base |
| Wind Markers | 4586671970 | $16.99 | ~$3.37 | 2–5d | 6–16d | PLA | tray name |
| Ornament | 4586658575 | $14.99 | ~$1.75 | 2–5d | 6–16d | PLA | photo→character |
| Token Tray | 4586661282 | $22.99 | ~$3.37–10.30 | 2–5d | 6–16d | PLA++magnets | name, colours |
| Cribbage Board | 4586671960 | $29.99 | ~$10.30 | 2–5d | 6–16d | PLA+ | family name |

*Tile rack inventory locked: qty 50 @ $12.99. Volume tiers 2/4/6 in listing copy.*

### Weddings & Couples

| SKU | Listing | Retail | Supplier | Cost basis | UK total | US total |
|-----|---------|--------|----------|------------|----------|----------|
| Memory Album | 4586678882 | $34.99 | Kunaki/DiskCr | CD $2 / £8 + production time | intl risk | 4–8d + prod |
| Wedding Video Album | 4586678898 | $59.99 | Kunaki+Prodigi | CD + edit + optional book | Q | Q |
| Playing Cards | 4586691388 | $22.99 | Prodigi/MPC/UK | deck Q / £12.99+ | 3–8d | 5–14d |
| Top Trumps | 4586691360 | $24.99 | Prodigi/MPC/UK | deck Q | 3–8d | 5–14d |
| Metal Pet Tag | 4586691324 | $16.99 | Prodigi | ~$11.16–14.95 all-in | 2–5d | 3–7d |

### Game Night — Prodigi side

| SKU | Listing | Retail | Cost | Status |
|-----|---------|--------|------|--------|
| Notebook | 4586687823 | $16.99 | Q pin SKU | draft |
| Coaster Set | 4586691376 | $19.99 | Q pin SKU | draft |

### Add-ons (all Prodigi listings)

| Item | Retail | Usual | Wholesale |
|------|--------|-------|-----------|
| Sticker sheet | **$3.99 add-on** | $7.99 | from £0.80 |
| Postcard | **$2.99 add-on** | $3.99 | £0.40 |

Free shipping listing-wide; **free over $19.99 combined** (copy + dashboard guarantee).

---

## Shipping policy (ours)

| Setting | Value |
|---------|-------|
| Etsy profile | `316299492609` standard |
| Primary / secondary cost | $0 / $0 (free ship) |
| Destinations configured | all, GB, US |
| Combined free threshold | **$19.99** |
| Enforcement | listing copy now; **Shop Manager free-shipping guarantee** for basket rule |

---

## Open quotes (blockers)

1. **P0** Printie all-in quotes — 8 STLs, US ZIP  
2. **P0** Makr3D exact per-file quotes — same 8 STLs  
3. **P0** Prodigi dashboard pin + wholesale for card/stickers/wrap/jigsaw/book/calendar/coaster/notebook/deck  
4. **P1** Pet tag US/UK quote confirm  
5. **P1** UK playing-card deck quote (Top Trumps)  
6. **P1** Kunaki sample CD + ship times  
7. **P1** Magnet hardware if trays need bought-in magnets  

---

## How to update this DB

1. New quote → edit `data/product-supplier-db.json` under `suppliers` + product `unit_cost` / `lead_time`  
2. New SKU pin → `suppliers.PRODIGI.docs_only_skus_pin_in_dashboard`  
3. New listing → append to `products[]` with `listing_id`  
4. Re-export this markdown table when JSON changes (manual for now)  

Related docs:
- `shop/US-3D-SUPPLIER.md` — Printie vs Makr3D vs Vikings  
- `shop/FLAGSHIP-COSTS.md` — margins + sections  
- `shop/PRODIGI-XMAS-OPS.md` — add-ons + pins  
- `shop/XMAS-FLAGSHIP-15.md` — earlier 15 (focus superseded)  

# Xmas Flagship 16 — Final Pack

> Shop: **PogPet** `67863887`  
> Date: 2026-10-01  
> Principle: **easy to make × demand-proven × great Xmas gift**  
> Machine-readable: `xmas-drafts-2026-10-01.json`

---

## Supplier tracks (internal)

| Track | Supplier | What it can actually make |
|-------|----------|---------------------------|
| **MAKR3D** | Makr3D (Huddersfield UK) | 3D print: racks, pegs, boards, stands, markers, ornaments |
| **PRODIGI** | Prodigi (UK/US/EU/AU) | Flat print: cards, stickers, wrapping, jigsaws, wall art, notebooks |
| **KUNAKI** | Kunaki (Sparks NV) | Physical media: CDs (jewel case ~$2), vinyl display/collectible |

### Prodigi capability answer (important)

**Prodigi does NOT sell custom Scrabble boards or custom Rummikub boards.**

Verified against our Prodigi docs (`/root/suppliers/suppliers/flat-print/`, `bwick/docs/prodigi-catalogue.md`, Prodigi API):

| Prodigi HAS | Prodigi does NOT have |
|-------------|----------------------|
| Greeting cards, postcards | Custom board games |
| Kiss-cut stickers | Scrabble / Rummikub boards |
| Wrapping paper | 3D printed game accessories |
| Jigsaw puzzles (multi print area incl. lid) | Vinyl manufacturing |
| Wall art / photo tiles / framed prints | Cribbage boards |
| Calendars, notebooks | Tile racks / pegs |

→ Custom Scrabble/Rummikub **boards** were overreach. Kill them.  
→ Custom **tile racks** (word-game racks) stay — those are Makr3D 3D prints, not Prodigi boards.

---

## Flagship 16

### MAKR3D (11) — 3D print, easy + proven

| # | SKU | Listing ID | Price | Demand / why flagship |
|---|-----|------------|-------|------------------------|
| 1 | Tile Rack (single, volume 1–6) | **4586662106** | $12.99 | Scrabble racks stuck in the 1970s. List as **1**; tiers: 2@$11.99, 4@$10.99, 6@$9.99 |
| 2 | Mahjong Line Reader | **4586657665** | $11.99 | **17k+ proven** on Etsy. $0.50 print. Highest-confidence SKU |
| 3 | Mahjong Wind Markers | **4586671970** | $16.99 | Accessory gap beyond line readers. Mahjong racks +228% on Etsy |
| 4 | Magnetic Token Tray | **4586661282** | $22.99 | **8.7k proven**. Magnetic = premium feel |
| 5 | First-Player Token | **4586658541** | $8.99 | Easy stocking stuffer. Dragon / Xmas motifs |
| 6 | Cribbage Pegs (personalised) | **4586671942** | $14.99 | **Flagship niche** — cribbage underserved, high willingness to pay |
| 7 | Travel Cribbage Board | **4586671960** | $29.99 | Flagship pair with pegs. Compact + magnetic peg seats |
| 8 | Figure Display Stand | **4586671984** | $9.99 | Proven pattern (4k+ review demand). Easy print, stocking stuffer |
| 9 | Vinyl / Album Display Stand | **4586671992** | $24.99 | Vinyl collection display **+28%**. Pairs with OddHobb Records |
| 10 | Christmas Ornament | **4586658575** | $14.99 | Classic Xmas. Photo→character option like brick figure |
| 11 | Christmas Dice Tower | **4586658561** | $24.99 | Tabletop flagship. Wizard/Xmas motifs, felt tray |

### PRODIGI (4) — flat print, fast + high margin

| # | SKU | Listing ID | Price | Why |
|---|-----|------------|-------|-----|
| 12 | Custom Christmas Greeting Card | **4586662046** | $5.99 | Hero volume SKU. Brick-style pet art |
| 13 | Personalised Wrapping Paper | **4586662062** | $12.99 | Seasonal spike. Repeating character pattern |
| 14 | Christmas Sticker Sheet | **4586658501** | $7.99 | Review-engine fuel. Highest margin % |
| 15 | Custom Jigsaw Puzzle | **4586657625** | $19.99 | Weekend-activity gift. Prodigi multi-area (lid art) |

### KUNAKI (1) — physical media

| # | SKU | Listing ID | Price | Why |
|---|-----|------------|-------|-----|
| 16 | Sleepy Cribbage Club Album CD | **4586671998** | $14.99 | **Album line locked in.** OHB-002. CD cost ~$2 → ~$12 margin. Order early (intl transit) |

---

## Tile Rack volume model (updated)

| Qty | Unit price | Rationale |
|-----|------------|-----------|
| 1 | $12.99 | Single-rack impulse / gift |
| 2 | $11.99 | Pair for two players |
| 4 | $10.99 | Full table set |
| 6 | $9.99 | Club / wedding / house gift |

- Listing sold as **1 unit** (qty available = 50)
- Tier price confirmed at checkout / message before print (customisable listing)
- Inventory offering locked at **$12.99 / qty 50** (`readiness_state_id=1518572416146`)

---

## Killed / deprioritised

| SKU | Listing ID | Why killed |
|-----|------------|------------|
| Custom Scrabble Board | 4586662026 | **Prodigi cannot print custom game boards.** Renamed `ZZ KILLED` — delete in dashboard |
| Custom Rummikub Board | 4586662030 | Same. Overreach |
| Chess Piece Holder | 4586657693 | Confusing SKU, not flagship. Renamed killed |
| Catan Resource Tower | 4586657705 | Not demand-proven, not easy enough for flagship 16 |
| D&D Initiative Tracker | 4586657725 | Complex build; deprioritise until pegs/racks prove the 3D line |

Etsy token lacks `listings_d` — kills were **renamed to `ZZ KILLED …`**. Manually delete in Shop Manager.

---

## Why this set wins Christmas

1. **Validate demand first** — line reader 17k, token trays 8.7k, figure stands 4k+, mahjong racks +228%
2. **Easy to make** — single-material PLA, small-medium prints; flat print needs only art
3. **Great gifts** — personalisation on almost everything; stocking fillers ($8–15) + step-ups ($22–30)
4. **Album line** — Kunaki CD + vinyl display stand = physical media gift story
5. **Cribbage flagship** — underserved niche, older/wealthier buyers, perfect for engraved pegs + travel board
6. **No IP landmines** — no Scrabble/Rummikub/Catan/LEGO marks; "fits tiles up to 15mm" language

---

## Still blocking go-live

| # | Action | Surface |
|---|--------|---------|
| 1 | Production partners: **Makr3D + Prodigi + Kunaki** | Etsy dashboard (no API create) |
| 2 | Shop sections + assign | Dashboard (`shops_w` missing on token) |
| 3 | Delete `ZZ KILLED …` drafts | Dashboard (`listings_d` missing) |
| 4 | Images (10-slot formula) | Dashboard or `uploadListingImage` |
| 5 | Confirm Prodigi jigsaw/card SKUs + wholesale | Prodigi dashboard |
| 6 | Kunaki sample order (OHB-002) before live | Kunaki account |
| 7 | Activate drafts after images + partners | PATCH `state=active` |

---

## Cost / margin anchors

| Supplier | Product | Cost est. | Retail | Margin |
|----------|---------|-----------|--------|--------|
| Makr3D | Small (pegs, first player, stand) | ~$1.75 | $8.99–$14.99 | 73–88% |
| Makr3D | Mid (line reader, rack, winds) | ~$3.37 | $11.99–$16.99 | 66–80% |
| Makr3D | Large (board, tower, dice, vinyl) | ~$10.30 | $22.99–$29.99 | 55–65% |
| Prodigi | Card | ~$1.90 | $5.99 | ~$1.59 |
| Prodigi | Stickers | ~$1.00 | $7.99 | ~$4.99 |
| Prodigi | Wrapping | ~$3.80 | $12.99 | ~$5.69 |
| Prodigi | Jigsaw | Q | $19.99 | Q |
| Kunaki | CD jewel case | ~$2.00 | $14.99 | ~$12.99 |

---

## Next session priority

1. Dashboard: kill 5 renamed drafts, add production partners, create sections  
2. Makr3D: upload STLs for tile rack, line reader, winds, pegs, cribbage board, stand, vinyl stage, ornament  
3. Prodigi: sample pack + pin jigsaw/card SKUs  
4. Kunaki: sample OHB-002 CD  
5. Photos → activate top 6 first (line reader, tile rack, token tray, first player, card, pegs)

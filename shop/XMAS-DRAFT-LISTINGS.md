# Xmas GEM Draft Listings — 2026-10-01

> Shop: **PogPet** (`67863887`) — https://www.etsy.com/shop/pogpet  
> Status: **15 drafts created via Etsy API** (state=`draft`, no images yet)  
> Machine-readable: `xmas-drafts-2026-10-01.json`

---

## Supplier split (internal)

| Track | Supplier | Fulfilment | Listings |
|-------|----------|------------|----------|
| **PRODIGI** | Prodigi (UK/US/EU/AU) | Flat print + personalise | 6 |
| **MAKR3D** | Makr3D (Huddersfield UK) | 3D print | 9 |

Etsy production partners **cannot** be created via Open API. Add both in dashboard:

1. Etsy → Shop Manager → Settings → **Production partners**
2. **Makr3D** — location `Huddersfield, UK` — https://makr3d.app — covers all `XMAS-3D-*`
3. **Prodigi** — location `UK / US / EU / AU` — https://prodigi.com — covers all `XMAS-PROD-*`
4. Then PATCH each listing to attach `production_partner_ids`

Shop sections (`Christmas 3D Print`, `Christmas Flat Print`) need `shops_w` scope — current token is listings-only. Create manually in dashboard, then assign.

---

## Shop constants

| Field | Value |
|-------|-------|
| shop_id | 67863887 |
| shipping_profile_id | 316299492609 |
| readiness_state_id | 1518572416146 (`made_to_order`) |
| who_made | `collective` (production-partner friendly) |
| when_made | `made_to_order` |
| tags rule | each tag **≤20 characters** |

---

## PRODIGI (6) — flat print / personalise

| SKU | Listing ID | Tax | Price | Title |
|-----|------------|-----|-------|-------|
| XMAS-PROD-SCRABBLE-BOARD | **4586662026** | 1554 Board Games | $34.99 | Custom Scrabble Board \| Personalised Family Game Night \| Christmas Gift \| Custom Board Game Mat \| Family Name Gift |
| XMAS-PROD-RUMMIKUB-BOARD | **4586662030** | 2352 Tile Games | $34.99 | Custom Rummikub Board \| Personalised Tile Game Mat \| Family Christmas Gift \| Rummikub Lover Gift \| Custom Game Board |
| XMAS-PROD-GREETING-CARD | **4586662046** | 1273 Christmas Cards | $5.99 | Custom Christmas Greeting Card \| Personalised Pet Portrait Card \| Christmas Card From Dog \| Cat Christmas Card \| Photo Card |
| XMAS-PROD-WRAPPING | **4586662062** | 6604 Gift Wrap | $12.99 | Personalised Wrapping Paper \| Custom Christmas Gift Wrap \| Pet Pattern Wrap \| Brick Figure Pattern \| Christmas Stocking Stuffer |
| XMAS-PROD-STICKERS | **4586658501** | 1326 Stickers | $7.99 | Christmas Sticker Sheet \| Custom Pet Stickers \| Personalised Gift Tags Stickers \| Brick Style \| Stocking Stuffer \| Party Favour |
| XMAS-PROD-PUZZLE | **4586657625** | 2353 Jigsaw Puzzles | $19.99 | Custom Jigsaw Puzzle \| Personalised Christmas Puzzle \| Family Photo Puzzle \| Pet Portrait Puzzle \| Christmas Gift \| Brick Figure Puzzle |

**Prodigi cost anchors (from bwick docs, ✓ verified 2026-09-30):**

| Product | Wholesale | Retail | Gross |
|---------|-----------|--------|-------|
| Greeting card 5x7 | ~$1.90 | $5.99 | ~$1.59 |
| Wrapping sheet | ~$3.80 | $12.99 | ~$5.69 |
| Sticker sheet | ~$1.00 | $7.99 | ~$4.99 |
| Postcard 6x4 | ~$0.50 | $3.99 | ~$0.99 |

Scrub board / Rummikub board / jigsaw — Q: confirm exact Prodigi SKU + wholesale before go-live (large-format print + puzzle SKU).

---

## MAKR3D (9) — 3D print

| SKU | Listing ID | Tax | Price | Title |
|-----|------------|-----|-------|-------|
| XMAS-3D-TILE-RACK-4 | **4586662106** | 1554 Board Games | $39.99 | Personalised Tile Rack 4 Pack \| Modern Scrabble Style Rack \| Christmas Game Night Gift \| Family Name Engraved \| Board Game Accessory |
| XMAS-3D-TOKEN-TRAY | **4586661282** | 2151 Game Pieces | $22.99 | Magnetic Token Tray Set Christmas \| Board Game Organizer \| Hex Token Holder \| Personalised Game Night Gift \| Catan Accessory |
| XMAS-3D-FIRST-PLAYER | **4586658541** | 2151 Game Pieces | $8.99 | Christmas First Player Token \| Dragon Egg Token \| Personalised Board Game Token \| Game Night Gift \| Stocking Stuffer \| Board Game Accessory |
| XMAS-3D-MAHJONG-READER | **4586657665** | 2387 Mahjong | $11.99 | Personalised Mahjong Line Reader \| Mahjong Gift \| Custom Tile Guide \| Christmas Mahjong Accessory \| Mahjong Player Gift |
| XMAS-3D-DICE-TOWER | **4586658561** | 1552 Toys & Games | $24.99 | Christmas Dice Tower \| Wizard Dice Tower \| Personalised D&D Gift \| Dungeon Master Christmas Gift \| Tabletop Accessory \| Dice Tower |
| XMAS-3D-CHESS-HOLDER | **4586657693** | 2389 Chess | $18.99 | Chess Piece Holder \| Captured Pieces Tray \| Personalised Chess Accessory \| Christmas Chess Gift \| Board Game Gift \| Chess Set Add-On |
| XMAS-3D-RESOURCE-TOWER | **4586657705** | 1554 Board Games | $24.99 | Catan Resource Tower \| Board Game Organizer \| Personalised Resource Holder \| Christmas Game Night Gift \| Family Board Game Gift |
| XMAS-3D-INITIATIVE | **4586657725** | 1552 Toys & Games | $29.99 | D&D Initiative Tracker \| Dice Tower Combo \| Dungeon Master Gift \| Christmas RPG Gift \| Personalised Campaign Tracker \| Tabletop |
| XMAS-3D-ORNAMENT | **4586658575** | 1857 Ornaments | $14.99 | Custom Christmas Ornament \| Personalised Pet Ornament \| 3D Printed Bauble \| Family Name Ornament \| Christmas Gift \| Stocking Stuffer |

**Makr3D cost anchors (EX-VAT, from oddhobbies SUPPLIERS.md):**

| Size class | Fulfilment | Our prices | Margin |
|------------|------------|------------|--------|
| Small desk toy | £1.29 (~$1.75) | $8.99–$14.99 | 73–88% |
| Fidget / mid | £2.50 (~$3.37) | $11.99–$22.99 | 69–84% |
| Large articulated | £7.60 (~$10.30) | $24.99–$39.99 | 58–74% |

---

## Copy formula (same as brick-figure drafts)

**Title:** keyword-first, occasion stack at back, ~140 chars, no brand marks (no "Scrabble®", "Rummikub®", "LEGO®", "Catan®", "MTG").

**Description pattern:**
1. Hook (1–2 lines)
2. HOW IT WORKS (order → personalise → preview → ship)
3. WHAT YOU GET (bullets)
4. IP line: *"Original design — not affiliated with any game brand. Fits tiles up to 15mm."*
5. Supplier + dispatch (UK printed / 3D printed via Makr3D)
6. Free shipping claim where applicable

**Photos (upload before activate):**
1. Hero on dark wood / table context
2. Personalised variant (name visible)
3. In-use / hand for scale
4. Detail close-up (engraving / print quality)
5. Packaging
6. Size diagram
7. Lifestyle game-night scene
8. Christmas occasion shot
9. Variant swatches
10. Bundle upsell (tile rack + token tray, etc.)

---

## What still blocks go-live

| # | Action | Owner surface |
|---|--------|---------------|
| 1 | Create production partners Makr3D + Prodigi | Etsy dashboard |
| 2 | Create shop sections + assign to drafts | Etsy dashboard (needs `shops_w` token) |
| 3 | Confirm Prodigi SKUs for board/jigsaw (Q) | Prodigi dashboard / quote API |
| 4 | Upload listing photos (10-slot formula) | Dashboard or `uploadListingImage` |
| 5 | Attach production partners to listings | PATCH `production_partner_ids` |
| 6 | Delete old PogPet test/pet drafts if superseded | Dashboard |
| 7 | Activate drafts once images + partners set | PATCH `state=active` |

---

## Notes / gotchas learned

- Access tokens expire in ~1h — refresh with client_id + refresh token
- Physical listings **require** `readiness_state_id`
- Etsy tags **max 20 characters** each
- `who_made=collective` + production partners is the clean dropship path
- Taxonomy IDs used: 1554 board games, 2352 tile games, 2387 mahjong, 2389 chess, 2151 game pieces, 2353 jigsaw, 1273 xmas cards, 6604 gift wrap, 1326 stickers, 1857 ornaments, 1552 toys

# Standardised listing image prompts (ChatGPT)

> Copy a **base template** + paste the **product block** → ChatGPT generates listing images.  
> Prompts inherit **real supplier materials + sizes** from our DB so images stay true to product.  
> Brand look: cream studio · soft light · Christmas bokeh · warm gift energy · brick/LEGO-style characters where relevant · never brand names (no LEGO®, Scrabble®).

---

## How to use (hand this to ChatGPT)

```
You are generating Etsy listing photos for PogPet.
Follow the STYLE LOCK exactly.
Then use the PRODUCT SPEC block for the SKU I name.
Generate N images for the slots I list.
If material/size conflicts with style lock, follow PRODUCT SPEC.
```

**Slots (pick 1–10):**
1. hero · 2. lifestyle_person · 3. detail · 4. in_use · 5. scale_hand  
6. personalisation · 7. packaging · 8. variants · 9. bundle · 10. gift_moment

---

## STYLE LOCK (always)

```
Etsy product photography, commercial gift-brand look.
Background: warm cream (#F7F3EE) or soft white; optional Christmas tree bokeh, out of focus.
Lighting: soft key light, gentle shadows, warm fill, no harsh flash.
Props: minimal — cream fabric, light wood, subtle red/green accents only if Xmas.
People: natural skin tones, cosy knitwear, genuine smile, product clearly visible.
Framing: product centred or rule-of-thirds; plenty of clean negative space for text overlays.
Aspect ratios: 1:1 hero, 4:5 listing, 2:3 Pinterest.
NO text/watermarks/logos in image unless slot=personalisation mock.
NO brand-name toys visible (no LEGO® marks, no Scrabble® boards).
Style of figures if applicable: blocky brick-style characters, simple faces, visible studs,
smooth matte PLA plastic look — like a custom keepsake toy, not a copyrighted character.
```

---

## BASE TEMPLATES

### T1 — 3D print hobby gift (Makr3D / Printie)
```
Generate {N} Etsy listing images for a {PRODUCT_NAME}.
PRODUCT SPEC:
- Material: {MATERIAL} (matte plastic look if PLA/PLA+; metallic if metal tag)
- Size: {SIZE} (show scale with hand or game pieces)
- Colour: {COLOUR_NOTES}
- Personalisation: {PERSONALISATION}
- Supplier fulfilment: made to order, UK/US 3D print, white-label pack
SCENE:
- Hero on cream with soft bokeh
- Lifestyle: person using it at a board-game table or Christmas gift moment
- Detail: engraving/texture/magnet
- Scale: in hand next to game tiles/cards
- Packaging: kraft/cream gift pack, discreet brand card
Avoid: cluttered tables, brand-name game logos, neon colors.
```

### T2 — Brick figure / couple (brand target)
```
Generate {N} Etsy listing images for a custom {BRICK_TYPE}.
PRODUCT SPEC:
- Style: blocky brick-style character(s), stud top, simple happy face
- Base: {BASE} (black shared base for couple / display base for solo)
- Size: {SIZE}
- Look: matte PLA, gift keepsake
SCENE:
- Hero: figure(s) on cream, Christmas tree bokeh
- Lifestyle: real couple/person holding the figure, cosy knitwear, white tee OK
- Detail: face + studs + base
- Gift moment: under tree / on table with ribbon
Inspiration mood: bright studio like a premium personalised gift ad.
NO copyrighted character likeness — generic brick-style only.
```

### T3 — Ornament / keychain (small 3D)
```
Generate {N} Etsy listing images for a {PRODUCT_NAME}.
PRODUCT SPEC:
- Material: {MATERIAL}
- Size: {SIZE}
- Loop/keyring: {LOOP_SPEC}
- Personalisation: {PERSONALISATION}
SCENE:
- Hero hanging on Christmas tree OR on cream with ribbon
- In-hand scale
- Detail of loop/engraving
- Stocking-stuffer flat-lay with ribbon + kraft tag
Warm, festive, premium small-gift feel.
```

### T4 — Physical media / CD album
```
Generate {N} Etsy listing images for a personalised {ALBUM_TYPE}.
PRODUCT SPEC:
- Format: {FORMAT} (jewel case CD / digital download mock)
- Cover art theme: {COVER_THEME}
- Liner notes / track count: {TRACK_INFO}
- Mood: {MOOD} (cosy, romantic, nostalgic)
SCENE:
- Hero: jewel case + disc on cream, soft bokeh
- Lifestyle: person listening with coffee/headphones, warm light
- Detail: cover art + catalog number
- Digital: phone/laptop showing download UI mock
- Gift: ribbon + kraft sleeve, “for {OCCASION}”
NO real artist photos; original cover art only.
```

### T5 — Flat print (wrapping / stickers / card / tag)
```
Generate {N} Etsy listing images for {PRODUCT_NAME}.
PRODUCT SPEC:
- Format: {FORMAT} (sheet/roll/card/tag)
- Material: {MATERIAL} (paper, gloss, satin, metal tag)
- Design: {DESIGN} (brick-style pattern, names, holiday motifs)
- Size: {SIZE}
SCENE:
- Hero flat-lay on cream
- Wrapped gift / gift-tagged present
- Close-up print quality
- Bundle with main product (if slot=bundle)
Clean, giftable, premium paper goods.
```

---

## PRODUCT SPEC blocks (from supplier DB)

Use these verbatim in the template. Update when quotes change.

### 3D — MAKR3D / PRINTIE
| SKU | PRODUCT_NAME | MATERIAL | SIZE | COLOUR_NOTES | PERSONALISATION |
|-----|--------------|----------|------|--------------|-----------------|
| XMAS-3D-TILE-RACK | Personalised tile rack (word-game rack) | PLA+ plastic, optional magnetic base | ~200×30×25mm, holds 7 tiles | black, white, walnut, oak, custom | family name engraving |
| XMAS-3D-MAHJONG-READER | Mahjong line reader | PLA+ | ~80×30×5mm | 16 colours | player name |
| XMAS-3D-MAHJONG-WINDS | Mahjong wind markers + tray | PLA | marker set + tray | match mahjong set | tray name |
| XMAS-3D-FIRST-PLAYER | First-player token (dragon egg / Xmas) | PLA | palm-size token | festive + dragon motifs | player name optional |
| XMAS-3D-CRIBBAGE-PEGS | Cribbage pegs set | PLA+ | peg set for board | wood-tone / colour | name + year |
| XMAS-3D-CRIBBAGE-BOARD | Travel cribbage board | PLA+ | compact travel board, magnetic peg seats | natural / dark | family name / motto |
| XMAS-3D-TOKEN-TRAY | Magnetic hex token tray set | PLA+ + magnets | ~80mm hex, stackable | 16 colours | game/player name |
| XMAS-3D-ORNAMENT | Pet chibi Christmas ornament | PLA + hanging loop | ~70–80mm + loop (5mm hole / 2.4mm wire) | golden puppy, etc. | photo→character or name |
| KEYCHAIN-PET (add) | Pet keychain figurine | PLA | ~40–60mm + keyring | chibi pet | pet name |
| KEYCHAIN-BRICK (add) | Brick figure keychain | PLA | ~40–60mm + keyring | brick character | name |

**Fulfilment line for prompts:** made to order · 3D printed UK/US · matte PLA · white-label pack · 5–8 day dispatch  
**Never say:** LEGO, minifig trademark, “official”

### Physical media — KUNAKI / DISKCR
| SKU | PRODUCT_NAME | FORMAT | COVER_THEME | TRACK_INFO | MOOD |
|-----|--------------|--------|-------------|------------|------|
| ALBUM-MEMORY-CD | Personalised memory album | CD jewel case + digital download | custom: wedding photos / pet / travel collage | 4–10 original tracks, liner notes | cosy, romantic, nostalgic |
| ALBUM-WEDDING-VIDEO | Wedding video album | CD + optional photo book add-on | wedding stills, gold/cream | audio from wedding footage | romantic, keepsake |

**Size/format:** standard CD jewel case · full-colour disc · 2-panel insert  
**Fulfilment:** Kunaki US $2 CD / DiskCrafters UK · order early for Xmas

### Flat print — PRODIGI
| SKU | PRODUCT_NAME | FORMAT | MATERIAL | DESIGN | SIZE |
|-----|--------------|--------|----------|--------|------|
| PROD-PET-TAG-SET | Metal pet tag | tag | metallic metal | bone or round, engraved name+phone | bone 28×38mm / round 32×39mm |
| PROD-WRAPPING (re-add) | Christmas wrapping paper | sheet/roll | 95gsm satin | brick-style repeating pattern | 50×70 or 75×90cm sheets |
| PROD-STICKERS (re-add) | Kiss-cut sticker sheet | sheet | waterproof laminate | brick-style / holiday motifs | A5-ish sheet |
| PROD-POSTCARD | Custom postcard | card | 350gsm gloss | brick-style portrait | 6×4" |
| PROD-CARD | Greeting card | card | premium card stock | Xmas brick character | 5×7" |

---

## Ready-to-paste examples

### Example A — Tile rack (T1)
```
Generate 4 Etsy listing images using TEMPLATE T1.
PRODUCT SPEC:
- MATERIAL: PLA+ plastic, matte, optional magnetic base
- SIZE: ~200mm x 30mm x 25mm, holds 7 word-game tiles
- COLOUR: black base, walnut accent
- PERSONALISATION: family name "The Smiths" engraved on side
- Fulfilment: made to order 3D print UK/US
Slots: hero, lifestyle_person, detail_engraving, scale_hand
```

### Example B — Brick couple (T2)
```
Generate 4 Etsy listing images using TEMPLATE T2.
PRODUCT SPEC:
- BRICK_TYPE: couple figurine (two blocky brick-style people on shared black base)
- BASE: black shared display base
- SIZE: ~70–80mm tall figures
- Look: matte PLA keepsake, simple happy faces, studs on head
Slots: hero, lifestyle_person (couple holding product, knitwear, Xmas bokeh), detail_face, gift_moment
NO LEGO marks.
```

### Example C — Memory album CD (T4)
```
Generate 4 Etsy listing images using TEMPLATE T4.
PRODUCT SPEC:
- ALBUM_TYPE: personalised memory album CD
- FORMAT: jewel case + digital download
- COVER_THEME: cream + gold, abstract couple silhouette, winter florals
- TRACK_INFO: 8 tracks, liner notes, catalog OHB style
- MOOD: cosy anniversary gift
- OCCASION: 10th wedding anniversary
Slots: hero_case, lifestyle_listening, detail_cover, digital_mock
```

### Example D — Pet keychain (T3)
```
Generate 3 Etsy listing images using TEMPLATE T3.
PRODUCT SPEC:
- PRODUCT_NAME: pet keychain figurine
- MATERIAL: matte PLA
- SIZE: ~50mm figurine + metal keyring
- LOOP_SPEC: split ring keyring
- PERSONALISATION: pet name "Max"
Slots: hero, scale_hand, gift_flatlay
```

---

## Negative prompt (append to any)
```
ugly, cluttered, low quality, watermark, brand logo, LEGO text, Scrabble board text,
harsh shadows, neon, cluttered altar, dark horror, anatomical errors, extra fingers,
blurry product, text overlay (except personalisation mock), stock-photo cheese
```

---

## Prompt pack (10 standard jobs)

| # | Job | Template | Typical SKU |
|---|-----|----------|-------------|
| 1 | Hero product | T1/T2/T3/T4/T5 | any |
| 2 | Lifestyle person | T2/T1 | brick, rack, album |
| 3 | Detail / material | T1/T3 | engraving, PLA texture |
| 4 | Scale in hand | T1/T3 | token, pegs, keychain |
| 5 | In use (game/table) | T1 | rack, tray, cribbage |
| 6 | Personalisation mock | T1/T3 | name visible |
| 7 | Packaging | T1/T4/T5 | kraft + ribbon |
| 8 | Variants | T1/T3 | colours/motifs |
| 9 | Bundle flat-lay | T5/T1 | add-ons + main |
| 10 | Gift moment Xmas | T2/T3/T4 | under tree / listening |

---

## After ChatGPT returns images
1. Save to `oddhobbies/assets/generated/<SKU>/`  
2. `python3 oddhobbies/db/r2_upload.py`  
3. Insert `assets` rows with labels (`role`, `agent_blurb`, suitability)  
4. `assets_pick` → Etsy upload when ready  

---

## Supplier truth sources
- Makr3D tiers: £1.29 / £2.50 / £7.60 ex-VAT  
- Printie: US flat fee incl. shipping  
- Kunaki CD: **$2.00**  
- Prodigi pet tag: **~£11.16 all-in** (live quote)  
- DB: `oddhobbies/data/product-supplier-db.json` · MCP `db_get_product`  

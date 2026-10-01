# PogPet / OddHobbies — Etsy Store Design

> Brand target: **couples brick figurine** (photo → brick couple on shared base)  
> Look: warm white studio + Christmas bokeh + brick/LEGO-style characters + clean gift energy  
> Shop: PogPet `67863887` · https://www.etsy.com/shop/pogpet  
> Date: 2026-10-01

---

## Brand target (from your live couple listing)

| Signal | What we copy |
|--------|----------------|
| **Look** | Bright white/cream studio, soft light, Christmas tree bokeh |
| **Product** | Blocky brick figures (studs, simple faces), shared black base for couples |
| **People** | Young couple, cosy knitwear, genuine smile — *they* sell the gift |
| **Occasion** | Christmas first, then weddings/anniversaries |
| **Price feel** | Gift ($20–60), not novelty $5 junk |

**Brand line:** *Your people. In brick. For the ones who matter.*  
**Shop name on storefront:** PogPet (keep) · tagline: **Custom brick figures & hobby gifts**

---

## Store architecture

> **Christmas is not a section** — the whole brand is Xmas/gift energy. Do not add an Xmas section.
 (sections = buying occasions)

| # | Section | What lives there |
|---|---------|------------------|
| 1 | **Featured** | Brick couple, brick figure, Xmas ornament, memory album |
| 2 | **Couples & Weddings** | Couple figurine, wedding video album, playing cards, pet tags |
| 3 | ~~Christmas Gifts~~ | **REMOVED** — whole store is Christmas. Use Game Night / Couples / Physical Media |
| 4 | **Game Night** | Tile rack, mahjong, cribbage, token tray, Top Trumps |
| 5 | **Add-Ons** | Stickers $3.99, postcards $2.99 (too cheap alone) |

Dashboard: create these 5 sections, then assign each draft.

---

## Visual system

### Banner (Etsy shop banner 1200×300 or 3360×840)
```
LEFT:  brick couple on black base, tree bokeh behind
CENTER: "PogPet" in warm sans (Poppins/Inter)
         "Custom brick figures & hobby gifts"
RIGHT:  small brick pet figure + ornament
BG: cream #F7F3EE · accent gold/terracotta
```
Use couple lifestyle photo as banner crop.

### Shop icon
Single brick figure face on cream circle — same as listing hero style.

### Listing photo formula (same every SKU)
1. **Hero** — product on cream/white, soft shadow, Xmas bokeh optional  
2. **Lifestyle person** — human holding product (scale + emotion)  
3. **Detail** — engraving / face / texture  
4. **In use** — on tree / table / desk  
5. **Scale** — hand or coin  
6. **Personalisation mock** — name visible  
7. **Packaging**  
8. **Variants** — colours/motifs  
9. **Bundle** — add-ons  
10. **Gift moment** — Xmas morning / wedding table  

**Shot list per product:** `oddhobbies/shop/listing-photo-shots.md`

---

## Copy voice

| Do | Don’t |
|----|-------|
| “Your dog. As a brick figure.” | “LEGO-compatible custom minifig” |
| “Preview before we print” | “Magic AI toy” |
| “Original design” | Brand names (LEGO/Scrabble/Catan) |
| Free ship over $19.99 | Hidden fees |
| Couples / game night / Xmas | Generic “personalised gift” spam |

**Title pattern:**  
`{Product} | {What it is} | {Occasion} | {Benefit}` ≤140 chars  
**Tags:** 13, ≤20 chars, product-specific (already in channel payloads)

---

## Etsy Plus / growth kit (what’s worth it)

| Feature | Worth it? | Why |
|---------|-----------|-----|
| **Custom banner + branding** | ✅ now | Already designing |
| **About section + process story** | ✅ now | Brick figure origin + photo→preview→print |
| **Announcement bar** | ✅ now | “Free shipping over $19.99 · Order by Dec 10 for Xmas” |
| **Shop sections** | ✅ now | 5 sections above |
| **Personalisation on listings** | ✅ now | Questions in DB → Etsy |
| **Video on listings** | ✅ when assets ready | 15s photo→brick morph (bwick pipeline) |
| **Etsy Plus ($10/mo)** | ⚠️ after first sales | Custom domain, advanced marketing tools — not day-1 |
| **Offsite ads** | ⚠️ after reviews | Etsy drives traffic; costs ~12–15% — only amplify winners |
| **Star Seller** | ✅ process | Free ship + fast dispatch + preview-before-print |

**Day-1 free stack is enough:** sections + banner + about + policies + personalisation + consistent photos.

---

## Policies (pre-kill 1-stars)

| Policy | Setting |
|--------|---------|
| Processing | Made to order 5–8 days 3D · 2–5 days flat print |
| Christmas order-by | Publish in announcement + every listing |
| Shipping | Free (profile 316299492609) · free combined over $19.99 |
| Preview | “We send a preview before printing personalised items” |
| Returns | Custom/made-to-order — case-by-case; defects reprint |
| Materials | PLA (3D) · metal tags (Prodigi) · CD (Kunaki) |

---

## Launch order (images are the blocker)

### Ready when photos land
| Priority | SKU | Why first |
|----------|-----|-----------|
| 1 | Brick couple (live) | Brand hero |
| 2 | Xmas ornament | Has photos already |
| 3 | Tile rack | Easy STL, volume tiers |
| 4 | Mahjong line reader | 17k demand |
| 5 | First player token | Stocking filler |
| 6 | Cribbage pegs | Niche flagship |
| 7 | Memory album | Need SOP + cover art |
| 8 | Rest of Game Night | After proof of 3D line |

### In the meantime (no photos)
- [ ] Create 5 shop sections in dashboard  
- [ ] Upload banner from couple lifestyle crop  
- [ ] Write About: photo → preview → brick → doorstep  
- [ ] Set announcement: free ship $19.99 + Xmas dates  
- [ ] Attach personalisation questions from DB  
- [ ] Generate mockups for each draft (AI or product_previews style)  
- [ ] Fill `assets` + `assets_pick` for every SKU  

---

## Files
- This doc — store design  
- `listing-photo-shots.md` — per-SKU shot lists  
- `channel_payloads` in DB — title/tags/description ready  
- `ASSET-LABELS.md` — agent asset routing  

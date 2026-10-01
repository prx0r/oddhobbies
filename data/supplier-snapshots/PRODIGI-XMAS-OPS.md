# Prodigi Xmas Ops — Add-ons + Free Shipping + Gaming SKUs

> Shop: PogPet `67863887`  
> Date: 2026-10-01  
> Focus: **Xmas first** (weddings stay, but not the push)

---

## Answer: do people get married at Christmas?

**Yes.** Common pattern:
- Proposals Dec 24–25 (biggest engagement window of the year)
- Christmas-week / NYE weddings
- Anniversary season + “Christmas engagement” gift shopping

→ Keep **wedding video album** + **personalised playing cards** as evergreen.  
→ **Xmas is the demand spike** — lead with game gifts + pet gifts + albums.

---

## Prodigi: can we get “all of it” from them?

| Product | On Prodigi? | Live SKU / note |
|---------|-------------|-----------------|
| Metal pet tags | ✅ **Verified API** | `PET-MET-BONE`, `PET-MET-ROUND` |
| Dog bandanas | ✅ **Verified API** | `PET-BANDANA-SML` / `MED` / `LRG` |
| Postcards | ✅ Verified | `CLASSIC-POST-GLOS-6X4` |
| Stickers / tattoos | ✅ (docs) | `STICK*` prefix — pin in dashboard |
| Wrapping | ✅ (docs) | `WRAP*` prefix — pin in dashboard |
| Jigsaws | ✅ catalogue | Multi print area incl. lid — pin SKU |
| Photo books / calendars | ✅ catalogue | Pin SKU |
| Wooden coasters | ✅ catalogue | Pin SKU |
| Custom notebooks | ✅ catalogue | Pin SKU |
| Playing cards / Top Trumps | ⚠️ Partial | Catalogue lists playing cards; **exact deck SKU needs dashboard pin**. Fallback: PersonalisedPlayingCards UK / MakePlayingCards |
| 3D game bits | ❌ | Makr3D / 3D Vikings only |

**Verdict:** Most flat-print Xmas + pet + gaming-adjacent **can** come from Prodigi.  
Playing-card **decks** (Top Trumps quality) — pin Prodigi SKU first; switch to UK/MPC if deck feel isn’t good enough.

---

## Add-on strategy (all Prodigi listings)

Stick + postcard are **too cheap to ship alone**. Every Prodigi listing description now includes:

```
ADD-ONS (too cheap to ship alone — add to any order):
• Christmas Sticker Sheet — add for $3.99 (usually $7.99)
• Custom Postcard — add for $2.99 (usually $3.99)

SHIPPING:
• Free shipping on this listing
• FREE SHIPPING on orders over $19.99 when combined with another product
• Prodigi items ship together when ordered together
```

### Listings updated with add-on block
| Listing ID | Product |
|------------|---------|
| 4586675549 | Photo Book |
| 4586675569 | 2027 Calendar |
| 4586662046 | Christmas Card |
| 4586662062 | Wrapping Paper |
| 4586657625 | Jigsaw Puzzle |
| 4586691324 | Metal Pet Tag |
| 4586691336 | Dog Bandana |
| 4586687823 | Board Game Notebook |
| 4586691360 | Custom Top Trumps |
| 4586691376 | Game Night Coaster Set |
| 4586691388 | Personalised Playing Cards |

### Current shipping profile
`316299492609` — **free shipping** on destinations `none` / `GB` / `US` ($0 primary + $0 secondary).

**Free shipping over $19.99 combined:**  
Etsy’s “free shipping guarantee for orders over $X” is a **Shop Manager setting**, not fully controllable via our current token (`shops_w` missing).  
→ Put policy in every listing (done).  
→ Also enable in dashboard: Settings → Shipping → **Free shipping guarantee** (threshold $19.99) when you’re in Shop Manager.

**Why listing copy still matters:** buyers see it before checkout; the guarantee setting enforces it at basket level.

---

## New Prodigi Xmas gaming / pet listings (drafts)

| Listing ID | Product | Price | Prodigi |
|------------|---------|-------|---------|
| **4586691324** | Metal Pet Tag (bone/round) | $16.99 | `PET-MET-BONE` / `PET-MET-ROUND` ✅ |
| **4586691336** | Christmas Dog Bandana | $14.99 | `PET-BANDANA-SML/MED/LRG` ✅ |
| **4586687823** | Board Game / Cribbage Notebook | $16.99 | Notebook SKU — pin in dashboard |
| **4586691360** | Custom Top Trumps / Family Battle Cards | $24.99 | Playing-card SKU — pin, or UK/MPC |
| **4586691376** | Game Night Coaster Set | $19.99 | Wooden coasters — pin SKU |
| **4586691388** | Personalised Playing Cards (Xmas / wedding guest-book alt) | $22.99 | Playing-card SKU — pin, or UK/MPC |

---

## Prodigi SKU pin checklist (dashboard)

Open `dashboard.prodigi.com/product-info` and copy exact SKUs into this file:

- [ ] Greeting card (Fine Art 5×7) — currently using legacy `GLOBAL-CFGA-5X7` (API says EntityNotFound — **re-pin**)
- [ ] Sticker sheet (kiss-cut)
- [ ] Wrapping paper sheet
- [ ] Jigsaw (piece count + lid art)
- [ ] Photo book (layflat)
- [ ] Calendar 2027
- [ ] Wooden coasters
- [ ] Custom notebook
- [ ] Playing cards / deck box

---

## Christmas wedding one-liner (for listing copy later)

> “Getting married over Christmas? Our personalised playing cards double as guest-book cards — guests write on them, you keep the deck.”

Use on: 4586691388, 4586678898 (wedding video album).

---

## Priority after flagship 15

1. Pin Prodigi SKUs (card, stickers, wrap, notebook, coasters, playing cards)  
2. Dashboard: free shipping guarantee $19.99  
3. Sample order: pet tag + bandana + notebook + coaster + card deck  
4. Photos → activate pet tag, bandana, notebook, Top Trumps first  
5. Makr3D STLs still the 3D half of the store — don’t block on Prodigi pins  

---

## Files

- `oddhobbies/shop/PRODIGI-XMAS-OPS.md` — this  
- `oddhobbies/shop/XMAS-FLAGSHIP-15.md` — core 15  
- `oddhobbies/shop/xmas-drafts-2026-10-01.json` — IDs  

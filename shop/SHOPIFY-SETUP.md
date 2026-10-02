# Shopify — create store + add listings

> Sources: shopify.dev · help.shopify.com (products, CSV import)  
> Our data: `shop/listings/*.json` + `db` Shopify CSV template  
> Goal: PogPet on Shopify without building a custom cart from scratch

---

## Create the store (5 steps)

1. **Start trial** — https://www.shopify.com  
   - Plan: start **Basic** (or $1/mo trial if offered)  
   - Store name: `pogpet` or `oddhobbies` (matches brand)

2. **Store settings**
   - Currency: USD  
   - Address: your fulfilment country (UK)  
   - Domains: `pogpet.com` / `oddhobbies.com` (buy or connect later)

3. **Theme**
   - Start with **Dawn** (free, clean, fast)  
   - Later: premium theme if needed — not day-1  
   - Banner: reuse couple-brick lifestyle crop + cream brand look

4. **Payments**
   - Shopify Payments (cards) + PayPal  
   - Optional: Monero only if you have a processor (not native)

5. **Shipping**
   - Free shipping profile (same policy as Etsy: free, or free over $19.99)  
   - Production partners (Makr3D / Prodigi / Kunaki) ship direct — set as **fulfilment** not local stock

---

## Add listings — three ways

| Method | When | How |
|--------|------|-----|
| **A. Admin UI** | 1–5 products | Products → Add product → paste from `shop/listings/<SKU>.json` |
| **B. CSV import** | 15+ products | Products → Import → use Shopify CSV columns (below) |
| **C. API / app** | Automated | Admin API `productCreate` or POD apps (Printful, Makr3D) |

**Day-1 recommendation:** B (CSV from our packs) + A for Featured heroes.

---

## Shopify CSV (official columns)

We already map these in `channel_payloads` (`template_key=shopify_product_v1`):

```
Handle,Title,Body (HTML),Vendor,Type,Tags,Published,
Option1 Name,Option1 Value,
Variant SKU,Variant Grams,Variant Inventory Qty,
Variant Inventory Policy,Variant Fulfillment Service,Variant Price,
Variant Requires Shipping,Image Src,Image Position,Image Alt Text,
SEO Title,SEO Description,Status
```

| Field | Our value |
|-------|-----------|
| Handle | `xmas-3d-tile-rack` (slug from SKU) |
| Vendor | `OddHobbies` |
| Status | `draft` until photos ready |
| Variant SKU | internal SKU |
| Fulfillment Service | `manual` (or app later) |
| Tags | from listing pack (comma-separated) |
| Body (HTML) | description from pack |

### Generate CSV from packs
```bash
# after OAuth/API later — or manual export
# payload: db → channel_payloads WHERE channel='shopify'
```

---

## Collections (= Etsy sections)

| Shopify collection | Maps from |
|-------------------|-----------|
| Featured | brick couple, memory album |
| Couples & Weddings | couple figure, wedding album, cards, pet tags |
| Game Night | 3D game gifts, Top Trumps, notebooks |
| Physical Media | Memory album CD, Wedding video album |
| Add-Ons | stickers, postcards, wrapping |

Collections power menus — don’t make an “Xmas” collection (whole store is Xmas).

---

## POD / fulfilment apps (same as Etsy plan)

| Supplier | Shopify app / method |
|----------|----------------------|
| Makr3D | Native Shopify fulfilment location |
| Printie (US 3D) | Connect store when ready |
| Prodigi | Native Etsy/Shopify POD |
| Kunaki | Manual/API CD fulfilment |
| Printful | If mugs/apparel later |

---

## Shopify vs your own webpage

| | **Shopify** | **Own site** (Next/WordPress/custom) |
|--|-------------|--------------------------------------|
| **What it is** | Hosted commerce platform | You host code + DB |
| **Cart/checkout** | Built-in, PCI, taxes, fraud | You build (Stripe etc.) |
| **Payments** | Shopify Payments + wallets | Stripe/PayPal only you wire |
| **Themes** | Drag-drop + Liquid themes | Full design control |
| **Apps** | App Store (POD, email, reviews) | You integrate each service |
| **Product CSV/API** | First-class | You implement |
| **Speed to first sale** | **Days** | Weeks–months |
| **Cost** | ~$39/mo Basic + fees | Hosting + dev time |
| **SEO/blog** | Good enough | You control everything |
| **Custom logic** | Limited (Liquid, Functions) | Unlimited |
| **Agent/MCP catalog** | Storefront API / MCP | Your API + SQLite (we already have) |
| **Brand design freedom** | Medium | High |
| **Ops burden** | Shopify maintains platform | **You** maintain servers, security |

### Plain English
- **Shopify** = rent a shop that already has a till, stock system, and checkout. You bring products + photos.  
- **Own webpage** = build the whole shop yourself. More control, more work, no “Import CSV and sell” on day-1.

### What we do
| Layer | Choice |
|-------|--------|
| **Sell** | Shopify (storefront) + Etsy (discovery) |
| **Product truth** | Our SQLite (`oddhobbies.db`) |
| **Images** | R2 + ChatGPT prompts |
| **Agents later** | Consumer MCP reads catalog — not Shopify-only |
| **Custom site later** | Optional headless storefront if Shopify limits us |

**Don’t build a custom shop first.** Etsy for discovery, Shopify for own-domain cart, our DB for truth.

---

## Day-1 Shopify checklist

- [ ] Create store + USD  
- [ ] Dawn theme + couple-brick banner  
- [ ] Shipping: free / free over $19.99  
- [ ] 5 collections (no Xmas section)  
- [ ] Import CSV for Featured + Game Night first  
- [ ] Connect Prodigi / note Makr3D as fulfilment  
- [ ] About: photo → preview → brick → doorstep  
- [ ] Images from ChatGPT prompt pack  

---

## Related
- `db/CHANNEL-TEMPLATES.md` — Shopify CSV contract  
- `shop/listings/*.json` — title/tags/body source  
- `shop/STORE-STRUCTURE.md` — sections  
- `shop/IMAGE-PROMPTS.md` — product images  

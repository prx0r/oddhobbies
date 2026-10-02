# Shopify API — connect + push listings

> You're already in Shopify Admin. We need a **custom app Admin API token**.  
> Script: `shop/shopify_push.py`

---

## Get a token (2 minutes)

1. Shopify Admin → **Settings** → **Apps and sales channels**  
2. **Develop apps** → **Create app** → name `oddhobbies-api`  
3. **Configure Admin API scopes** → check:
   - `read_products`
   - `write_products`
   - (optional later) `read_orders`, `write_orders`, `read_customers`  
4. **Install app**  
5. **API credentials** → **Reveal Admin API access token**  
   - Starts with `shpat_...`  
6. Copy your store domain: `https://YOUR-STORE.myshopify.com`

---

## Store secrets

Preferred:
```bash
agent-vault vault credential set SHOPIFY_SHOP_DOMAIN --vault oracle
agent-vault vault credential set SHOPIFY_ACCESS_TOKEN --vault oracle
```

Or local file (not in git):
```
~/.config/oddhobbies/shopify.env
```
```
SHOPIFY_SHOP_DOMAIN=https://YOUR-STORE.myshopify.com
SHOPIFY_ACCESS_TOKEN=shpat_xxxxxxxxxxxx
```

---

## Push listing packs

```bash
# list existing products
python3 /root/oddhobbies/shop/shopify_push.py --list

# dry-run all packs
python3 /root/oddhobbies/shop/shopify_push.py --dry-run

# create all as draft products
python3 /root/oddhobbies/shop/shopify_push.py

# one SKU
python3 /root/oddhobbies/shop/shopify_push.py --sku ALBUM-MEMORY-CD

# go live when ready
python3 /root/oddhobbies/shop/shopify_push.py --status active
```

Each pack → Shopify product:
| Field | Source |
|-------|--------|
| Title | listing pack `etsy_title` |
| Body HTML | pack description |
| Vendor | OddHobbies |
| Tags | pack tags |
| Status | draft (default) |
| SKU | internal SKU |
| Price | pack price |
| Handle | slug from SKU |

Shopify product id is written back into `shop/listings/<SKU>.json`.

---

## Admin API shape (what the script calls)

```
POST https://YOUR-STORE.myshopify.com/admin/api/2026-10/products.json
X-Shopify-Access-Token: shpat_...
```
```json
{
  "product": {
    "title": "...",
    "body_html": "...",
    "vendor": "OddHobbies",
    "status": "draft",
    "tags": "...",
    "variants": [{"option1":"Default Title","price":"12.99","sku":"XMAS-3D-TILE-RACK", ...}]
  }
}
```

---

## After products exist (dashboard)

- Collections: Featured · Couples · Game Night · Physical Media · Add-Ons  
- Images: upload from R2 / generated assets  
- Shipping profile: free / free over $19.99  
- Connect Prodigi / note Makr3D as fulfilment  

---

## Shopify vs Etsy

Same product truth (`shop/listings/*.json` + SQLite).  
Etsy = discovery drafts. Shopify = own domain + cart.  
Don’t duplicate copy by hand — push from packs.

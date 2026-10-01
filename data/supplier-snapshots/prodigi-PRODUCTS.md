# Prodigi Products — PogPet

> Verified SKUs, dimensions, print areas, and availability.
> Last verified: 2026-09-30

## Active Products (used in PogPet store)

### Postcard
| Field | Value |
|-------|-------|
| **SKU** | `CLASSIC-POST-GLOS-6X4` |
| **Size** | 6x4" (152x109mm) |
| **Paper** | 350gsm gloss card |
| **Print method** | HP Indigo digital print |
| **Print areas** | `default` (front) |
| **Ships from** | UK |
| **Dispatch** | 24 hours |
| **Ships to** | Worldwide |
| **Wholesale** | From £0.40 |
| **Etsy listing** | ID: 4585445592, Price: $3.99 |

### Greeting Card (Fine Art)
| Field | Value |
|-------|-------|
| **SKU** | `GLOBAL-CFGA-5X7` (verify in dashboard) |
| **Size** | 5x7" |
| **Paper** | Mohawk card or gloss coated art |
| **Print areas** | `default` (front) |
| **Ships from** | UK, EU |
| **Dispatch** | 24-48 hours |
| **Ships to** | Worldwide |
| **Wholesale** | From £1.50 |
| **Etsy listing** | ID: 4584649933, Price: $5.99 |

### Wrapping Paper (Satin)
| Field | Value |
|-------|-------|
| **SKU prefix** | `WRAP` |
| **Sizes** | Sheets: 50x70cm, 75x90cm / Rolls: 70cm at 1-5m |
| **Paper** | 95gsm, gloss or satin laminate |
| **Print method** | Giclée |
| **Print areas** | `default` (all-over print) |
| **Ships from** | UK, EU |
| **Dispatch** | 24-48 hours |
| **Ships to** | Worldwide |
| **Wholesale** | From £3.00 |
| **Etsy listing** | ID: 4584649927, Price: $12.99 |

### Kiss-Cut Stickers
| Field | Value |
|-------|-------|
| **SKU prefix** | `STICK` (verify in dashboard) |
| **Types** | Kiss-cut, transparent, temporary tattoos |
| **Print areas** | `default` |
| **Ships from** | UK, EU |
| **Dispatch** | 24-48 hours |
| **Ships to** | Worldwide |
| **Wholesale** | From £0.80 |
| **Etsy listing** | ID: 4584659500, Price: $7.99 |

## Products NOT on Prodigi (3D printed — need Makr3D/Vikings)

| Product | Supplier | Notes |
|---------|----------|-------|
| Brick Figure | Makr3D (UK) / 3D Vikings (US) | Needs Meshy API key |
| Couple Figure | Makr3D / Vikings | 2x mesh |
| Pet Ornament | Makr3D / Vikings | Needs hook loop |
| Keychain | Makr3D / Vikings | Highest margin |

## Product Lookup (API)

```bash
curl -s "https://api.prodigi.com/v4.0/products/{SKU}" \
  -H "X-API-Key: {YOUR_API_KEY}"
```

Returns: dimensions, print areas, variants, shipping destinations.

## File Requirements

| Format | Optimal DPI | Notes |
|--------|-------------|-------|
| JPG or PNG | 300dpi | Most products |
| PDF | 300dpi | Some products (postcard back) |

**Important:** Postcards require address + stamp on back — download template from Prodigi dashboard.

## Pricing Tool

Download full price sheets (wholesale + shipping + +1 rates) from:
- **Dashboard:** `dashboard.prodigi.com/product-info`
- Shows per-product, per-destination pricing with combined shipping rates

# Prodigi Pricing — PogPet Margins

> Wholesale costs, suggested retail, and margin analysis.
> Last verified: 2026-09-30

## Wholesale Costs (from product pages)

| Product | SKU | Wholesale (GBP) | Wholesale (USD est.) |
|---------|-----|-----------------|---------------------|
| Postcard 6x4" | `CLASSIC-POST-GLOS-6X4` | £0.40 | ~$0.50 |
| Greeting Card 5x7" | `GLOBAL-CFGA-5X7` | £1.50 | ~$1.90 |
| Wrapping Paper (sheet) | `WRAP` | £3.00 | ~$3.80 |
| Wrapping Paper (roll 1m) | `WRAP` | £3.50 | ~$4.40 |
| Kiss-Cut Sticker Sheet | `STICK` | £0.80 | ~$1.00 |

*USD estimates based on ~1.26 exchange rate. Check live rates.*

## PogPet Retail Pricing

| Product | Retail | Wholesale | Shipping (est.) | **Gross Margin** |
|---------|--------|-----------|-----------------|-----------------|
| Postcard | $3.99 | $0.50 | $2.50 | **$0.99 (25%)** |
| Greeting Card | $5.99 | $1.90 | $2.50 | **$1.59 (27%)** |
| Wrapping Paper | $12.99 | $3.80 | $3.50 | **$5.69 (44%)** |
| Sticker Sheet | $7.99 | $1.00 | $2.00 | **$4.99 (62%)** |

*Shipping estimates include +1 rates for combined orders. Actual margins improve with multi-item orders.*

## Margin Notes

1. **Free shipping = you absorb shipping cost** — build it into retail price
2. **Combined orders boost margin** — one full shipping rate + cheap +1s
3. **Stickers are highest margin** — low wholesale, low shipping
4. **Postcards are lowest margin** — but lowest risk, highest volume potential
5. **Wrapping paper is mid-tier** — good margin, seasonal spike at Christmas

## Prodigi Pro Discount

If volume grows, **Prodigi Pro** gives:
- 15% off all postcards
- 10-25% off other products
- 75% off branded packaging inserts
- Dedicated account manager

**Worth it at:** ~50+ orders/month

## 3D Products (Not Prodigi)

| Product | Retail | Est. Cost (Makr3D) | **Gross Margin** |
|---------|--------|-------------------|-----------------|
| Brick Figure | $19.99 | ~$5.00 | **$14.99 (75%)** |
| Couple Figure | $34.99 | ~$10.00 | **$24.99 (71%)** |
| Pet Ornament | $14.99 | ~$4.00 | **$10.99 (73%)** |
| Keychain | $12.99 | ~$1.50 | **$11.49 (88%)** |

*3D products have much higher margins but need Meshy API + Makr3D account.*

## Revenue Scenarios (Monthly)

### Conservative (10 orders/month)
| Mix | Revenue | COGS | **Profit** |
|-----|---------|------|-----------|
| 5 postcards + 3 cards + 2 stickers | $47.93 | $22.40 | **$25.53** |

### Moderate (50 orders/month)
| Mix | Revenue | COGS | **Profit** |
|-----|---------|------|-----------|
| 20 postcards + 15 cards + 10 wrapping + 5 stickers | $339.65 | $148.50 | **$191.15** |

### With 3D products (30 orders/month)
| Mix | Revenue | COGS | **Profit** |
|-----|---------|------|-----------|
| 10 figures + 10 ornaments + 10 cards | $409.70 | $109.00 | **$300.70** |

## Pricing Strategy

1. **Start with free shipping** — absorbs ~$2-3 per order but increases conversion
2. **Bundle incentives** — "Add a postcard for $2 with any figure order"
3. **Christmas premium** — wrapping paper + ornament bundles at 10% discount
4. **Volume threshold** — at 50+ orders/month, evaluate Prodigi Pro subscription

## API Quote Endpoint

For exact per-order pricing, use the Prodigi Quote API:
```bash
curl -X POST "https://api.prodigi.com/v4.0/Quotes" \
  -H "X-API-Key: {key}" \
  -H "Content-Type: application/json" \
  -d '{"items": [{"sku": "CLASSIC-POST-GLOS-6X4", "copies": 1}], "shippingMethod": "Standard"}'
```

Note: Quote endpoint format may vary — test in sandbox first.

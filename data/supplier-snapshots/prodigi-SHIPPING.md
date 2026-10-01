# Prodigi Shipping — Consolidation Rules

> How combined shipping works, production times, and delivery estimates.
> Last verified: 2026-09-30

## Key Fact: Yes, Qty 1 Works

**Every product can be ordered individually (qty 1).** There is no minimum order. Prodigi is print-on-demand — one item, one order, no problem.

## Shipping Consolidation

### How Multi-Item Orders Work

When a customer buys multiple Prodigi products in one order:

1. **Same facility** → Items ship together, combined shipping
2. **Different facilities** → Each facility ships separately, costs combined

### The "+1" Rate System

| Item | Shipping Charge |
|------|----------------|
| 1st item (largest) | **Full rate** |
| 2nd+ items (same type) | **+1 rate** (reduced) |
| Items from different facilities | Full rate per facility |

**Example — Single postcard to US:**
- Postcard: Full shipping rate (~$2-4)

**Example — Postcard + greeting card to US:**
- Postcard: Full rate
- Greeting card: +1 rate (much cheaper)
- Total: 1 full + 1 small add-on

**Example — Postcard + wrapping paper + stickers to UK:**
- Wrapping paper: Full rate (largest item)
- Postcard: +1 rate
- Stickers: +1 rate
- Total: 1 full + 2 small add-ons

### Rolled Prints Exception

For rolled prints (wrapping paper on rolls), many regions use a **flat rate**:
- Full cost once for the largest roll
- No +1 charges for additional rolls
- Applies to US, EU, AU (in-house fulfilled)

## Shipping Methods

| Method | Speed | Tracking | Cost |
|--------|-------|----------|------|
| **Budget** | Slowest | Untracked (US always tracked) | Cheapest |
| **Standard** | Mid | Varies by destination | Medium |
| **Express** | Fastest | Always tracked (courier) | Most expensive |

**Recommendation for PogPet:** Use **Standard** — good balance of cost and speed. Offer free shipping (absorb cost into product price).

## Production + Dispatch Times

| Product Category | Dispatch Time |
|-----------------|---------------|
| **Global products** (prints, cards, stickers, wrapping) | 24-48 hours |
| **Apparel** | 1-4 days |
| **Homewares** (mugs, cushions) | 1-4 days |
| **Framed/canvased art** | 2-5 days |

**Important:** Production time is separate from shipping time.
- "Standard 3-5 day" = 3-5 days AFTER dispatch
- Total delivery = production + shipping

## Global Fulfilment

- Orders auto-routed to nearest print facility
- Facilities: UK, US, EU (mainland), AU
- 70+ manufacturing partners in 10+ countries
- Shorter distance = faster + cheaper + greener

## Delivery Estimates (Production + Shipping)

| Destination | Budget | Standard | Express |
|------------|--------|----------|---------|
| **UK** | 5-8 days | 3-5 days | 1-2 days |
| **US** | 7-12 days | 5-8 days | 2-3 days |
| **EU** | 7-12 days | 5-8 days | 2-4 days |
| **AU** | 10-15 days | 7-10 days | 3-5 days |
| **Rest of World** | 10-20 days | 7-15 days | 5-7 days |

*Estimates include production time. Actual times vary by product and destination.*

## Tracking

- **Budget:** Untracked (except US — all US orders tracked)
- **Standard:** Tracked or untracked depending on destination
- **Express:** Always tracked (courier service)
- Tracking link provided via email when order ships

## Lost/Replacement Policy

- If order not received within **30 days** → free replacement
- Exception: orders with incorrect address (not covered)

## PogPet Shipping Strategy

### Recommended Approach

1. **Offer FREE shipping** on all listings (absorb cost into product price)
2. **Use Standard shipping** as default
3. **Set processing time to 1-2 days** (matches Prodigi dispatch)
4. **Add buffer:** Tell buyers "5-10 business days" total delivery

### Pricing Template (Etsy listing)

```
FREE SHIPPING worldwide.
Your order will be produced and dispatched within 1-2 business days.
Estimated delivery: 5-10 business days (varies by location).
```

## Exact Pricing Source

Download per-product, per-destination shipping rates (including +1 rates) from:
- **Dashboard:** `dashboard.prodigi.com/product-info`
- **API:** Quote endpoint (requires correct format)

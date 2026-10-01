# 3D Print Suppliers

> For products that need to be physically 3D printed.

---

## Makr3D — PRIMARY

| Field | Value |
|-------|-------|
| **URL** | https://makr3d.app |
| **Location** | Huddersfield, UK (Yorkshire3D farm) |
| **Printers** | Hundreds of Bambu printers |
| **Capacity** | 500+ plates/day |
| **Materials** | PLA, PLA+, PETG, TPU, resin |
| **Colors** | 40+ stocked |
| **Etsy integration** | Native order sync (live) |
| **Shopify integration** | Yes |
| **API** | Full REST API (quotes, orders, webhooks) |
| **Monthly fee** | None |
| **White-label** | Yes |
| **Shipping** | Worldwide |
| **Shipper of record** | Yes |

### Pricing (ex-VAT)
| Size | Fulfilment | Typical Retail | Margin |
|------|-----------|----------------|--------|
| Small (Benchy-class) | £1.29 | £3-10 | 60-83% |
| Medium (fidget) | £2.50 | £12-20 | 72-83% |
| Large (articulated) | £7.60 | £25-35 | 59-71% |

### API Key
- Create at: makr3d.app → Settings → API keys
- Key format: `m3d_live_...`
- Auth: `Authorization: Bearer m3d_live_...`
- Docs: https://makr3d.app/help/api

### Integration Steps
1. Create account
2. Upload test STL
3. Get instant quote
4. Connect Etsy store
5. Test order flow

---

## Alternatives (for comparison)

### Shapeways (Closed 2023, replaced by others)
### Treatstock
| Field | Value |
|-------|-------|
| **URL** | https://treatstock.com |
| **Location** | Global network |
| **Materials** | PLA, ABS, nylon, resin, metal |
| **Note** | Good for metal prints |

### Craftcloud (by All3DP)
| Field | Value |
|-------|-------|
| **URL** | https://craftcloud3d.com |
| **Note** | Price comparison across multiple printers |

### Xometry
| Field | Value |
|-------|-------|
| **URL** | https://xometry.com |
| **Note** | Industrial grade, higher MOQ, better for production runs |

### JLC3DP (JLCPCB)
| Field | Value |
|-------|-------|
| **URL** | https://jlc3dp.com |
| **Location** | China |
| **Note** | Very cheap, longer shipping, good for bulk |

---

## Material Guide

| Material | Best For | Properties |
|----------|----------|------------|
| **PLA** | Display pieces, low-stress items | Easy to print, biodegradable, limited heat resistance |
| **PLA+** | Functional items, gifts | Stronger than PLA, better detail |
| **PETG** | Outdoor, durable items | Flexible, impact resistant, food-safe |
| **TPU** | Flexible items, phone cases | Rubber-like, bendable |
| **Resin (SLA)** | High-detail miniatures, jewelry | Smooth surface, fine detail, brittle |
| **Nylon** | Functional mechanical parts | Strong, flexible, expensive |

---

## File Formats

| Format | Use |
|--------|-----|
| **STL** | Universal, single color |
| **3MF** | Multi-color, print settings included |
| **OBJ** | Universal, with textures |
| **STEP** | CAD interchange |

**Makr3D prefers 3MF** — preserves your print settings through production.

# OddHobbies Canonical DB (SQLite + MCP)

> One relational database for **suppliers × products × channel listings**.  
> Readable by MCP tools (Etsy, Shopify, future channels).  
> **DB file:** `oddhobbies.db`  
> **Schema:** `schema.sql`  
> **Seed:** `seed.py` ← `data/product-supplier-db.json`

---

## Why SQLite

| Need | Fit |
|------|-----|
| One file, no server | Perfect for agents + local tools |
| Relational suppliers↔products | Real FKs, not JSON soup |
| MCP-readable | `mcp_server.py` stdio JSON-RPC |
| Multi-channel | `shops` + `listings.external_id` |
| Point-in-time costs | `product_costs` with `is_current` |
| Lead times by place | `supplier_lead_times` + `product_shipping` |

---

## Entity map

```
suppliers ──< supplier_locations
         ──< supplier_materials
         ──< supplier_cost_tiers
         ──< supplier_lead_times
              │
products ──< product_suppliers >── suppliers
         ──< product_costs
         ──< product_retail_prices
         ──< product_files
         ──< product_shipping >── suppliers
              │
shops ──< listings >── products
              ──< listing_addons
shop_policies
open_quotes
decisions
```

---

## Tables (summary)

| Table | Purpose |
|-------|---------|
| `suppliers` | Makr3D, Printie, Prodigi, Kunaki, … |
| `supplier_cost_tiers` | £1.29 small, PET-MET-BONE, CD $2, … |
| `supplier_lead_times` | UK 2–5d, US 6–16d, … |
| `products` | SKU, section, make, material, status |
| `product_suppliers` | Which supplier makes it (role) |
| `product_costs` | Current unit cost per supplier |
| `product_retail_prices` | Etsy/Shopify price + volume tiers |
| `listings` | Etsy `external_id`, Shopify later |
| `listing_addons` | Sticker $3.99, postcard $2.99 |
| `open_quotes` | P0/P1 blockers |

---

## Setup

```bash
# 1. Create + seed
python3 /root/oddhobbies/db/seed.py

# 2. Inspect
sqlite3 /root/oddhobbies/db/oddhobbies.db ".tables"
sqlite3 /root/oddhobbies/db/oddhobbies.db "SELECT * FROM v_products_current;"

# 3. Run MCP server (stdio)
python3 /root/oddhobbies/db/mcp_server.py
```

---

## MCP tools

| Tool | Args | Returns |
|------|------|---------|
| `db_stats` | — | table counts |
| `db_list_suppliers` | `region_focus?` | directory + cost tiers + leads |
| `db_list_products` | `section?` `status?` `supplier?` | products + cost + retail |
| `db_get_product` | `sku` or `listing_id` | full graph for one product |
| `db_fulfilment_matrix` | `sku?` `supplier_id?` | cost + lead by destination |
| `db_list_etsy_drafts` | — | draft listings |
| `db_open_quotes` | — | blockers |
| `db_search` | `q` | products + suppliers LIKE |
| `db_sql` | `sql` | **read-only** SQL |

### Register MCP in opencode

Copy into project opencode config, or:

```json
{
  "mcpServers": {
    "oddhobbies-db": {
      "command": "python3",
      "args": ["/root/oddhobbies/db/mcp_server.py"]
    }
  }
}
```

Example config file: `db/mcp.config.json`

---

## Useful views

```sql
-- What we're selling + who + cost + price
SELECT * FROM v_products_current ORDER BY section, sku;

-- Supplier phone-book
SELECT * FROM v_supplier_directory;

-- Where things ship from and how long
SELECT * FROM v_product_fulfilment_matrix WHERE destination = 'US';

-- Etsy drafts
SELECT * FROM v_etsy_drafts;

-- Blockers
SELECT * FROM v_open_quotes;
```

---

## MCP call examples (JSON-RPC lines)

```json
{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"db_list_products","arguments":{"section":"Game Night"}}}
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"db_get_product","arguments":{"sku":"XMAS-3D-TILE-RACK"}}}
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"db_sql","arguments":{"sql":"SELECT sku, unit_cost FROM product_costs WHERE is_current=1"}}}
```

---

## Multi-channel plan

| Channel | How |
|---------|-----|
| **Etsy** | `shops.id='etsy:67863887'`, `listings.external_id=listing_id` |
| **Shopify** | `shops.id='shopify:pogpet'`, `listings.external_id=product/variant id` |
| **Future** | New `shops` row; same `products` |

Sync rules:
- Product truth lives in `products` + costs
- Channel copies live in `listings` (price, state, taxonomy)
- Never store API tokens in DB — only `api_key_ref` names

---

## Updating costs

1. Get quote → INSERT new `product_costs` row (`is_current=0` old, `1` new)  
2. Or UPDATE `product_costs` where `is_current=1`  
3. Re-run MCP `db_get_product` to verify  

---

## Related docs

- `data/product-supplier-db.json` — flat seed (source for `seed.py`)  
- `data/PRODUCT-SUPPLIER-DB.md` — human tables  
- `shop/US-3D-SUPPLIER.md` — Printie vs Makr3D  
- `shop/FLAGSHIP-COSTS.md` — margins + sections  

---

## Status

| Item | State |
|------|-------|
| Schema | ✅ |
| Seed script | ✅ |
| DB file | ✅ after `seed.py` |
| MCP server | ✅ stdio |
| Etsy listing IDs | ✅ seeded |
| Shopify IDs | ⬜ placeholder shop row |
| Live quotes (Printie/Makr3D/Prodigi pins) | ⬜ open_quotes |

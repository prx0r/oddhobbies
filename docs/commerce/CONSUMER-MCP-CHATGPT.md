# Consumer MCP — ChatGPT / Muse / Grok

**Shell:** `db/consumer_mcp.py`  
**Theory:** bgraph `docs/architecture/AGENT-SURFACE.md` + OpenAI plugin guidelines  
**Purpose:** agents interact with stores for the **full chain** — not ops.

---

## Connect

### Local / stdio (now)

```bash
cd /root/oddhobbies
python3 db/consumer_mcp.py
```

### ChatGPT developer mode (later public URL)

```
https://mcp.oddhobb.com/mcp
```

Local test: pipe MCP JSON-RPC lines, or connect via MCP Inspector.

---

## Full chain

```
1. search_products / get_product     catalog
2. upload_photo                     person/dog image → photo_id
3. get_photo_status                 machine view + mesh status
4. get_quote                        price + fulfilment (show customer)
5. start_checkout                   external Shopify / store URL
6. get_order_status                 by order_ref
```

Mesh sculpt / heavy QC stays on **pogpet site pipeline** (Meshy, credits).
This MCP reserves the order and hands the customer to **Shopify checkout**.

---

## Tools + annotations

| Tool | readOnly | openWorld | destructive |
|------|----------|-----------|-------------|
| search_products | true | false | false |
| get_product | true | false | false |
| upload_photo | false | false | false |
| get_photo_status | true | false | false |
| get_quote | true | false | false |
| start_checkout | false | **true** | false |
| get_order_status | true | false | false |

---

## store_id

`oddhobb` · `grimoirer` · `stonedoorway`  
Default: `oddhobb` if omitted.

---

## What agents never get

Unit costs · vault keys · ops SQL · supplier APIs.

---

## Example call sequence

```json
{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_products","arguments":{"store_id":"oddhobb","q":"figurine"}}}
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"upload_photo","arguments":{"store_id":"oddhobb","image_url":"https://…/dog.jpg","customer_email":"a@b.com"}}}
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_photo_status","arguments":{"store_id":"oddhobb","photo_id":"ph_…"}}}
{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"get_quote","arguments":{"store_id":"oddhobb","sku":"XMAS-3D-ORNAMENT","photo_id":"ph_…"}}}
{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"start_checkout","arguments":{"store_id":"oddhobb","sku":"XMAS-3D-ORNAMENT","photo_id":"ph_…","customer_email":"a@b.com"}}}
```

---

## Related

- Commerce ops MCP: `db/commerce_mcp.py` (internal)
- Site Muse MCP: `/root/pogpet` `mcp_server.py` + `docs/muse-mcp-design.md`
- Consumer projection: `db/CONSUMER-MCP.md`
- Agent surface spec: `/root/bgraph/registry/agent_surfaces/consumer_mcp.json`

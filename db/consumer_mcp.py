#!/usr/bin/env python3
"""Consumer MCP — ChatGPT / Muse / Grok surface for brand stores.

Basic flexible shell for the full chain:
  photo → machine view/mesh → products/pricing → Shopify checkout

stdio JSON-RPC 2.0 MCP. No UI. No secrets in tool results.

Usage:
  python3 consumer_mcp.py
  # or connect ChatGPT dev mode to a public HTTPS /mcp later
"""
from __future__ import annotations

import json
import os
import re
import sqlite3
import sys
import uuid
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
COMMERCE_DB = ROOT / "db" / "commerce.db"
LEGACY_DB = ROOT / "db" / "oddhobbies.db"
SESSIONS = Path(os.environ.get("CONSUMER_MCP_SESSIONS", "/tmp/oddhobbies_consumer_mcp.json"))
DEFAULT_STORE = os.environ.get("CONSUMER_MCP_DEFAULT_STORE", "oddhobb")
VALID_STORES = {"oddhobb", "grimoirer", "stonedoorway"}

# In-process session store (photo uploads + checkout refs).
# Durable later; flexible shell for now.
_SESSIONS: dict[str, dict] = {}


def _db() -> Path:
    if COMMERCE_DB.exists():
        return COMMERCE_DB
    return LEGACY_DB


def connect() -> sqlite3.Connection:
    path = _db()
    if not Path(path).exists():
        raise FileNotFoundError(f"commerce db missing: {path}")
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def store_id(raw: Any) -> str:
    sid = (raw or DEFAULT_STORE or "").strip()
    if not sid:
        return DEFAULT_STORE
    if sid not in VALID_STORES:
        raise ValueError(f"unknown store_id: {sid} (expected one of {sorted(VALID_STORES)})")
    return sid


def _public_product(row: sqlite3.Row) -> dict:
    return {
        "sku": row["sku"],
        "agent_sku": row["agent_sku"] or row["sku"],
        "display_name": row["display_name"] or row["title"],
        "summary": row["summary"] or (row["title"] or "")[:200],
        "price_tier": row["price_tier"] or "gift",
        "display_price": row["display_price"],
        "display_currency": row["display_currency"],
        "section": row["section"],
        "fulfilment_blurb": row["fulfilment_blurb"],
        "is_orderable": bool(row["is_orderable"]),
        "is_customisable": bool(row["is_customisable"]),
        "gift_occasions": row["gift_occasions"],
    }


def tool_search_products(args: dict) -> dict:
    sid = store_id(args.get("store_id"))
    conn = connect()
    q = args.get("q") or args.get("query") or ""
    sql = "SELECT * FROM v_agent_catalog WHERE store_id=?"
    params: list[Any] = [sid]
    if q:
        sql += " AND (display_name LIKE ? OR summary LIKE ? OR product_sku LIKE ?)"
        like = f"%{q}%"
        params.extend([like, like, like])
    if args.get("gift_for"):
        sql += " AND gift_occasions LIKE ?"
        params.append(f"%{args['gift_for']}%")
    if args.get("section"):
        sql += " AND section=?"
        params.append(args["section"])
    sql += " ORDER BY is_orderable DESC, display_name LIMIT ?"
    params.append(int(args.get("limit") or 20))
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    products = [
        {
            "sku": r["product_sku"],
            "agent_sku": r["agent_sku"],
            "display_name": r["display_name"],
            "summary": (r["summary"] or "")[:240],
            "price_tier": r["price_tier"],
            "display_price": r["display_price"],
            "display_currency": r["display_currency"],
            "section": r["section"],
            "fulfilment_blurb": r["fulfilment_blurb"],
            "is_orderable": bool(r["is_orderable"]),
        }
        for r in rows
    ]
    return {
        "store_id": sid,
        "count": len(products),
        "products": products,
        "hint": "Use get_product for details, get_quote for price, start_checkout when ready.",
    }


def tool_get_product(args: dict) -> dict:
    sid = store_id(args.get("store_id"))
    sku = args.get("sku") or args.get("agent_sku")
    if not sku:
        raise ValueError("sku or agent_sku required")
    conn = connect()
    row = conn.execute(
        """SELECT * FROM v_agent_catalog
           WHERE store_id=? AND (agent_sku=? OR product_sku=?)""",
        (sid, sku, sku),
    ).fetchone()
    if not row:
        # fallback ops product public fields
        row2 = conn.execute(
            """SELECT p.sku, p.title, p.agent_sku, p.section, p.status,
                      rp.price, rp.currency
               FROM products p
               LEFT JOIN product_retail_prices rp
                 ON rp.product_id=p.id AND rp.is_current=1 AND rp.channel='etsy'
                AND rp.tier_code IS NULL
               WHERE p.store_id=? AND (p.sku=? OR p.agent_sku=?)""",
            (sid, sku, sku),
        ).fetchone()
        conn.close()
        if not row2:
            raise ValueError(f"product not found: {sid}/{sku}")
        return {
            "store_id": sid,
            "sku": row2["sku"],
            "agent_sku": row2["agent_sku"],
            "display_name": row2["title"],
            "summary": row2["title"],
            "section": row2["section"],
            "status": row2["status"],
            "display_price": row2["price"],
            "display_currency": row2["currency"],
            "personalisation_questions": [],
            "hint": "Limited public record. Call get_quote for pricing blurb.",
        }
    questions = conn.execute(
        """SELECT question_text, question_type, required, max_chars
           FROM personalisation_questions pq
           JOIN products p ON p.id = pq.product_id
           WHERE p.store_id=? AND (p.sku=? OR p.agent_sku=?)""",
        (sid, sku, sku),
    ).fetchall()
    assets = conn.execute(
        """SELECT asset_key, role, path_or_url, alt_text
           FROM assets WHERE store_id=? AND sku=? LIMIT 5""",
        (sid, row["product_sku"]),
    ).fetchall()
    conn.close()
    return {
        "store_id": sid,
        **_public_product(row),
        "personalisation_questions": [dict(q) for q in questions],
        "public_assets": [
            {"asset_key": a["asset_key"], "role": a["role"], "url": a["path_or_url"], "alt": a["alt_text"]}
            for a in assets
        ],
        "hint": "Show questions to the customer before get_quote / start_checkout.",
    }


def tool_upload_photo(args: dict) -> dict:
    sid = store_id(args.get("store_id"))
    b64 = args.get("file_b64") or args.get("image_b64")
    url = args.get("image_url") or args.get("url")
    owner = (args.get("customer_email") or args.get("owner") or "guest").strip()[:80]
    if not b64 and not url:
        raise ValueError("Provide file_b64 or image_url")
    if b64 and len(b64) < 64:
        raise ValueError("file_b64 looks too small")
    photo_id = f"ph_{uuid.uuid4().hex[:12]}"
    record = {
        "photo_id": photo_id,
        "store_id": sid,
        "owner": owner,
        "source": "b64" if b64 else "url",
        "bytes_b64_len": len(b64) if b64 else 0,
        "image_url": url,
        "status": "uploaded",
        "qc": {
            "passed": True,
            "notes": ["Accepted into consumer shell. Full QC/mesh runs on site pipeline."],
        },
        "mesh": {
            "status": "not_started",
            "mesh_id": None,
            "preview_url": None,
            "note": "Mesh sculpt is site/pogpet pipeline (credits). Call get_photo_status; start mesh on site or via site MCP.",
        },
        "machine_view": {
            "subject_guess": args.get("subject") or "person_or_pet",
            "has_person": None,
            "has_pet": None,
        },
        "next": "get_photo_status then search_products / start_checkout with photo_id",
    }
    _SESSIONS[photo_id] = record
    _persist_sessions()
    return {
        "store_id": sid,
        "photo_id": photo_id,
        "status": "uploaded",
        "qc": record["qc"],
        "mesh": record["mesh"],
        "hint": record["next"],
    }


def tool_get_photo_status(args: dict) -> dict:
    sid = store_id(args.get("store_id"))
    photo_id = args.get("photo_id")
    if not photo_id:
        raise ValueError("photo_id required")
    rec = _SESSIONS.get(photo_id)
    if not rec:
        # try legacy figg db if present
        legacy = ROOT.parent / "pogpet" / "data" / "figg.db"
        if legacy.exists():
            try:
                c = sqlite3.connect(legacy)
                c.row_factory = sqlite3.Row
                row = c.execute(
                    "SELECT * FROM photos WHERE id=? OR r2_key LIKE ?",
                    (photo_id, f"%{photo_id}%"),
                ).fetchone()
                c.close()
                if row:
                    return {
                        "store_id": sid,
                        "photo_id": photo_id,
                        "status": "found_legacy",
                        "source": "pogpet/data/figg.db",
                        "fields": {k: row[k] for k in row.keys() if k in ("id", "owner", "mime", "width", "height", "created_at")},
                        "mesh": {"status": "check_site_pipeline", "note": "Mesh jobs live in pogpet backend"},
                    }
            except Exception:
                pass
        raise ValueError(f"photo_id not found: {photo_id}")
    if rec.get("store_id") != sid and sid != DEFAULT_STORE:
        # allow status if store matches or is default query
        pass
    return rec


def tool_get_quote(args: dict) -> dict:
    sid = store_id(args.get("store_id"))
    sku = args.get("sku") or args.get("agent_sku")
    if not sku:
        raise ValueError("sku required")
    photo_id = args.get("photo_id")
    answers = args.get("answers") or {}
    conn = connect()
    row = conn.execute(
        """SELECT ac.*, p.sku AS product_sku, p.title, p.make
           FROM agent_catalog ac
           JOIN products p ON p.id=ac.product_id
           WHERE ac.store_id=? AND (ac.agent_sku=? OR p.sku=?)""",
        (sid, sku, sku),
    ).fetchone()
    if not row:
        conn.close()
        raise ValueError(f"product not found for quote: {sku}")
    retail = conn.execute(
        """SELECT price, currency FROM product_retail_prices
           WHERE product_id=(SELECT id FROM products WHERE store_id=? AND sku=?)
             AND is_current=1 AND channel='etsy' AND tier_code IS NULL""",
        (sid, row["product_sku"]),
    ).fetchone()
    conn.close()
    personalisation = []
    if answers:
        personalisation = [{"key": k, "value": v} for k, v in answers.items()]
    quote = {
        "store_id": sid,
        "sku": row["product_sku"],
        "agent_sku": row["agent_sku"],
        "display_name": row["display_name"] or row["title"],
        "price_tier": row["price_tier"] or "gift",
        "display_price": retail["price"] if retail else None,
        "display_currency": retail["currency"] if retail else None,
        "fulfilment_blurb": row["fulfilment_blurb"] or "Made to order · tracked shipping",
        "personalisation": personalisation,
        "photo_id": photo_id,
        "notes": [
            "Price shown to customer before checkout.",
            "Final total and shipping confirmed on store checkout.",
        ],
        "next": "start_checkout when the customer accepts this quote",
    }
    return quote


def tool_start_checkout(args: dict) -> dict:
    sid = store_id(args.get("store_id"))
    sku = args.get("sku") or args.get("agent_sku")
    photo_id = args.get("photo_id")
    customer_email = (args.get("customer_email") or "").strip()
    if not sku:
        raise ValueError("sku required")
    if not customer_email:
        raise ValueError("customer_email required for checkout")
    if photo_id and photo_id not in _SESSIONS:
        raise ValueError(f"photo_id not found: {photo_id}")

    order_ref = f"ORD-{uuid.uuid4().hex[:10].upper()}"
    domains = {
        "oddhobb": "https://oddhobb.com",
        "grimoirer": "https://grimoirer.com",
        "stonedoorway": "https://stonedoorway.com",
    }
    # Shopify store for oddhobb catalog
    shopify = "https://byg8sv-p6.myshopify.com"
    # Prefer brand domain cart path; Shopify handle-style checkout later.
    checkout_url = f"{domains.get(sid, domains['oddhobb'])}/checkout?sku={sku}&photo_id={photo_id or ''}&order_ref={order_ref}"
    alt_url = f"{shopify}/cart/1:1?sku={sku}"

    order = {
        "order_ref": order_ref,
        "store_id": sid,
        "sku": sku,
        "photo_id": photo_id,
        "customer_email": customer_email,
        "status": "reserved",
        "checkout_url": checkout_url,
        "shopify_cart_url": alt_url,
        "currency_hint": "See store checkout",
        "notes": [
            "Order reserved in consumer shell.",
            "Customer completes payment on Shopify/store checkout (external checkout).",
            "Fulfilment: site pipeline (mesh/print) + Shopify order ops.",
        ],
    }
    _SESSIONS[order_ref] = order
    _persist_sessions()
    return {
        "store_id": sid,
        "order_ref": order_ref,
        "status": "reserved",
        "checkout_url": checkout_url,
        "shopify_cart_url": alt_url,
        "hint": "Send the customer the checkout_url. Use get_order_status later.",
    }


def tool_get_order_status(args: dict) -> dict:
    sid = store_id(args.get("store_id"))
    order_ref = args.get("order_ref")
    if not order_ref:
        raise ValueError("order_ref required")
    rec = _SESSIONS.get(order_ref)
    if not rec:
        raise ValueError(f"order_ref not found: {order_ref}")
    return rec


TOOLS: dict[str, dict] = {
    "search_products": {
        "description": "List products for a store (browse catalog).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string", "enum": sorted(VALID_STORES)},
                "q": {"type": "string"},
                "gift_for": {"type": "string"},
                "section": {"type": "string"},
                "limit": {"type": "integer", "minimum": 1, "maximum": 50},
            },
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": False, "destructiveHint": False},
        "handler": tool_search_products,
    },
    "get_product": {
        "description": "Public product details + personalisation questions.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string"},
                "sku": {"type": "string"},
                "agent_sku": {"type": "string"},
            },
            "required": ["sku"],
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": False, "destructiveHint": False},
        "handler": tool_get_product,
    },
    "upload_photo": {
        "description": "Upload person/pet photo to start custom figurine pipeline.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string"},
                "file_b64": {"type": "string"},
                "image_url": {"type": "string"},
                "customer_email": {"type": "string"},
                "subject": {"type": "string"},
            },
        },
        "annotations": {"readOnlyHint": False, "openWorldHint": False, "destructiveHint": False},
        "handler": tool_upload_photo,
    },
    "get_photo_status": {
        "description": "Machine-readable photo + mesh status.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string"},
                "photo_id": {"type": "string"},
            },
            "required": ["photo_id"],
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": False, "destructiveHint": False},
        "handler": tool_get_photo_status,
    },
    "get_quote": {
        "description": "Price tier + fulfilment blurb before checkout.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string"},
                "sku": {"type": "string"},
                "agent_sku": {"type": "string"},
                "photo_id": {"type": "string"},
                "answers": {"type": "object"},
            },
            "required": ["sku"],
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": False, "destructiveHint": False},
        "handler": tool_get_quote,
    },
    "start_checkout": {
        "description": "Reserve order + external Shopify/store checkout URL (physical goods).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string"},
                "sku": {"type": "string"},
                "agent_sku": {"type": "string"},
                "photo_id": {"type": "string"},
                "customer_email": {"type": "string"},
            },
            "required": ["sku", "customer_email"],
        },
        "annotations": {"readOnlyHint": False, "openWorldHint": True, "destructiveHint": False},
        "handler": tool_start_checkout,
    },
    "get_order_status": {
        "description": "Order status by order_ref.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string"},
                "order_ref": {"type": "string"},
            },
            "required": ["order_ref"],
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": False, "destructiveHint": False},
        "handler": tool_get_order_status,
    },
}

SERVER_INFO = {
    "name": "oddhobbies-consumer-mcp",
    "version": "0.1.0",
    "instructions": (
        "Consumer tools for OddHobb/Grimoirer stores. Full chain: upload_photo → get_photo_status "
        "→ search_products/get_product → get_quote → start_checkout (external Shopify URL) → get_order_status. "
        "store_id: oddhobb|grimoirer|stonedoorway. Never invent unit costs. Show quote before checkout."
    ),
}


def _persist_sessions() -> None:
    try:
        SESSIONS.parent.mkdir(parents=True, exist_ok=True)
        SESSIONS.write_text(json.dumps(_SESSIONS, indent=2))
    except Exception:
        pass


def _load_sessions() -> None:
    global _SESSIONS
    if SESSIONS.exists():
        try:
            _SESSIONS = json.loads(SESSIONS.read_text())
        except Exception:
            _SESSIONS = {}


def _write(stream, obj: dict) -> None:
    stream.write(json.dumps(obj, ensure_ascii=False) + "\n")
    stream.flush()


def main() -> int:
    _load_sessions()
    stdin, stdout = sys.stdin, sys.stdout
    while True:
        line = stdin.readline()
        if not line:
            break
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        method = msg.get("method")
        msg_id = msg.get("id")
        if method == "initialize":
            _write(
                stdout,
                {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": SERVER_INFO,
                        "instructions": SERVER_INFO["instructions"],
                    },
                },
            )
        elif method == "tools/list":
            tools = [
                {
                    "name": k,
                    "description": v["description"],
                    "inputSchema": v["inputSchema"],
                    "annotations": v.get("annotations", {}),
                }
                for k, v in TOOLS.items()
            ]
            _write(stdout, {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": tools}})
        elif method == "tools/call":
            params = msg.get("params") or {}
            name = params.get("name")
            args = params.get("arguments") or {}
            tool = TOOLS.get(name)
            if not tool:
                _write(
                    stdout,
                    {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "error": {"code": -32602, "message": f"unknown tool: {name}"},
                    },
                )
                continue
            try:
                result = tool["handler"](args)
                _write(
                    stdout,
                    {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": {
                            "content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}],
                            "structuredContent": result,
                            "isError": False,
                        },
                    },
                )
            except Exception as e:  # noqa: BLE001
                _write(
                    stdout,
                    {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": {
                            "content": [{"type": "text", "text": json.dumps({"error": str(e)})}],
                            "isError": True,
                        },
                    },
                )
        elif method in ("ping", "shutdown"):
            _write(stdout, {"jsonrpc": "2.0", "id": msg_id, "result": {"ok": True}})
        elif msg_id is not None:
            _write(
                stdout,
                {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {"code": -32601, "message": f"method not found: {method}"},
                },
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

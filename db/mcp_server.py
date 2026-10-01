#!/usr/bin/env python3
"""Minimal MCP stdio server: query the OddHobbies product-supplier SQLite DB.

Tools:
  db_stats                  — row counts
  db_list_suppliers         — supplier directory view
  db_list_products          — products + primary supplier + cost + retail
  db_get_product            — one product + suppliers + costs + shipping + files + listings
  db_fulfilment_matrix      — product × supplier × destination lead times
  db_list_etsy_drafts       — draft listings
  db_open_quotes            — open quote blockers
  db_search                 — LIKE search across products/suppliers
  db_sql                    — read-only SQL (SELECT only)
"""

from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parent / "oddhobbies.db"

# --- tiny MCP protocol over stdio (JSON-RPC 2.0, line-delimited optional) ---
# Implements: initialize, tools/list, tools/call, ping, shutdown


def connect() -> sqlite3.Connection:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"DB not found: {DB_PATH}. Run db/seed.py first.")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def rows_to_dicts(rows: list[sqlite3.Row]) -> list[dict[str, Any]]:
    return [dict(r) for r in rows]


def tool_db_stats(_: dict) -> dict:
    conn = connect()
    tables = [
        "suppliers",
        "supplier_locations",
        "supplier_materials",
        "supplier_cost_tiers",
        "supplier_lead_times",
        "products",
        "product_suppliers",
        "product_costs",
        "product_retail_prices",
        "product_files",
        "product_shipping",
        "shops",
        "listings",
        "listing_addons",
        "shop_policies",
        "open_quotes",
        "decisions",
    ]
    counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in tables}
    conn.close()
    return {"db_path": str(DB_PATH), "counts": counts}


def tool_db_list_suppliers(args: dict) -> dict:
    conn = connect()
    q = "SELECT * FROM v_supplier_directory"
    params: list[Any] = []
    if args.get("region_focus"):
        q += " WHERE region_focus LIKE ?"
        params.append(f"%{args['region_focus']}%")
    q += " ORDER BY id"
    out = rows_to_dicts(conn.execute(q, params).fetchall())
    conn.close()
    return {"suppliers": out}


def tool_db_list_products(args: dict) -> dict:
    conn = connect()
    q = "SELECT * FROM v_products_current"
    where = []
    params: list[Any] = []
    if args.get("section"):
        where.append("section = ?")
        params.append(args["section"])
    if args.get("status"):
        where.append("status = ?")
        params.append(args["status"])
    if args.get("supplier"):
        where.append("primary_supplier = ?")
        params.append(args["supplier"])
    if where:
        q += " WHERE " + " AND ".join(where)
    q += " ORDER BY section, sku"
    out = rows_to_dicts(conn.execute(q, params).fetchall())
    conn.close()
    return {"products": out, "count": len(out)}


def tool_db_get_product(args: dict) -> dict:
    sku = args.get("sku") or args.get("listing_id")
    if not sku:
        raise ValueError("sku or listing_id required")
    conn = connect()
    # resolve product by sku or etsy external id
    row = conn.execute("SELECT * FROM products WHERE sku = ?", (sku,)).fetchone()
    if not row and str(sku).isdigit():
        row = conn.execute(
            """SELECT p.* FROM products p
               JOIN listings l ON l.product_id = p.id
               WHERE l.external_id = ?""",
            (str(sku),),
        ).fetchone()
    if not row:
        conn.close()
        raise ValueError(f"product not found: {sku}")
    pid = row["id"]
    product = dict(row)
    product["suppliers"] = rows_to_dicts(
        conn.execute(
            """SELECT ps.role, ps.supplier_sku, s.id, s.name, s.location, s.status
               FROM product_suppliers ps JOIN suppliers s ON s.id = ps.supplier_id
               WHERE ps.product_id = ? ORDER BY ps.role""",
            (pid,),
        ).fetchall()
    )
    product["costs"] = rows_to_dicts(
        conn.execute(
            """SELECT pc.*, s.name AS supplier_name
               FROM product_costs pc JOIN suppliers s ON s.id = pc.supplier_id
               WHERE pc.product_id = ? AND pc.is_current = 1""",
            (pid,),
        ).fetchall()
    )
    product["retail"] = rows_to_dicts(
        conn.execute(
            "SELECT * FROM product_retail_prices WHERE product_id = ? AND is_current = 1",
            (pid,),
        ).fetchall()
    )
    product["shipping"] = rows_to_dicts(
        conn.execute(
            """SELECT sh.*, s.name AS supplier_name
               FROM product_shipping sh JOIN suppliers s ON s.id = sh.supplier_id
               WHERE sh.product_id = ?""",
            (pid,),
        ).fetchall()
    )
    product["files"] = rows_to_dicts(
        conn.execute("SELECT * FROM product_files WHERE product_id = ?", (pid,)).fetchall()
    )
    product["listings"] = rows_to_dicts(
        conn.execute(
            """SELECT l.*, sh.channel, sh.shop_name
               FROM listings l JOIN shops sh ON sh.id = l.shop_id
               WHERE l.product_id = ?""",
            (pid,),
        ).fetchall()
    )
    conn.close()
    return product


def tool_db_fulfilment_matrix(args: dict) -> dict:
    conn = connect()
    q = "SELECT * FROM v_product_fulfilment_matrix"
    params: list[Any] = []
    if args.get("sku"):
        q += " WHERE sku = ?"
        params.append(args["sku"])
    elif args.get("supplier_id"):
        q += " WHERE supplier_id = ?"
        params.append(args["supplier_id"])
    out = rows_to_dicts(conn.execute(q, params).fetchall())
    conn.close()
    return {"rows": out, "count": len(out)}


def tool_db_list_etsy_drafts(args: dict) -> dict:
    conn = connect()
    out = rows_to_dicts(conn.execute("SELECT * FROM v_etsy_drafts").fetchall())
    conn.close()
    return {"drafts": out, "count": len(out)}


def tool_db_open_quotes(args: dict) -> dict:
    conn = connect()
    out = rows_to_dicts(conn.execute("SELECT * FROM v_open_quotes").fetchall())
    conn.close()
    return {"open_quotes": out, "count": len(out)}


def tool_db_search(args: dict) -> dict:
    term = args.get("q") or args.get("query") or ""
    if not term:
        raise ValueError("q required")
    like = f"%{term}%"
    conn = connect()
    products = rows_to_dicts(
        conn.execute(
            """SELECT sku, title, section, make, status FROM products
               WHERE sku LIKE ? OR title LIKE ? OR section LIKE ? OR material LIKE ?
               ORDER BY sku LIMIT 50""",
            (like, like, like, like),
        ).fetchall()
    )
    suppliers = rows_to_dicts(
        conn.execute(
            """SELECT id, name, role, location, region_focus FROM suppliers
               WHERE id LIKE ? OR name LIKE ? OR role LIKE ? OR location LIKE ?
               ORDER BY id LIMIT 50""",
            (like, like, like, like),
        ).fetchall()
    )
    conn.close()
    return {"products": products, "suppliers": suppliers}


_SQL_OK = re.compile(r"^\s*(SELECT|WITH|PRAGMA|EXPLAIN)\b", re.I)
_SQL_FORBIDDEN = re.compile(r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|ATTACH|DETACH|REPLACE)\b", re.I)


def tool_db_sql(args: dict) -> dict:
    sql = args.get("sql") or ""
    if not sql:
        raise ValueError("sql required")
    if not _SQL_OK.match(sql) or _SQL_FORBIDDEN.search(sql):
        raise ValueError("only read-only SELECT/PRAGMA/EXPLAIN allowed")
    conn = connect()
    try:
        if not re.search(r"\bLIMIT\b", sql, re.I):
            sql = sql.rstrip().rstrip(";") + " LIMIT 500"
        cur = conn.execute(sql)
        cols = [d[0] for d in cur.description] if cur.description else []
        data = rows_to_dicts(cur.fetchall()[:500])
    finally:
        conn.close()
    return {"columns": cols, "rows": data, "count": len(data)}


def tool_assets_search(args: dict) -> dict:
    conn = connect()
    q = args.get("q") or args.get("query") or ""
    where = []
    params: list[Any] = []
    if q:
        like = f"%{q}%"
        where.append(
            "(agent_blurb LIKE ? OR agent_keywords LIKE ? OR alt_text LIKE ? OR asset_key LIKE ? OR sku LIKE ?)"
        )
        params.extend([like, like, like, like, like])
    for col, key in (
        ("role", "role"),
        ("product_family", "product_family"),
        ("scene", "scene"),
        ("mood", "mood"),
        ("sku", "sku"),
        ("source", "source"),
    ):
        if args.get(key):
            where.append(f"{col} = ?")
            params.append(args[key])
    if args.get("channel"):
        ch = args["channel"]
        where.append("suitability LIKE ?")
        params.append(f'%"{ch}"%')
    sql = "SELECT * FROM v_asset_catalog"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY role='hero' DESC, confidence='high' DESC, id LIMIT ?"
    params.append(int(args.get("limit", 20)))
    out = rows_to_dicts(conn.execute(sql, params).fetchall())
    conn.close()
    return {"assets": out, "count": len(out)}


def tool_assets_pick(args: dict) -> dict:
    sku = args.get("sku") or args.get("product_sku")
    channel = (args.get("channel") or "etsy").lower()
    conn = connect()
    if not sku:
        raise ValueError("sku required")
    score_col = "etsy_score" if channel in ("etsy", "shopify") else "pinterest_score"
    sql = f"""
        SELECT * FROM v_asset_pick
        WHERE sku = ?
        ORDER BY {score_col} DESC, role='hero' DESC
        LIMIT ?
    """
    out = rows_to_dicts(conn.execute(sql, (sku, int(args.get("limit", 5)))).fetchall())
    conn.close()
    return {"sku": sku, "channel": channel, "picks": out, "count": len(out)}


def tool_assets_get(args: dict) -> dict:
    key = args.get("asset_key") or args.get("key")
    if not key:
        raise ValueError("asset_key required")
    conn = connect()
    row = conn.execute("SELECT * FROM v_asset_catalog WHERE asset_key = ?", (key,)).fetchone()
    conn.close()
    if not row:
        raise ValueError(f"asset not found: {key}")
    return dict(row)


def tool_assets_bulk_meta(args: dict) -> dict:
    sku = args.get("sku")
    conn = connect()
    if sku:
        out = rows_to_dicts(
            conn.execute(
                "SELECT * FROM v_asset_catalog WHERE sku = ? ORDER BY role, id", (sku,)
            ).fetchall()
        )
    else:
        out = rows_to_dicts(
            conn.execute(
                "SELECT product_family, role, COUNT(*) n FROM v_asset_catalog GROUP BY 1,2 ORDER BY 1,2"
            ).fetchall()
        )
    conn.close()
    return {"rows": out, "count": len(out)}


TOOLS: dict[str, dict] = {
    "db_stats": {
        "description": "Row counts for all DB tables",
        "inputSchema": {"type": "object", "properties": {}},
        "handler": tool_db_stats,
    },
    "db_list_suppliers": {
        "description": "Supplier directory with cost tiers and lead times",
        "inputSchema": {
            "type": "object",
            "properties": {"region_focus": {"type": "string"}},
        },
        "handler": tool_db_list_suppliers,
    },
    "db_list_products": {
        "description": "Products with primary supplier, unit cost, retail",
        "inputSchema": {
            "type": "object",
            "properties": {
                "section": {"type": "string"},
                "status": {"type": "string"},
                "supplier": {"type": "string"},
            },
        },
        "handler": tool_db_list_products,
    },
    "db_get_product": {
        "description": "Full product: suppliers, costs, retail, shipping, files, listings",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sku": {"type": "string"},
                "listing_id": {"type": "string"},
            },
        },
        "handler": tool_db_get_product,
    },
    "db_fulfilment_matrix": {
        "description": "Product × supplier × destination lead times / cost to user",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sku": {"type": "string"},
                "supplier_id": {"type": "string"},
            },
        },
        "handler": tool_db_fulfilment_matrix,
    },
    "db_list_etsy_drafts": {
        "description": "Etsy draft listings joined to products",
        "inputSchema": {"type": "object", "properties": {}},
        "handler": tool_db_list_etsy_drafts,
    },
    "db_open_quotes": {
        "description": "Open quote blockers (P0/P1)",
        "inputSchema": {"type": "object", "properties": {}},
        "handler": tool_db_open_quotes,
    },
    "db_search": {
        "description": "Search products and suppliers by keyword",
        "inputSchema": {
            "type": "object",
            "properties": {"q": {"type": "string"}, "query": {"type": "string"}},
        },
        "handler": tool_db_search,
    },
    "assets_search": {
        "description": "Search labelled assets by keyword/family/scene/channel without viewing images",
        "inputSchema": {
            "type": "object",
            "properties": {
                "q": {"type": "string"},
                "role": {"type": "string"},
                "product_family": {"type": "string"},
                "scene": {"type": "string"},
                "sku": {"type": "string"},
                "channel": {"type": "string"},
                "limit": {"type": "integer"},
            },
        },
        "handler": tool_assets_search,
    },
    "assets_pick": {
        "description": "Pick best assets for a SKU + channel (etsy/pinterest/shopify) by score",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sku": {"type": "string"},
                "channel": {"type": "string"},
                "limit": {"type": "integer"},
            },
            "required": ["sku"],
        },
        "handler": tool_assets_pick,
    },
    "assets_get": {
        "description": "Get full labels for one asset_key",
        "inputSchema": {
            "type": "object",
            "properties": {"asset_key": {"type": "string"}, "key": {"type": "string"}},
        },
        "handler": tool_assets_get,
    },
    "assets_bulk_meta": {
        "description": "All assets for a SKU, or counts by family/role",
        "inputSchema": {
            "type": "object",
            "properties": {"sku": {"type": "string"}},
        },
        "handler": tool_assets_bulk_meta,
    },
    "db_sql": {
        "description": "Read-only SQL against the canonical DB",
        "inputSchema": {
            "type": "object",
            "properties": {"sql": {"type": "string"}},
            "required": ["sql"],
        },
        "handler": tool_db_sql,
    },
}


PROTOCOL_VERSION = "2024-11-05"
SERVER_INFO = {"name": "oddhobbies-db", "version": "1.0.0"}


def handle(req: dict) -> dict:
    method = req.get("method")
    req_id = req.get("id")
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {}},
                "serverInfo": SERVER_INFO,
            },
        }
    if method == "notifications/initialized":
        return {}
    if method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}
    if method == "tools/list":
        tools = [
            {"name": n, "description": t["description"], "inputSchema": t["inputSchema"]}
            for n, t in TOOLS.items()
        ]
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": tools}}
    if method == "tools/call":
        params = req.get("params") or {}
        name = params.get("name")
        arguments = params.get("arguments") or {}
        if name not in TOOLS:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"unknown tool: {name}"},
            }
        try:
            result = TOOLS[name]["handler"](arguments)
            text = json.dumps(result, indent=2, default=str)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": text}],
                    "isError": False,
                },
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": f"Error: {e}"}],
                    "isError": True,
                },
            }
    if method == "shutdown":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}
    if req_id is None:
        return {}
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"method not found: {method}"},
    }


def main() -> None:
    # JSON-RPC over stdio: one JSON object per line
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        resp = handle(req)
        if resp:
            sys.stdout.write(json.dumps(resp, separators=(",", ":")) + "\n")
            sys.stdout.flush()
        if req.get("method") == "shutdown":
            break


if __name__ == "__main__":
    import sys

    main()

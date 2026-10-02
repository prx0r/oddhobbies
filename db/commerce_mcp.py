#!/usr/bin/env python3
"""Multi-store ops MCP server (stdio JSON-RPC).

Tools are store-scoped. Consumer agents should use store_agent_catalog /
store_product_public only — never unit costs or vault paths.

Usage: python3 db/commerce_mcp.py
"""

from __future__ import annotations

import json
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parent / "commerce.db"

_SQL_OK = re.compile(r"^\s*(SELECT|WITH|PRAGMA|EXPLAIN)\b", re.I)
_SQL_FORBIDDEN = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|ATTACH|DETACH|REPLACE)\b", re.I
)


def connect() -> sqlite3.Connection:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"missing {DB_PATH} — run db/seed_store.py")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def rows_to_dicts(rows: list[sqlite3.Row]) -> list[dict[str, Any]]:
    return [dict(r) for r in rows]


def require_store(conn: sqlite3.Connection, store_id: str | None) -> str | None:
    if not store_id:
        return None
    row = conn.execute("SELECT id FROM stores WHERE id=?", (store_id,)).fetchone()
    if not row:
        raise ValueError(f"unknown store_id: {store_id}")
    return store_id


def tool_store_list(args: dict) -> dict:
    conn = connect()
    out = rows_to_dicts(conn.execute("SELECT * FROM v_stores ORDER BY id").fetchall())
    conn.close()
    return {"stores": out, "count": len(out)}


def tool_store_get(args: dict) -> dict:
    store_id = args.get("store_id")
    if not store_id:
        raise ValueError("store_id required")
    conn = connect()
    store = conn.execute(
        """SELECT s.*, b.name AS brand_name, b.thesis AS brand_thesis
           FROM stores s JOIN brands b ON b.id=s.brand_id WHERE s.id=?""",
        (store_id,),
    ).fetchone()
    if not store:
        conn.close()
        raise ValueError(f"unknown store: {store_id}")
    config = rows_to_dicts(
        conn.execute("SELECT key, value_json FROM store_config WHERE store_id=?", (store_id,)).fetchall()
    )
    channels = rows_to_dicts(
        conn.execute("SELECT * FROM channels WHERE store_id=?", (store_id,)).fetchall()
    )
    conn.close()
    out = dict(store)
    out["config"] = {c["key"]: json.loads(c["value_json"]) for c in config}
    out["channels"] = channels
    return out


def tool_store_products(args: dict) -> dict:
    store_id = require_store(connect(), args.get("store_id")) or args.get("store_id")
    if not store_id:
        raise ValueError("store_id required")
    conn = connect()
    q = [
        "SELECT p.*, rp.price AS retail_price, rp.currency AS retail_currency,",
        "ps.supplier_id AS primary_supplier, pc.unit_cost, pc.currency AS cost_currency",
        "FROM products p",
        "LEFT JOIN product_retail_prices rp ON rp.product_id=p.id AND rp.is_current=1 AND rp.channel='etsy' AND rp.tier_code IS NULL",
        "LEFT JOIN product_suppliers ps ON ps.product_id=p.id AND ps.role='primary'",
        "LEFT JOIN product_costs pc ON pc.product_id=p.id AND pc.is_current=1 AND pc.supplier_id=ps.supplier_id",
        "WHERE p.store_id=?",
    ]
    params: list[Any] = [store_id]
    if args.get("section"):
        q.append("AND p.section=?")
        params.append(args["section"])
    if args.get("status"):
        q.append("AND p.status=?")
        params.append(args["status"])
    if args.get("sku"):
        q.append("AND p.sku=?")
        params.append(args["sku"])
    q.append("ORDER BY p.section, p.sku")
    out = rows_to_dicts(conn.execute(" ".join(q), params).fetchall())
    conn.close()
    return {"store_id": store_id, "products": out, "count": len(out)}


def tool_store_product(args: dict) -> dict:
    store_id = args.get("store_id")
    sku = args.get("sku")
    if not store_id or not sku:
        raise ValueError("store_id and sku required")
    conn = connect()
    product = conn.execute(
        "SELECT * FROM products WHERE store_id=? AND sku=?", (store_id, sku)
    ).fetchone()
    if not product:
        conn.close()
        raise ValueError(f"product not found: {store_id}/{sku}")
    pid = product["id"]
    out = dict(product)
    out["suppliers"] = rows_to_dicts(
        conn.execute(
            """SELECT ps.role, ps.supplier_sku, s.id, s.name, s.location
               FROM product_suppliers ps JOIN suppliers s ON s.id=ps.supplier_id
               WHERE ps.product_id=?""",
            (pid,),
        ).fetchall()
    )
    out["costs"] = rows_to_dicts(
        conn.execute(
            """SELECT pc.*, s.name AS supplier_name FROM product_costs pc
               JOIN suppliers s ON s.id=pc.supplier_id
               WHERE pc.product_id=? AND pc.is_current=1""",
            (pid,),
        ).fetchall()
    )
    out["retail"] = rows_to_dicts(
        conn.execute(
            "SELECT * FROM product_retail_prices WHERE product_id=? AND is_current=1", (pid,)
        ).fetchall()
    )
    out["listings"] = rows_to_dicts(
        conn.execute("SELECT * FROM listings WHERE product_id=?", (pid,)).fetchall()
    )
    out["assets"] = rows_to_dicts(
        conn.execute(
            "SELECT asset_key, asset_type, role, path_or_url, alt_text, agent_blurb FROM assets WHERE product_id=?",
            (pid,),
        ).fetchall()
    )
    out["agent_catalog"] = rows_to_dicts(
        conn.execute("SELECT * FROM agent_catalog WHERE product_id=?", (pid,)).fetchall()
    )
    conn.close()
    return out


def tool_store_agent_catalog(args: dict) -> dict:
    """Consumer-facing catalog. No unit costs, no vault paths."""
    store_id = args.get("store_id")
    conn = connect()
    sql = "SELECT * FROM v_agent_catalog"
    params: list[Any] = []
    where = []
    if store_id:
        require_store(conn, store_id)
        where.append("store_id=?")
        params.append(store_id)
    if args.get("orderable_only"):
        where.append("is_orderable=1")
    if args.get("gift_for"):
        where.append("gift_occasions LIKE ?")
        params.append(f"%{args['gift_for']}%")
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY store_id, agent_sku"
    out = rows_to_dicts(conn.execute(sql, params).fetchall())
    conn.close()
    return {"catalog": out, "count": len(out)}


def tool_store_product_public(args: dict) -> dict:
    """Public product view for consumer agents."""
    store_id = args.get("store_id")
    agent_sku = args.get("agent_sku")
    if not store_id or not agent_sku:
        raise ValueError("store_id and agent_sku required")
    conn = connect()
    row = conn.execute(
        """SELECT ac.*, p.sku, p.section, p.title,
                  rp.price AS display_price, rp.currency AS display_currency,
                  s.store_name
           FROM agent_catalog ac
           JOIN products p ON p.id=ac.product_id
           JOIN stores s ON s.id=ac.store_id
           LEFT JOIN product_retail_prices rp
             ON rp.product_id=p.id AND rp.is_current=1 AND rp.channel='etsy' AND rp.tier_code IS NULL
           WHERE ac.store_id=? AND ac.agent_sku=?""",
        (store_id, agent_sku),
    ).fetchone()
    if not row:
        conn.close()
        raise ValueError(f"agent product not found: {store_id}/{agent_sku}")
    assets = rows_to_dicts(
        conn.execute(
            """SELECT asset_key, role, path_or_url, alt_text, agent_blurb
               FROM assets WHERE store_id=? AND sku=? AND channel_fit LIKE '%agent%'
               ORDER BY role='hero' DESC""",
            (store_id, row["sku"]),
        ).fetchall()
    )
    # if no agent-fit assets, return any for the sku
    if not assets:
        assets = rows_to_dicts(
            conn.execute(
                """SELECT asset_key, role, path_or_url, alt_text, agent_blurb
                   FROM assets WHERE store_id=? AND sku=? ORDER BY role='hero' DESC""",
                (store_id, row["sku"]),
            ).fetchall()
        )
    out = dict(row)
    out["assets"] = assets
    conn.close()
    return out


def tool_sales_summary(args: dict) -> dict:
    store_id = args.get("store_id")
    conn = connect()
    if store_id:
        require_store(conn, store_id)
    by_store = rows_to_dicts(
        conn.execute("SELECT * FROM v_sales_by_store").fetchall()
    )
    by_product = rows_to_dicts(
        conn.execute("SELECT * FROM v_sales_by_product").fetchall()
    )
    orders = []
    q = "SELECT * FROM orders"
    params: list[Any] = []
    if store_id:
        q += " WHERE store_id=?"
        params.append(store_id)
    q += " ORDER BY id DESC LIMIT 50"
    orders = rows_to_dicts(conn.execute(q, params).fetchall())
    conn.close()
    if store_id:
        by_store = [r for r in by_store if r.get("store_id") == store_id]
        by_product = [r for r in by_product if r.get("store_id") == store_id]
    return {
        "store_id": store_id,
        "by_store_channel": by_store,
        "by_product": by_product,
        "recent_orders": orders,
    }


def tool_sales_record(args: dict) -> dict:
    """Insert a manual order (ops use). Consumer agents must not call this."""
    store_id = args.get("store_id")
    channel = args.get("channel") or "manual"
    external_order_id = args.get("external_order_id") or f"manual-{store_id}"
    lines = args.get("lines") or []
    if not store_id or not lines:
        raise ValueError("store_id and lines[] required")
    conn = connect()
    require_store(conn, store_id)
    total = 0.0
    line_rows = []
    for ln in lines:
        sku = ln.get("sku")
        qty = int(ln.get("qty") or 1)
        unit = float(ln.get("unit_price") or 0)
        row = conn.execute(
            "SELECT id, title FROM products WHERE store_id=? AND sku=?", (store_id, sku)
        ).fetchone()
        if not row:
            conn.close()
            raise ValueError(f"unknown sku in store: {sku}")
        line_total = unit * qty
        total += line_total
        line_rows.append((row["id"], sku, qty, unit, line_total))
    cur = conn.execute(
        """INSERT INTO orders
           (store_id,channel,external_order_id,currency,total,status,placed_at,source)
           VALUES (?,?,?,?,?,?,datetime('now'),'manual')""",
        (store_id, channel, external_order_id, args.get("currency") or "USD", total, "paid"),
    )
    order_id = cur.lastrowid
    for pid, sku, qty, unit, line_total in line_rows:
        conn.execute(
            """INSERT INTO order_lines (order_id,product_id,sku,qty,unit_price,line_total)
               VALUES (?,?,?,?,?,?)""",
            (order_id, pid, sku, qty, unit, line_total),
        )
    conn.commit()
    conn.close()
    return {"order_id": order_id, "store_id": store_id, "total": total, "lines": len(line_rows)}


def tool_ads_readiness(args: dict) -> dict:
    store_id = args.get("store_id")
    conn = connect()
    if store_id:
        require_store(conn, store_id)
    q = "SELECT * FROM v_ad_readiness"
    params: list[Any] = []
    if store_id:
        q += " WHERE store_id=?"
        params.append(store_id)
    q += " ORDER BY store_id, sku"
    out = rows_to_dicts(conn.execute(q, params).fetchall())
    conn.close()
    return {"rows": out, "count": len(out)}


def tool_ads_campaign_upsert(args: dict) -> dict:
    store_id = args.get("store_id")
    name = args.get("name")
    channel = args.get("channel") or "pinterest"
    if not store_id or not name:
        raise ValueError("store_id and name required")
    conn = connect()
    require_store(conn, store_id)
    conn.execute(
        """INSERT INTO ad_campaigns (store_id,channel,name,objective,status,budget_daily,currency,target_audience,notes)
           VALUES (?,?,?,?,?,?,?,?,?)""",
        (
            store_id,
            channel,
            name,
            args.get("objective"),
            args.get("status") or "draft",
            args.get("budget_daily"),
            args.get("currency"),
            args.get("target_audience"),
            args.get("notes"),
        ),
    )
    conn.commit()
    cid = conn.execute(
        "SELECT id FROM ad_campaigns WHERE store_id=? AND name=? ORDER BY id DESC LIMIT 1",
        (store_id, name),
    ).fetchone()[0]
    conn.close()
    return {"campaign_id": cid, "store_id": store_id, "name": name}


def tool_ads_creative_add(args: dict) -> dict:
    campaign_id = args.get("campaign_id")
    if not campaign_id:
        raise ValueError("campaign_id required")
    conn = connect()
    camp = conn.execute("SELECT * FROM ad_campaigns WHERE id=?", (campaign_id,)).fetchone()
    if not camp:
        conn.close()
        raise ValueError(f"campaign not found: {campaign_id}")
    store_id = camp["store_id"]
    product_id = None
    listing_id = None
    asset_id = None
    if args.get("sku"):
        prod = conn.execute(
            "SELECT id FROM products WHERE store_id=? AND sku=?", (store_id, args["sku"])
        ).fetchone()
        if not prod:
            conn.close()
            raise ValueError(f"unknown sku: {args['sku']}")
        product_id = prod["id"]
    if args.get("listing_id"):
        listing_id = args["listing_id"]
    if args.get("asset_key"):
        asset = conn.execute(
            "SELECT id FROM assets WHERE store_id=? AND asset_key=?", (store_id, args["asset_key"])
        ).fetchone()
        if asset:
            asset_id = asset["id"]
    cur = conn.execute(
        """INSERT INTO ad_creatives
           (campaign_id,store_id,product_id,asset_id,listing_id,name,headline,body,destination_url,status,notes)
           VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        (
            campaign_id,
            store_id,
            product_id,
            asset_id,
            listing_id,
            args.get("name"),
            args.get("headline"),
            args.get("body"),
            args.get("destination_url"),
            args.get("status") or "draft",
            args.get("notes"),
        ),
    )
    conn.commit()
    conn.close()
    return {"creative_id": cur.lastrowid, "campaign_id": campaign_id, "store_id": store_id}


def tool_assets_search(args: dict) -> dict:
    conn = connect()
    where = []
    params: list[Any] = []
    if args.get("store_id"):
        require_store(conn, args["store_id"])
        where.append("store_id=?")
        params.append(args["store_id"])
    if args.get("sku"):
        where.append("sku=?")
        params.append(args["sku"])
    q = args.get("q") or args.get("query")
    if q:
        like = f"%{q}%"
        where.append("(asset_key LIKE ? OR agent_blurb LIKE ? OR alt_text LIKE ? OR agent_keywords LIKE ?)")
        params.extend([like, like, like, like])
    if args.get("role"):
        where.append("role=?")
        params.append(args["role"])
    if args.get("channel"):
        where.append("channel_fit LIKE ?")
        params.append(f'%"{args["channel"]}"%')
    sql = "SELECT * FROM v_asset_catalog"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY role='hero' DESC, id LIMIT ?"
    params.append(int(args.get("limit", 20)))
    out = rows_to_dicts(conn.execute(sql, params).fetchall())
    conn.close()
    return {"assets": out, "count": len(out)}


def tool_assets_pick(args: dict) -> dict:
    store_id = args.get("store_id")
    sku = args.get("sku") or args.get("product_sku")
    channel = (args.get("channel") or "etsy").lower()
    if not store_id or not sku:
        raise ValueError("store_id and sku required")
    conn = connect()
    require_store(conn, store_id)
    score = "etsy_score" if channel in ("etsy", "shopify") else "pinterest_score"
    # v_asset_pick may not exist in commerce schema — use simple rank
    out = rows_to_dicts(
        conn.execute(
            """SELECT * FROM assets WHERE store_id=? AND sku=?
               ORDER BY role='hero' DESC, id LIMIT ?""",
            (store_id, sku, int(args.get("limit", 5))),
        ).fetchall()
    )
    conn.close()
    return {"store_id": store_id, "sku": sku, "channel": channel, "picks": out, "count": len(out)}


def tool_graph_export(args: dict) -> dict:
    """Trigger in-process export path pointer (agent should run export_graph.py or read graph/)."""
    store_id = args.get("store_id")
    path = Path(__file__).resolve().parent.parent / "graph" / f"{store_id or 'index'}.json"
    if not path.exists():
        return {
            "ok": False,
            "hint": "run: python3 db/export_graph.py --store <store_id>",
            "expected_path": str(path),
        }
    data = json.loads(path.read_text())
    return {"ok": True, "path": str(path), "counts": data.get("counts")}


def tool_db_sql(args: dict) -> dict:
    sql = args.get("sql") or ""
    if not sql:
        raise ValueError("sql required")
    if not _SQL_OK.match(sql) or _SQL_FORBIDDEN.search(sql):
        raise ValueError("only read-only SELECT/PRAGMA/EXPLAIN allowed")
    if not re.search(r"\bLIMIT\b", sql, re.I):
        sql = sql.rstrip().rstrip(";") + " LIMIT 500"
    conn = connect()
    try:
        cur = conn.execute(sql)
        cols = [d[0] for d in cur.description] if cur.description else []
        data = rows_to_dicts(cur.fetchall()[:500])
    finally:
        conn.close()
    return {"columns": cols, "rows": data, "count": len(data)}


TOOLS: dict[str, dict] = {
    "store_list": {
        "description": "List all commerce stores with brand + counts",
        "inputSchema": {"type": "object", "properties": {}},
        "handler": tool_store_list,
    },
    "store_get": {
        "description": "Full store config + channels",
        "inputSchema": {
            "type": "object",
            "properties": {"store_id": {"type": "string"}},
            "required": ["store_id"],
        },
        "handler": tool_store_get,
    },
    "store_products": {
        "description": "Products for one store (ops — includes costs)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string"},
                "section": {"type": "string"},
                "status": {"type": "string"},
                "sku": {"type": "string"},
            },
            "required": ["store_id"],
        },
        "handler": tool_store_products,
    },
    "store_product": {
        "description": "One product full graph (costs, listings, assets)",
        "inputSchema": {
            "type": "object",
            "properties": {"store_id": {"type": "string"}, "sku": {"type": "string"}},
            "required": ["store_id", "sku"],
        },
        "handler": tool_store_product,
    },
    "store_agent_catalog": {
        "description": "Consumer-facing catalog (no costs/secrets)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string"},
                "orderable_only": {"type": "boolean"},
                "gift_for": {"type": "string"},
            },
        },
        "handler": tool_store_agent_catalog,
    },
    "store_product_public": {
        "description": "Public product view for consumer agents",
        "inputSchema": {
            "type": "object",
            "properties": {"store_id": {"type": "string"}, "agent_sku": {"type": "string"}},
            "required": ["store_id", "agent_sku"],
        },
        "handler": tool_store_product_public,
    },
    "sales_summary": {
        "description": "Sales by store/channel/product + recent orders",
        "inputSchema": {
            "type": "object",
            "properties": {"store_id": {"type": "string"}},
        },
        "handler": tool_sales_summary,
    },
    "sales_record": {
        "description": "Record a manual order (ops only)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string"},
                "channel": {"type": "string"},
                "external_order_id": {"type": "string"},
                "currency": {"type": "string"},
                "lines": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "sku": {"type": "string"},
                            "qty": {"type": "integer"},
                            "unit_price": {"type": "number"},
                        },
                        "required": ["sku"],
                    },
                },
            },
            "required": ["store_id", "lines"],
        },
        "handler": tool_sales_record,
    },
    "ads_readiness": {
        "description": "Which products can run ads (price + assets + live listing)",
        "inputSchema": {
            "type": "object",
            "properties": {"store_id": {"type": "string"}},
        },
        "handler": tool_ads_readiness,
    },
    "ads_campaign_upsert": {
        "description": "Create an ad campaign draft for a store",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string"},
                "name": {"type": "string"},
                "channel": {"type": "string"},
                "objective": {"type": "string"},
                "budget_daily": {"type": "number"},
                "currency": {"type": "string"},
            },
            "required": ["store_id", "name"],
        },
        "handler": tool_ads_campaign_upsert,
    },
    "ads_creative_add": {
        "description": "Attach a creative (product/asset/copy) to a campaign",
        "inputSchema": {
            "type": "object",
            "properties": {
                "campaign_id": {"type": "integer"},
                "sku": {"type": "string"},
                "asset_key": {"type": "string"},
                "name": {"type": "string"},
                "headline": {"type": "string"},
                "body": {"type": "string"},
                "destination_url": {"type": "string"},
            },
            "required": ["campaign_id"],
        },
        "handler": tool_ads_creative_add,
    },
    "assets_search": {
        "description": "Search labelled assets (filter by store_id/sku/role/channel)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string"},
                "sku": {"type": "string"},
                "q": {"type": "string"},
                "role": {"type": "string"},
                "channel": {"type": "string"},
                "limit": {"type": "integer"},
            },
        },
        "handler": tool_assets_search,
    },
    "assets_pick": {
        "description": "Pick assets for a product SKU on a channel",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string"},
                "sku": {"type": "string"},
                "channel": {"type": "string"},
                "limit": {"type": "integer"},
            },
            "required": ["store_id", "sku"],
        },
        "handler": tool_assets_pick,
    },
    "graph_export": {
        "description": "Check graph export status for a store",
        "inputSchema": {
            "type": "object",
            "properties": {"store_id": {"type": "string"}},
        },
        "handler": tool_graph_export,
    },
    "db_sql": {
        "description": "Read-only SQL on commerce.db (LIMIT auto-applied)",
        "inputSchema": {
            "type": "object",
            "properties": {"sql": {"type": "string"}},
            "required": ["sql"],
        },
        "handler": tool_db_sql,
    },
}


def _read_message(stream) -> dict | None:
    line = stream.readline()
    if not line:
        return None
    line = line.strip()
    if not line:
        return {}
    return json.loads(line)


def _write(stream, obj: dict) -> None:
    stream.write(json.dumps(obj, ensure_ascii=False) + "\n")
    stream.flush()


def main() -> int:
    stdin, stdout = sys.stdin, sys.stdout
    while True:
        msg = _read_message(stdin)
        if msg is None:
            break
        if not msg:
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
                        "serverInfo": {"name": "commerce-mcp", "version": "1.0.0"},
                    },
                },
            )
        elif method == "tools/list":
            tools = [
                {"name": k, "description": v["description"], "inputSchema": v["inputSchema"]}
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
                            "isError": False,
                        },
                    },
                )
            except Exception as e:  # noqa: BLE001 — surface to agent
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

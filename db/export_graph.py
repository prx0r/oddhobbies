#!/usr/bin/env python3
"""Export a store graph JSON for other systems (influence, agents, dashboards).

Usage:
  python3 db/export_graph.py
  python3 db/export_graph.py --store pogpet
  python3 db/export_graph.py --store ochema --out graph/ochema.json
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "db" / "commerce.db"
GRAPH_DIR = ROOT / "graph"


def connect() -> sqlite3.Connection:
    if not DB_PATH.exists():
        raise SystemExit(f"missing {DB_PATH} — run db/seed_store.py first")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def rows(conn: sqlite3.Connection, sql: str, params=()) -> list[dict]:
    return [dict(r) for r in conn.execute(sql, params).fetchall()]


def export_store(conn: sqlite3.Connection, store_id: str) -> dict:
    store = conn.execute(
        """SELECT s.*, b.name AS brand_name, b.thesis AS brand_thesis
           FROM stores s JOIN brands b ON b.id=s.brand_id WHERE s.id=?""",
        (store_id,),
    ).fetchone()
    if not store:
        raise SystemExit(f"unknown store: {store_id}")
    store = dict(store)

    products = rows(
        conn,
        """SELECT p.id AS product_row_id, p.sku, p.title, p.section, p.make, p.status,
                  p.agent_sku, p.priority,
                  rp.price AS retail_price, rp.currency AS retail_currency,
                  pc.unit_cost, pc.currency AS cost_currency
           FROM products p
           LEFT JOIN product_retail_prices rp
             ON rp.product_id=p.id AND rp.is_current=1 AND rp.channel='etsy' AND rp.tier_code IS NULL
           LEFT JOIN product_suppliers ps ON ps.product_id=p.id AND ps.role='primary'
           LEFT JOIN product_costs pc
             ON pc.product_id=p.id AND pc.is_current=1 AND pc.supplier_id=ps.supplier_id
           WHERE p.store_id=?
           ORDER BY p.section, p.sku""",
        (store_id,),
    )
    listings = rows(
        conn,
        """SELECT id, product_id, channel, external_id, title, state, channel_price, channel_currency
           FROM listings WHERE store_id=? ORDER BY channel, title""",
        (store_id,),
    )
    assets = rows(
        conn,
        """SELECT id, asset_key, sku, asset_type, role, path_or_url, alt_text, agent_blurb, channel_fit
           FROM assets WHERE store_id=? ORDER BY sku, role""",
        (store_id,),
    )
    agent_catalog = rows(
        conn,
        """SELECT agent_sku, display_name, summary, price_tier, gift_occasions,
                  fulfilment_blurb, is_orderable, product_id
           FROM agent_catalog WHERE store_id=? ORDER BY agent_sku""",
        (store_id,),
    )
    channels = rows(
        conn,
        """SELECT id, channel, shop_name, external_id, domain, currency, status
           FROM channels WHERE store_id=? ORDER BY channel""",
        (store_id,),
    )
    sales = rows(
        conn,
        """SELECT channel, status, COUNT(*) AS orders, SUM(total) AS revenue, currency
           FROM orders WHERE store_id=? GROUP BY channel, status, currency""",
        (store_id,),
    )
    ad_ready = rows(
        conn,
        """SELECT sku, title, status, retail_price, asset_count, creative_count, live_listing_id
           FROM v_ad_readiness WHERE store_id=? ORDER BY sku""",
        (store_id,),
    )

    # product_id mapping for edges (rowid vs graph id)
    product_by_row = {p["product_row_id"]: p for p in products}
    product_by_sku = {p["sku"]: p for p in products}

    nodes = []
    edges = []

    nodes.append(
        {
            "id": store_id,
            "type": "store",
            "label": store["store_name"],
            "data": {
                "brand_id": store["brand_id"],
                "brand_name": store["brand_name"],
                "currency": store["currency"],
                "status": store["status"],
                "thesis": store.get("brand_thesis") or store.get("thesis"),
            },
        }
    )
    edges.append({"from": store["brand_id"], "to": store_id, "rel": "operates"})

    if store.get("brand_id") not in {n["id"] for n in nodes}:
        nodes.append(
            {
                "id": store["brand_id"],
                "type": "brand",
                "label": store["brand_name"],
                "data": {"thesis": store.get("brand_thesis")},
            }
        )

    for ch in channels:
        nodes.append(
            {
                "id": ch["id"],
                "type": "channel",
                "label": ch.get("shop_name") or ch["channel"],
                "data": ch,
            }
        )
        edges.append({"from": store_id, "to": ch["id"], "rel": "channel"})

    for p in products:
        pid = f"{store_id}:product:{p['sku']}"
        nodes.append({"id": pid, "type": "product", "label": p["title"], "data": p})
        edges.append({"from": store_id, "to": pid, "rel": "sells"})
        if p.get("agent_sku"):
            aid = f"{store_id}:agent:{p['agent_sku']}"
            nodes.append(
                {
                    "id": aid,
                    "type": "agent_sku",
                    "label": p["agent_sku"],
                    "data": {"agent_sku": p["agent_sku"]},
                }
            )
            edges.append({"from": pid, "to": aid, "rel": "exposed_as"})

    for lst in listings:
        lid = f"{store_id}:listing:{lst['channel']}:{lst.get('external_id') or lst['id']}"
        nodes.append({"id": lid, "type": "listing", "label": lst.get("title") or lid, "data": lst})
        # attach to product by row
        prod = product_by_row.get(lst.get("product_id"))
        if prod:
            edges.append(
                {
                    "from": f"{store_id}:product:{prod['sku']}",
                    "to": lid,
                    "rel": "listed_as",
                }
            )

    for a in assets:
        aid = f"{store_id}:asset:{a['asset_key']}"
        nodes.append({"id": aid, "type": "asset", "label": a["asset_key"], "data": a})
        if a.get("sku") and a["sku"] in product_by_sku:
            edges.append(
                {
                    "from": f"{store_id}:product:{a['sku']}",
                    "to": aid,
                    "rel": "has_image",
                }
            )

    for row in agent_catalog:
        if not row.get("product_id"):
            continue
        prod = product_by_row.get(row["product_id"])
        if not prod:
            continue
        # already have agent node via product.agent_sku; ensure edge from catalog
        aid = f"{store_id}:agent:{row['agent_sku']}"
        if not any(n["id"] == aid for n in nodes):
            nodes.append(
                {
                    "id": aid,
                    "type": "agent_sku",
                    "label": row["agent_sku"],
                    "data": row,
                }
            )
        edges.append(
            {
                "from": f"{store_id}:product:{prod['sku']}",
                "to": aid,
                "rel": "exposed_as",
            }
        )

    # de-dupe edges
    seen = set()
    deduped = []
    for e in edges:
        key = (e["from"], e["to"], e["rel"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(e)

    graph = {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "store_id": store_id,
        "store": {
            "id": store["id"],
            "name": store["store_name"],
            "brand_id": store["brand_id"],
            "brand_name": store["brand_name"],
            "currency": store["currency"],
            "status": store["status"],
            "pack_path": store.get("pack_path"),
            "r2_prefix": store.get("r2_prefix"),
        },
        "counts": {
            "products": len(products),
            "listings": len(listings),
            "assets": len(assets),
            "agent_catalog": len(agent_catalog),
            "channels": len(channels),
            "nodes": len(nodes),
            "edges": len(deduped),
        },
        "channels": channels,
        "products": products,
        "listings": listings,
        "assets": assets,
        "agent_catalog": agent_catalog,
        "sales_summary": sales,
        "ad_readiness": ad_ready,
        "nodes": nodes,
        "edges": deduped,
    }
    return graph


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", action="append", dest="stores")
    ap.add_argument("--out", type=str)
    args = ap.parse_args()
    GRAPH_DIR.mkdir(parents=True, exist_ok=True)
    conn = connect()
    store_ids = args.stores or [
        r["id"] for r in conn.execute("SELECT id FROM stores ORDER BY id")
    ]
    for store_id in store_ids:
        graph = export_store(conn, store_id)
        out = Path(args.out) if args.out else GRAPH_DIR / f"{store_id}.json"
        if args.out and len(store_ids) > 1:
            out = GRAPH_DIR / f"{store_id}.json"
        out.write_text(json.dumps(graph, indent=2, ensure_ascii=False) + "\n")
        conn.execute(
            """INSERT INTO graph_exports (store_id,path,node_count,edge_count)
               VALUES (?,?,?,?)""",
            (store_id, str(out.relative_to(ROOT)), graph["counts"]["nodes"], graph["counts"]["edges"]),
        )
        print(f"wrote {out} nodes={graph['counts']['nodes']} edges={graph['counts']['edges']}")
    conn.commit()
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

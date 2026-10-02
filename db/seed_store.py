#!/usr/bin/env python3
"""Seed multi-store commerce.db from stores/<id>/ packs.

Usage:
  python3 db/seed_store.py                 # all stores
  python3 db/seed_store.py --store pogpet  # one store
  python3 db/seed_store.py --reset         # rebuild DB from schema first

Source of truth for authoring: stores/<id>/store.json + stores/<id>/listings/*.json
Runtime DB: db/commerce.db (gitignored)
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STORES = ROOT / "stores"
SCHEMA = ROOT / "db" / "schema_commerce.sql"
DB_PATH = ROOT / "db" / "commerce.db"

# Shared suppliers (catalog, not secrets). Costs stay on products.
SUPPLIERS = [
    ("MAKR3D", "Makr3D (Yorkshire3D Ltd)", "primary_3d_uk", "Yorkshire, UK", "UK", "native", "yes", "https://makr3d.example", "GBP small £1.29 / mid £2.50 / large £7.60"),
    ("PRINTIE", "Printie", "primary_3d_us", "US", "US", "yes", "yes", None, "US 3D print farm"),
    ("PRODIGI", "Prodigi", "flat_print", "Global labs", "GLOBAL", "native", "native", None, "POD cards/stickers/tags"),
    ("KUNAKI", "Kunaki", "media_us", "US", "US", "api", "none", None, "CD/DVD POD"),
    ("DISKCR", "DiskCrafters", "media_uk", "UK", "UK", "none", "none", None, "UK premium CD"),
    ("PERSONALISED_PLAYING_CARDS_UK", "PersonalisedPlayingCards.com", "cards_uk", "UK", "UK", "none", "none", None, "Card decks"),
    ("MAKE_PLAYING_CARDS", "MakePlayingCards (MPC)", "cards_global", "Global", "GLOBAL", "api", "none", None, "Card decks"),
    ("INGRAMSPARK", "IngramSpark", "books", "Global", "GLOBAL", "none", "none", None, "Book print"),
    ("QINPRINTING", "QinPrinting", "tarot_print", "CN", "ROW", "none", "none", None, "Tarot/book MOQ"),
    ("SELF", "Self-fulfilled / digital", "self", "Operator", "GLOBAL", "n/a", "n/a", None, "Digital + packed kits"),
]

SUPPLIER_LEADS = {
    "MAKR3D": [("UK", 2, 5), ("EU", 4, 9), ("US", 6, 16), ("AU", 8, 16)],
    "PRINTIE": [("US", 6, 14), ("UK", 8, 18)],
    "PRODIGI": [("UK", 2, 5), ("US", 3, 7), ("EU", 3, 8), ("AU", 5, 12)],
    "KUNAKI": [("US", 4, 8), ("UK", 8, 22), ("ROW", 8, 22)],
    "DISKCR": [("UK", 3, 7)],
    "SELF": [("GLOBAL", 0, 3)],
}

DECISIONS = [
    ("oddhobb", "commerce_core", "Multi-store commerce.db is source of truth", "Packs in stores/<id>/ seed commerce.db", "2026-10-02", "docs/commerce/COMMERCE-GRAPH.md"),
    ("oddhobb", "supplier_us_3d", "Printie", "US facility, Etsy, qty1", "2026-10-01", "US-3D-SUPPLIER.md"),
    ("oddhobb", "supplier_uk_3d", "Makr3D", "UK farm, native Etsy", "2026-10-01", "US-3D-SUPPLIER.md"),
    ("oddhobb", "positioning", "3D-first Game Night + Weddings/Couples", "Quirky hobby objects not POD mall", "2026-10-01", "FLAGSHIP-COSTS.md"),
    ("oddhobb", "prodigi_role", "Add-ons + albums/cards/pet tags only", "Not 3D", "2026-10-01", "PRODIGI-XMAS-OPS.md"),
    ("oddhobb", "brand_lock", "Public brand = OddHobb only", "No PogPet store naming", "2026-10-02", "stores/oddhobb/IDENTITY.md"),
    ("grimoirer", "store_bootstrap", "Grimoirer store pack created", "Grimoire packs + spell kits first SKUs", "2026-10-02", "stores/grimoirer/store.json"),
    ("grimoirer", "brand_lock", "Public brand = Grimoirer only", "No Ochemy store naming", "2026-10-02", "stores/grimoirer/IDENTITY.md"),
    ("stonedoorway", "store_bootstrap", "Placeholder store only", "Thesis undefined — no live SKUs", "2026-10-02", "stores/stonedoorway/README.md"),
]

OPEN_QUOTES = [
    ("oddhobb", "PRINTIE", "All-in quotes for 8 Game Night STLs (US ZIP)", "P0"),
    ("oddhobb", "MAKR3D", "Exact per-file quotes for 8 Game Night STLs", "P0"),
    ("oddhobb", "PRODIGI", "Pin SKUs: card, stickers, wrap, coaster, notebook, playing cards", "P0"),
    ("grimoirer", "SELF", "Confirm digital PDF production + delivery flow", "P0"),
    ("grimoirer", "QINPRINTING", "Tarot deck MOQ + unit cost if custom line later", "P2"),
]


def connect(reset: bool) -> sqlite3.Connection:
    if reset and DB_PATH.exists():
        DB_PATH.unlink()
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA.read_text())
    return conn


def ensure_supplier(conn: sqlite3.Connection, sid: str) -> None:
    row = conn.execute("SELECT id FROM suppliers WHERE id=?", (sid,)).fetchone()
    if row:
        return
    match = next((s for s in SUPPLIERS if s[0] == sid), None)
    if not match:
        conn.execute(
            "INSERT OR IGNORE INTO suppliers (id, name, role, region_focus, status) VALUES (?,?,?,?,?)",
            (sid, sid, None, None, "documented"),
        )
        return
    _id, name, role, location, region, etsy, shopify, url, note = match
    conn.execute(
        """INSERT OR IGNORE INTO suppliers
           (id,name,role,location,region_focus,url,etsy_integration,shopify_integration,notes,status)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (sid, name, role, location, region, url, etsy, shopify, note, "documented"),
    )
    for dest, dmin, dmax in SUPPLIER_LEADS.get(sid, []):
        conn.execute(
            """INSERT OR IGNORE INTO supplier_lead_times
               (supplier_id,destination_region,total_days_min,total_days_max)
               VALUES (?,?,?,?)""",
            (sid, dest, dmin, dmax),
        )


def upsert_brand_store(conn: sqlite3.Connection, store_json: dict) -> None:
    brand_id = store_json["brand_id"]
    store_id = store_json["store_id"]
    conn.execute(
        """INSERT OR REPLACE INTO brands (id,name,tagline,thesis,country,status,updated_at)
           VALUES (?,?,?,?,?, 'active', datetime('now'))""",
        (
            brand_id,
            store_json.get("store_name") or brand_id,
            store_json.get("brand_line"),
            store_json.get("thesis"),
            store_json.get("base_country", "GB"),
        ),
    )
    conn.execute(
        """INSERT OR REPLACE INTO stores
           (id,brand_id,store_name,currency,base_country,status,pack_path,r2_prefix,updated_at)
           VALUES (?,?,?,?,?,?,?,?, datetime('now'))""",
        (
            store_id,
            brand_id,
            store_json.get("store_name") or store_id,
            store_json.get("currency", "USD"),
            store_json.get("base_country", "GB"),
            store_json.get("status", "draft"),
            store_json.get("pack_path") or f"stores/{store_id}",
            store_json.get("r2_prefix") or f"commerce/stores/{store_id}",
        ),
    )
    config_keys = [
        "sections",
        "sections_forbidden",
        "style_lock",
        "pricing_policy",
        "fulfilment",
        "thesis",
        "brand_line",
        "channel_currencies",
        "related_repos",
        "blockers",
        "content_machine",
        "shopify_store_name",
    ]
    for key in config_keys:
        if key in store_json and store_json[key] is not None:
            conn.execute(
                """INSERT OR REPLACE INTO store_config (store_id,key,value_json)
                   VALUES (?,?,?)""",
                (store_id, key, json.dumps(store_json[key], ensure_ascii=False)),
            )
    for ch in store_json.get("channels") or []:
        cid = ch.get("channel_id") or f"{ch.get('channel')}:{store_id}"
        conn.execute(
            """INSERT OR REPLACE INTO channels
               (id,store_id,channel,shop_name,external_id,domain,currency,auth_ref,status,notes)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (
                cid,
                store_id,
                ch.get("channel"),
                ch.get("shop_name"),
                ch.get("external_id"),
                ch.get("domain"),
                ch.get("currency"),
                ch.get("auth_ref"),
                ch.get("status", "draft"),
                None,
            ),
        )


def pack_price(pack: dict, channel: str = "etsy") -> tuple[float, str]:
    store_ccy = pack.get("currency") or "USD"
    price = pack.get("price")
    if price is None:
        price = pack.get("price_usd") or 0.0
    return float(price), store_ccy


def insert_product(conn: sqlite3.Connection, store_id: str, pack: dict) -> int:
    sku = pack["sku"]
    agent_sku = pack.get("agent_sku") or sku.lower()
    section = pack.get("section") or pack.get("shop_section_target") or "Featured"
    title = pack.get("etsy_title") or pack.get("title") or sku
    cur = conn.execute(
        """INSERT INTO products
           (store_id,sku,title,short_name,section,make,material,size_class,
            dimensions_json,personalisation_json,description,demand_evidence,ip_notes,
            status,priority,agent_sku)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
           ON CONFLICT(store_id,sku) DO UPDATE SET
             title=excluded.title,
             section=excluded.section,
             make=excluded.make,
             description=excluded.description,
             ip_notes=excluded.ip_notes,
             status=excluded.status,
             agent_sku=excluded.agent_sku,
             updated_at=datetime('now')""",
        (
            store_id,
            sku,
            title,
            pack.get("short_name"),
            section,
            pack.get("make") or "digital",
            pack.get("material"),
            pack.get("size_class"),
            json.dumps(pack.get("dimensions")) if pack.get("dimensions") else None,
            json.dumps(pack.get("personalisation"), ensure_ascii=False)
            if pack.get("personalisation")
            else None,
            pack.get("description"),
            pack.get("demand_evidence"),
            pack.get("ip_notes"),
            pack.get("state") or pack.get("status") or "draft",
            pack.get("priority"),
            agent_sku,
        ),
    )
    product_id = cur.lastrowid or conn.execute(
        "SELECT id FROM products WHERE store_id=? AND sku=?", (store_id, sku)
    ).fetchone()[0]

    # suppliers
    for role, key in (("primary", "supplier_primary"), ("alt", "supplier_alt")):
        sid = pack.get(key)
        if not sid:
            continue
        ensure_supplier(conn, sid)
        conn.execute(
            """INSERT OR IGNORE INTO product_suppliers (product_id,supplier_id,role,supplier_sku)
               VALUES (?,?,?,?)""",
            (product_id, sid, role, pack.get("supplier_sku")),
        )

    # costs
    unit_cost = pack.get("unit_cost")
    if unit_cost is not None and str(unit_cost).strip() != "":
        try:
            uc = float(unit_cost)
        except (TypeError, ValueError):
            uc = None
        if uc is not None:
            sid = pack.get("supplier_primary") or "SELF"
            ensure_supplier(conn, sid)
            conn.execute(
                """INSERT INTO product_costs
                   (product_id,supplier_id,currency,unit_cost,cost_includes,source,source_note,is_current)
                   VALUES (?,?,?,?,?,?,?,1)""",
                (
                    product_id,
                    sid,
                    pack.get("cost_currency") or "USD",
                    uc,
                    pack.get("cost_includes"),
                    pack.get("cost_source") or "estimate",
                    pack.get("cost_note") or pack.get("unit_cost_note"),
                ),
            )

    # retail
    price, ccy = pack_price(pack)
    conn.execute(
        """INSERT OR REPLACE INTO product_retail_prices
           (product_id,channel,currency,price,is_current)
           VALUES (?, 'etsy', ?, ?, 1)""",
        (product_id, ccy, price),
    )
    # optional per-channel price override in pack
    for ch in ("shopify", "pinterest", "wholesale"):
        p = pack.get(f"price_{ch}") or pack.get("prices", {}).get(ch)
        if p is not None:
            conn.execute(
                """INSERT OR REPLACE INTO product_retail_prices
                   (product_id,channel,currency,price,is_current)
                   VALUES (?,?,?,?,1)""",
                (product_id, ch, ccy, float(p)),
            )

    # agent catalog
    ac = pack.get("agent_catalog") or {}
    if ac or pack.get("agent_sku"):
        conn.execute(
            """INSERT OR REPLACE INTO agent_catalog
               (store_id,product_id,agent_sku,display_name,summary,how_it_works,
                personalisation_schema_json,price_tier,gift_occasions,fulfilment_blurb,
                is_orderable,is_customisable)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                store_id,
                product_id,
                agent_sku,
                ac.get("display_name") or pack.get("short_name") or title,
                ac.get("summary") or (pack.get("description") or "")[:240],
                ac.get("how_it_works"),
                json.dumps(ac.get("personalisation_schema")) if ac.get("personalisation_schema") else pack.get("personalisation_json"),
                ac.get("price_tier"),
                ac.get("gift_occasions") or pack.get("gift_occasions"),
                ac.get("fulfilment_blurb") or pack.get("fulfilment_blurb"),
                int(ac.get("is_orderable", 0)),
                int(ac.get("is_customisable", 1)),
            ),
        )

    # personalisation questions
    for q in pack.get("personalisation") or []:
        qkey = re.sub(r"[^a-z0-9]+", "_", (q.get("question_text") or "q").lower()).strip("_")
        conn.execute(
            """INSERT OR IGNORE INTO personalisation_questions
               (product_id,question_key,question_text,question_type,required,max_chars,max_files,instructions)
               VALUES (?,?,?,?,?,?,?,?)""",
            (
                product_id,
                qkey,
                (q.get("question_text") or "")[:45],
                q.get("question_type") or "text_input",
                int(q.get("required", 0)),
                int(q.get("max_chars") or 1024),
                int(q.get("max_files") or 2),
                q.get("instructions"),
            ),
        )

    # listing row for known external ids
    etsy_id = pack.get("etsy_listing_id") or pack.get("listing_id")
    shopify_id = pack.get("shopify_product_id")
    if etsy_id:
        conn.execute(
            """INSERT OR REPLACE INTO listings
               (product_id,store_id,channel,external_id,title,state,channel_price,channel_currency,tags,
                personalisation_json,is_personalizable)
               VALUES (?, ?, 'etsy', ?, ?, ?, ?, ?, ?, ?, 1)""",
            (
                product_id,
                store_id,
                str(etsy_id),
                title,
                pack.get("state") or "draft",
                price,
                ccy,
                json.dumps(pack.get("tags") or [], ensure_ascii=False),
                json.dumps(pack.get("personalisation") or [], ensure_ascii=False),
            ),
        )
    if shopify_id:
        # channel row
        ch_row = conn.execute(
            "SELECT id FROM channels WHERE store_id=? AND channel='shopify'",
            (store_id,),
        ).fetchone()
        cid = ch_row[0] if ch_row else None
        conn.execute(
            """INSERT OR REPLACE INTO listings
               (product_id,store_id,channel_id,channel,external_id,external_sku,title,state,channel_price,channel_currency,tags)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (
                product_id,
                store_id,
                cid,
                "shopify",
                str(shopify_id),
                sku,
                title,
                pack.get("shopify_status") or pack.get("state") or "draft",
                price,
                "GBP" if store_id == "pogpet" else ccy,
                json.dumps(pack.get("tags") or [], ensure_ascii=False),
            ),
        )
    return product_id


def load_packs(store_dir: Path) -> list[dict]:
    packs = []
    listing_dir = store_dir / "listings"
    if not listing_dir.exists():
        return packs
    for path in sorted(listing_dir.glob("*.json")):
        if path.name.startswith("_"):
            continue
        try:
            pack = json.loads(path.read_text())
        except json.JSONDecodeError as e:
            print(f"  ! skip {path.name}: {e}", file=sys.stderr)
            continue
        if not isinstance(pack, dict) or "sku" not in pack:
            continue
        if pack["sku"] == "TEMPLATE-SKU":
            continue
        packs.append(pack)
    return packs


def migrate_assets_from_legacy(conn: sqlite3.Connection, store_id: str) -> None:
    """Copy asset rows from legacy oddhobbies.db if present."""
    legacy = ROOT / "db" / "oddhobbies.db"
    if store_id != "oddhobb" or not legacy.exists():
        return
    try:
        leg = sqlite3.connect(legacy)
        leg.row_factory = sqlite3.Row
        cols = {r[1] for r in leg.execute("PRAGMA table_info(assets)")}
        rows = leg.execute("SELECT * FROM assets").fetchall()
    except Exception:
        return

    def g(r, key, default=None):
        if key in cols:
            try:
                v = r[key]
            except Exception:
                return default
            return default if v is None else v
        return default

    for r in rows:
        path = g(r, "path_or_url") or ""
        new_path = path.replace(
            "powpowpow/oddhobbies/assets/",
            "commerce/stores/oddhobb/assets/",
        )
        key = g(r, "asset_key")
        if key and not str(key).startswith("oddhobb/"):
            key = f"oddhobb/{key}"
        # best-effort sku from path/key when legacy rows lacked sku
        sku = g(r, "sku")
        if not sku:
            hay = f"{key or ''} {path}"
            for marker in (
                "ACTIVE-BRICK-FIGURE",
                "ACTIVE-COUPLE-FIGURE",
                "ACTIVE-XMAS-ORNAMENT",
            ):
                if marker in hay:
                    sku = {
                        "ACTIVE-BRICK-FIGURE": "KEYCHAIN-BRICK",
                        "ACTIVE-COUPLE-FIGURE": "KEYCHAIN-BRICK",
                        "ACTIVE-XMAS-ORNAMENT": "XMAS-3D-ORNAMENT",
                    }[marker]
                    break
        conn.execute(
            """INSERT OR IGNORE INTO assets
               (store_id,asset_key,product_id,sku,asset_type,role,product_family,scene,mood,
                channel_fit,suitability_json,mime,width,height,storage,path_or_url,
                alt_text,agent_blurb,agent_keywords,source,confidence,needs_review)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                store_id,
                key,
                g(r, "product_id"),
                sku,
                g(r, "asset_type", "image"),
                g(r, "role"),
                g(r, "product_family"),
                g(r, "scene"),
                g(r, "mood"),
                g(r, "channel_fit"),
                g(r, "suitability_json"),
                g(r, "mime"),
                g(r, "width"),
                g(r, "height"),
                g(r, "storage", "r2"),
                new_path,
                g(r, "alt_text"),
                g(r, "agent_blurb"),
                g(r, "agent_keywords"),
                g(r, "source"),
                g(r, "confidence"),
                g(r, "needs_review", 0) or 0,
            ),
        )
    leg.close()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", action="append", dest="stores", help="store id (repeatable)")
    ap.add_argument("--reset", action="store_true", help="rebuild commerce.db from schema")
    args = ap.parse_args()

    conn = connect(reset=args.reset)
    for sid, name, role, loc, region, etsy, shopify, url, note in SUPPLIERS:
        ensure_supplier(conn, sid)

    store_dirs = []
    if args.stores:
        store_dirs = [STORES / s for s in args.stores]
    else:
        store_dirs = sorted([p for p in STORES.iterdir() if p.is_dir()])

    for store_dir in store_dirs:
        store_json_path = store_dir / "store.json"
        if not store_json_path.exists():
            print(f"skip {store_dir.name}: no store.json", file=sys.stderr)
            continue
        store_json = json.loads(store_json_path.read_text())
        store_id = store_json.get("store_id") or store_dir.name
        upsert_brand_store(conn, store_json)
        packs = load_packs(store_dir)
        n = 0
        for pack in packs:
            pack.setdefault("store_id", store_id)
            insert_product(conn, store_id, pack)
            n += 1
        migrate_assets_from_legacy(conn, store_id)
        print(f"store {store_id}: {n} products seeded")

    for store_id, topic, decision, rationale, on, src in DECISIONS:
        conn.execute(
            """INSERT INTO decisions (store_id,topic,decision,rationale,decided_on,source_doc)
               VALUES (?,?,?,?,?,?)
               ON CONFLICT DO NOTHING""",
            (store_id, topic, decision, rationale, on, src),
        )
        # decisions has no unique constraint; skip exact dupes
        # (ON CONFLICT DO NOTHING may no-op without unique — filter manually)
    # de-dupe decisions by (store_id,topic,decision)
    conn.execute(
        """DELETE FROM decisions WHERE id NOT IN (
             SELECT MIN(id) FROM decisions GROUP BY store_id, topic, decision
           )"""
    )

    for store_id, supplier_id, item, priority in OPEN_QUOTES:
        ensure_supplier(conn, supplier_id)
        exists = conn.execute(
            "SELECT 1 FROM open_quotes WHERE store_id=? AND item=? AND status='open'",
            (store_id, item),
        ).fetchone()
        if not exists:
            conn.execute(
                """INSERT INTO open_quotes (store_id,supplier_id,item,priority,status)
                   VALUES (?,?,?,?,'open')""",
                (store_id, supplier_id, item, priority),
            )

    conn.commit()
    counts = {}
    for t in (
        "brands",
        "stores",
        "channels",
        "suppliers",
        "products",
        "listings",
        "assets",
        "agent_catalog",
        "orders",
        "ad_campaigns",
        "decisions",
        "open_quotes",
    ):
        counts[t] = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print("commerce.db counts:", json.dumps(counts, indent=2))
    print(f"DB: {DB_PATH}")
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

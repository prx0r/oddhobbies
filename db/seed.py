#!/usr/bin/env python3
"""Seed canonical SQLite from product-supplier-db.json + known Etsy draft IDs."""

import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "db" / "oddhobbies.db"
SCHEMA = ROOT / "db" / "schema.sql"
SEED_JSON = ROOT / "data" / "product-supplier-db.json"
DRAFTS_JSON = ROOT / "data" / "xmas-drafts-2026-10-01.json"

# Explicit product -> etsy listing + retail (authoritative from drafts)
LISTINGS = {
    "XMAS-3D-MAHJONG-READER": {"etsy_id": 4586657665, "price": 11.99, "tax": 2387, "tags": "mahjong,line reader,personalised,christmas gift,board game accessory,mahjong gift,tile guide,mahjong player,game night,family gift,mahjong accessory,custom"},
    "XMAS-3D-FIRST-PLAYER": {"etsy_id": 4586658541, "price": 8.99, "tax": 2151, "tags": "first player token,board game token,christmas stocking stuffer,dragon token,personalised token,game night gift,board game accessory,tabletop gift,christmas gift,custom token"},
    "XMAS-3D-CRIBBAGE-PEGS": {"etsy_id": 4586671942, "price": 14.99, "tax": 2151, "tags": "cribbage pegs,cribbage gift,personalised cribbage,cribbage player,christmas gift,magnetic pegs,card game gift,game night,family gift,cribbage board,custom pegs"},
    "XMAS-3D-TILE-RACK": {"etsy_id": 4586662106, "price": 12.99, "tax": 1554, "tags": "tile rack,scrabble rack,board game accessory,christmas gift,game night,personalised gift,magnetic rack,word game,tile holder,family gift,board game gift"},
    "XMAS-3D-MAHJONG-WINDS": {"etsy_id": 4586671970, "price": 16.99, "tax": 2387, "tags": "mahjong wind markers,mahjong accessory,personalised mahjong,mahjong gift,christmas gift,tile markers,mahjong player,board game accessory,custom mahjong,family game night"},
    "XMAS-3D-ORNAMENT": {"etsy_id": 4586658575, "price": 14.99, "tax": 1857, "tags": "christmas ornament,custom ornament,pet ornament,personalised bauble,3d printed ornament,christmas gift,stocking stuffer,family ornament,brick figure,christmas tree,pet gift"},
    "XMAS-3D-TOKEN-TRAY": {"etsy_id": 4586661282, "price": 22.99, "tax": 2151, "tags": "token tray,board game organizer,magnetic tray,hex token,game night,christmas gift,board game accessory,personalised gift,token holder,tabletop,game organizer gift"},
    "XMAS-3D-CRIBBAGE-BOARD": {"etsy_id": 4586671960, "price": 29.99, "tax": 1554, "tags": "cribbage board,travel cribbage,cribbage gift,personalised cribbage,magnetic pegs,cribbage player,christmas gift,card game,game night,family gift,compact board"},
    "ALBUM-MEMORY-CD": {"etsy_id": 4586678882, "price": 34.99, "tax": 1250, "tags": "personalised album,custom album,memory album,anniversary gift,birthday gift,song ep,digital download,personalised music,story album,gift for her,gift for him,keepsake"},
    "ALBUM-WEDDING-VIDEO": {"etsy_id": 4586678898, "price": 59.99, "tax": 1250, "tags": "wedding album,wedding cd,video album,anniversary gift,wedding keepsake,custom wedding,personalised wedding,photo album,gift for couple,engagement gift,wedding gift"},
    "PROD-PET-TAG-SET": {"etsy_id": 4586691324, "price": 16.99, "tax": 1250, "tags": "metal pet tag,custom dog tag,pet tag,personalised pet,christmas gift,dog lover,pet gift,custom tag,pet accessory,gift for dog,keepsake,pet parent"},
    "PROD-BOARDGAME-NOTEBOOK": {"etsy_id": 4586687823, "price": 16.99, "tax": 1250, "tags": "board game notebook,cribbage notebook,game scorebook,custom journal,game night,personalised notebook,christmas gift,family game,card game,notebook,gift for him,keepsake"},
    "PROD-COASTER-SET": {"etsy_id": 4586691376, "price": 19.99, "tax": 1250, "tags": "coaster set,custom coasters,game night,house rules,personalised coasters,christmas gift,family game,coasters,gift for host,table decor,custom gift,game night gift"},
    "PROD-TOP-TRUMPS": {"etsy_id": 4586691360, "price": 24.99, "tax": 1554, "tags": "top trumps,custom card game,battle cards,family cards,game night,christmas gift,personalised cards,playing cards,custom trumps,gift for family,card game,personalised gift"},
    "PROD-XMAS-PLAYING-CARDS": {"etsy_id": 4586691388, "price": 22.99, "tax": 1554, "tags": "personalised playing cards,custom deck,christmas gift,family cards,wedding cards,gift for couple,card deck,personalised gift,playing cards,custom cards,keepsake,game night"},
}

# product sku -> (supplier_id, role, supplier_sku or None)
PRODUCT_SUPPLIERS = {
    "XMAS-3D-MAHJONG-READER": [("MAKR3D", "primary", None), ("PRINTIE", "us_lab", None)],
    "XMAS-3D-FIRST-PLAYER": [("MAKR3D", "primary", None), ("PRINTIE", "us_lab", None)],
    "XMAS-3D-CRIBBAGE-PEGS": [("MAKR3D", "primary", None), ("PRINTIE", "us_lab", None)],
    "XMAS-3D-TILE-RACK": [("MAKR3D", "primary", None), ("PRINTIE", "us_lab", None)],
    "XMAS-3D-MAHJONG-WINDS": [("MAKR3D", "primary", None), ("PRINTIE", "us_lab", None)],
    "XMAS-3D-ORNAMENT": [("MAKR3D", "primary", None), ("PRINTIE", "us_lab", None)],
    "XMAS-3D-TOKEN-TRAY": [("MAKR3D", "primary", None), ("PRINTIE", "us_lab", None)],
    "XMAS-3D-CRIBBAGE-BOARD": [("MAKR3D", "primary", None), ("PRINTIE", "us_lab", None)],
    "ALBUM-MEMORY-CD": [("KUNAKI", "primary", None), ("DISKCR", "alt", None)],
    "ALBUM-WEDDING-VIDEO": [("KUNAKI", "primary", None), ("PRODIGI", "alt", None)],
    "PROD-PET-TAG-SET": [("PRODIGI", "primary", "PET-MET-BONE|PET-MET-ROUND")],
    "PROD-BOARDGAME-NOTEBOOK": [("PRODIGI", "primary", None)],
    "PROD-COASTER-SET": [("PRODIGI", "primary", None)],
    "PROD-TOP-TRUMPS": [("PRODIGI", "primary", None), ("PERSONALISED_PLAYING_CARDS_UK", "alt", None), ("MAKE_PLAYING_CARDS", "alt", None)],
    "PROD-XMAS-PLAYING-CARDS": [("PRODIGI", "primary", None), ("PERSONALISED_PLAYING_CARDS_UK", "alt", None)],
}

# unit cost estimates current (USD unless noted)
UNIT_COSTS = {
    ("XMAS-3D-MAHJONG-READER", "MAKR3D"): (1.75, "USD", "fulfilment only", "estimate", "Makr3D small tier £1.29"),
    ("XMAS-3D-FIRST-PLAYER", "MAKR3D"): (1.75, "USD", "fulfilment only", "estimate", "small"),
    ("XMAS-3D-CRIBBAGE-PEGS", "MAKR3D"): (2.50, "USD", "fulfilment only", "estimate", "small-mid"),
    ("XMAS-3D-TILE-RACK", "MAKR3D"): (3.37, "USD", "fulfilment only", "estimate", "mid £2.50"),
    ("XMAS-3D-MAHJONG-WINDS", "MAKR3D"): (3.37, "USD", "fulfilment only", "estimate", "mid"),
    ("XMAS-3D-ORNAMENT", "MAKR3D"): (1.75, "USD", "fulfilment only", "estimate", "small"),
    ("XMAS-3D-TOKEN-TRAY", "MAKR3D"): (6.00, "USD", "fulfilment only", "estimate", "mid-large range"),
    ("XMAS-3D-CRIBBAGE-BOARD", "MAKR3D"): (10.30, "USD", "fulfilment only", "estimate", "large £7.60"),
    ("ALBUM-MEMORY-CD", "KUNAKI"): (2.00, "USD", "CD only", "verified", "Kunaki jewel case"),
    ("ALBUM-WEDDING-VIDEO", "KUNAKI"): (2.00, "USD", "CD only", "verified", "Kunaki jewel case"),
    ("PROD-PET-TAG-SET", "PRODIGI"): (14.95, "USD", "all-in est", "quote", "£11.16 all-in converted"),
    ("PROD-TOP-TRUMPS", "PERSONALISED_PLAYING_CARDS_UK"): (17.30, "USD", "deck from", "quote", "£12.99 trumps from"),
    ("PROD-XMAS-PLAYING-CARDS", "PERSONALISED_PLAYING_CARDS_UK"): (17.30, "USD", "deck from", "quote", "£12.99 playing cards from"),
}

# product shipping rows (supplier, dest, total days, cost_to_user)
SHIPPING = {
    "XMAS-3D-*": None,  # handled below
}

M3D_LEAD = [
    ("UK", 2, 5, "free_listing", ""),
    ("EU", 4, 9, "free_listing", "check UK-origin customs"),
    ("US", 6, 16, "free_listing", "buyer may pay duties"),
    ("AU", 8, 16, "free_listing", "possible customs"),
]
PRODIGI_LEAD = [
    ("UK", 2, 5, "free_listing", ""),
    ("US", 3, 7, "free_listing", "US labs"),
    ("EU", 3, 8, "free_listing", ""),
    ("AU", 5, 12, "free_listing", ""),
]
KUNAKI_LEAD = [
    ("US", 4, 8, "free_listing", ""),
    ("UK", 8, 22, "free_listing", "intl — order early Xmas"),
    ("ROW", 8, 22, "free_listing", "intl"),
]

DECISIONS = [
    ("supplier_us_3d", "Printie", "US facility, Etsy, qty1, flat fee includes shipping", "US-3D-SUPPLIER.md"),
    ("supplier_uk_3d", "Makr3D", "UK farm, native Etsy, shipper of record, cost model ready", "US-3D-SUPPLIER.md"),
    ("reject_us_primary_3d_vikings", "Not US primary", "Print farm is Riga Latvia — intl ship/customs for US buyers", "US-3D-SUPPLIER.md"),
    ("positioning", "3D-first Game Night + Weddings/Couples", "Avoid generic personalised POD mall; quirky hobby objects", "FLAGSHIP-COSTS.md"),
    ("cut_bandana", "Cut", "User rejected bandana SKU", "FLAGSHIP-COSTS.md"),
    ("prodigi_role", "Add-ons + albums/cards/pet tags only", "Not 3D, not custom game boards", "PRODIGI-XMAS-OPS.md"),
    ("tile_rack_pricing", "Single unit + volume tiers 1/2/4/6", "Inventory locked qty50 @ 12.99", "FLAGSHIP-COSTS.md"),
    ("free_shipping", "Free listing ship + threshold 19.99 combined", "Copy + Shop Manager guarantee", "PRODIGI-XMAS-OPS.md"),
]

OPEN_QUOTES = [
    ("PRINTIE", None, "All-in quotes for 8 Game Night STLs (US ZIP)", "P0"),
    ("MAKR3D", None, "Exact per-file quotes for 8 Game Night STLs", "P0"),
    ("PRODIGI", None, "Pin SKUs + wholesale: card, stickers, wrap, jigsaw, photo book, calendar, coaster, notebook, playing cards", "P0"),
    ("PRODIGI", None, "Confirm pet tag US/UK all-in quote", "P1"),
    ("PERSONALISED_PLAYING_CARDS_UK", None, "Top Trumps 40-pk quote", "P1"),
    ("KUNAKI", None, "Sample CD + ship times US/UK", "P1"),
    ("MAKR3D", None, "Magnet hardware cost for token tray if not printed-in", "P1"),
]


def reset_db() -> sqlite3.Connection:
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA.read_text())
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def seed_suppliers(conn: sqlite3.Connection, data: dict) -> None:
    for sid, s in data["suppliers"].items():
        region = s.get("region_focus") or s.get("locations")
        if isinstance(region, (list, tuple)):
            region = ", ".join(str(x) for x in region)
        elif isinstance(region, dict):
            region = ", ".join(f"{k}:{v}" for k, v in region.items())
        notes_payload = {}
        for k, v in s.items():
            if k in {
                "name", "role", "url", "location", "region_focus", "monthly_fee", "moq",
                "white_label", "etsy_integration", "shopify_integration", "api_base",
                "api_key_live", "dispatch_days", "branding", "caveats", "note", "status",
                "locations", "company_no", "materials", "verified_skus_live_2026_10_01",
                "docs_only_skus_pin_in_dashboard", "cost_tiers_gbp_ex_vat", "cost_tiers_usd_est",
                "shipping_from_hub", "lead_time_by_location", "costs_usd", "costs_gbp",
                "costs_gbp_from", "example_fulfilment_eur", "example_recommended_price_eur",
                "fulfilment_model", "services", "api", "guarantee", "pricing_model",
                "products", "files", "preferred_format", "best_for", "integration_priority",
                "caveats", "not_us", "note",
            }:
                continue
            if isinstance(v, (list, dict)):
                notes_payload[k] = v
        caveats = s.get("caveats")
        if isinstance(caveats, list):
            caveats = "; ".join(str(x) for x in caveats)
        conn.execute(
            """INSERT INTO suppliers
               (id,name,role,url,location,region_focus,monthly_fee,moq,white_label,
                etsy_integration,shopify_integration,api_base,api_key_ref,
                dispatch_days_note,branding_note,caveats,status,notes)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                sid,
                s.get("name") or sid,
                s.get("role"),
                s.get("url"),
                s.get("location"),
                region,
                float(s.get("monthly_fee") or 0),
                int(s.get("moq") or 1) if str(s.get("moq") or 1).isdigit() else s.get("moq") or 1,
                1 if s.get("white_label", True) else 0,
                s.get("etsy_integration"),
                s.get("shopify_integration"),
                s.get("api_base") or s.get("url"),
                "VAULT:PRODIGI_API_KEY" if s.get("api_key_live") else None,
                str(s.get("dispatch_days") or s.get("dispatch_days_note") or ""),
                str(s.get("branding") or s.get("branding_note") or ""),
                caveats,
                s.get("status") or "documented",
                json.dumps(notes_payload, default=str),
            ),
        )
        loc = s.get("location") or ""
        if not loc and isinstance(s.get("locations"), list):
            loc = ", ".join(str(x) for x in s["locations"])
        elif not loc and isinstance(s.get("locations"), str):
            loc = s["locations"]
        country = None
        for iso in ("UK", "US", "EU", "LV", "GB", "DE"):
            if iso.lower() in loc.lower() or (iso == "UK" and "united kingdom" in loc.lower()):
                country = {"UK": "GB", "GB": "GB"}.get(iso, iso if iso in ("US", "LV", "DE") else None)
                if iso == "UK":
                    country = "GB"
                break
        if s.get("location") and "latvia" in str(s.get("location")).lower():
            country = "LV"
        if s.get("location") and "usa" in str(s.get("location")).lower() or (s.get("location") and "Nevada" in str(s.get("location"))):
            country = "US"
        if s.get("location") and "manchester" in str(s.get("location")).lower():
            country = "GB"
        if s.get("location") and "huddersfield" in str(s.get("location")).lower():
            country = "GB"
        conn.execute(
            "INSERT INTO supplier_locations (supplier_id, city, country_iso, is_primary) VALUES (?,?,?,1)",
            (sid, loc.split(",")[0] if loc else None, country),
        )
        # materials
        mats = s.get("materials") or []
        if isinstance(mats, list):
            for m in mats:
                conn.execute(
                    "INSERT OR IGNORE INTO supplier_materials (supplier_id, material) VALUES (?,?)",
                    (sid, m),
                )
        # cost tiers
        if sid == "MAKR3D":
            for code, gbp, usd in (
                ("small", 1.29, 1.75),
                ("medium", 2.50, 3.37),
                ("large", 7.60, 10.30),
            ):
                conn.execute(
                    """INSERT INTO supplier_cost_tiers
                       (supplier_id,tier_code,tier_name,currency,amount,amount_usd_est,includes,source,source_note)
                       VALUES (?,?,?,?,?,?,?,?,?)""",
                    (sid, code, code, "GBP", gbp, usd, "fulfilment only", "estimate", "suppliers repo ex-VAT"),
                )
        if sid == "PRODIGI":
            skus = s.get("verified_skus_live_2026_10_01") or {}
            for sku, meta in skus.items():
                if not isinstance(meta, dict):
                    continue
                amt = meta.get("cost_all_in_gbp_est") or meta.get("wholesale_gbp")
                if amt is None:
                    continue
                conn.execute(
                    """INSERT INTO supplier_cost_tiers
                       (supplier_id,tier_code,tier_name,currency,amount,includes,source,source_note)
                       VALUES (?,?,?,?,?,?,?,?)""",
                    (sid, sku, meta.get("description"), "GBP", float(amt),
                     "all-in" if "all_in" in str(meta) else "wholesale",
                     "verified" if meta.get("api") == "Ok" else "quote",
                     "Prodigi API/docs"),
                )
        if sid == "KUNAKI":
            for code, usd in (
                ("cd_jewel_case", 2.00),
                ("cd_printed_jacket", 1.50),
                ("vinyl_12_display", 11.00),
                ("vinyl_12_black", 36.00),
            ):
                conn.execute(
                    """INSERT INTO supplier_cost_tiers
                       (supplier_id,tier_code,currency,amount,includes,source)
                       VALUES (?,?,?,?,?,?)""",
                    (sid, code, "USD", usd, "unit", "verified"),
                )
        if sid == "DISKCR":
            for code, gbp in (
                ("standard_jewel_case", 7.99),
                ("slim_jewel_case", 7.50),
            ):
                conn.execute(
                    """INSERT INTO supplier_cost_tiers
                       (supplier_id,tier_code,currency,amount,includes,source)
                       VALUES (?,?,?,?,?,?)""",
                    (sid, code, "GBP", gbp, "unit", "verified"),
                )
        if sid == "PERSONALISED_PLAYING_CARDS_UK":
            for code, gbp in (
                ("trumps_40", 12.99),
                ("playing_cards", 12.99),
                ("tarot_78", 25.99),
            ):
                conn.execute(
                    """INSERT INTO supplier_cost_tiers
                       (supplier_id,tier_code,currency,amount,includes,source)
                       VALUES (?,?,?,?,?,?)""",
                    (sid, code, "GBP", gbp, "from", "verified"),
                )
        # lead times
        if sid == "MAKR3D":
            for dest, tmin, tmax, cost, note in M3D_LEAD:
                conn.execute(
                    """INSERT INTO supplier_lead_times
                       (supplier_id,destination_region,total_days_min,total_days_max,shipping_cost_note,customs_buyer_pays,source)
                       VALUES (?,?,?,?,?,?,?)""",
                    (sid, dest, tmin, tmax, cost, 1 if dest in ("US", "AU") else 0, "estimate"),
                )
        if sid == "PRODIGI":
            for dest, tmin, tmax, cost, note in PRODIGI_LEAD:
                conn.execute(
                    """INSERT INTO supplier_lead_times
                       (supplier_id,destination_region,total_days_min,total_days_max,shipping_cost_note,source)
                       VALUES (?,?,?,?,?,?)""",
                    (sid, dest, tmin, tmax, cost, "estimate"),
                )
        if sid == "KUNAKI":
            for dest, tmin, tmax, cost, note in KUNAKI_LEAD:
                conn.execute(
                    """INSERT INTO supplier_lead_times
                       (supplier_id,destination_region,total_days_min,total_days_max,shipping_cost_note,source)
                       VALUES (?,?,?,?,?,?)""",
                    (sid, dest, tmin, tmax, cost, "estimate"),
                )
        if sid == "PRINTIE":
            conn.execute(
                """INSERT INTO supplier_lead_times
                   (supplier_id,destination_region,shipping_cost_note,source)
                   VALUES (?,?,?,?)""",
                (sid, "US", "bundled in flat fee", "research"),
            )


def seed_products(conn: sqlite3.Connection, data: dict) -> dict:
    sku_to_id = {}
    for row in data["products"]:
        sku = row["sku"]
        cur = conn.execute(
            """INSERT INTO products
               (sku,title,section,make,material,size_class,dimensions_json,
                personalisation_json,demand_evidence,status,priority)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (
                sku,
                row.get("title") or sku,
                row.get("section"),
                row.get("make"),
                row.get("material"),
                (row.get("dimensions") or {}).get("size_class"),
                json.dumps(row.get("dimensions") or {}),
                json.dumps(row.get("personalisation") or []),
                row.get("demand_evidence"),
                row.get("status") or "draft",
                "P0" if "3d_print" in (row.get("make") or "") else "P1",
            ),
        )
        pid = cur.lastrowid
        sku_to_id[sku] = pid

        # suppliers
        for sid, role, ssup in PRODUCT_SUPPLIERS.get(sku, []):
            conn.execute(
                """INSERT OR IGNORE INTO product_suppliers
                   (product_id,supplier_id,role,supplier_sku) VALUES (?,?,?,?)""",
                (pid, sid, role, ssup),
            )
        # also pull from seed json if any
        if row.get("supplier_primary"):
            conn.execute(
                """INSERT OR IGNORE INTO product_suppliers
                   (product_id,supplier_id,role,supplier_sku) VALUES (?,?,?,?)""",
                (pid, row["supplier_primary"], "primary", row.get("prodigi_skus") and "|".join(row["prodigi_skus"]) or None),
            )

        # costs
        for (psku, sid), (cost, ccy, includes, source, note) in UNIT_COSTS.items():
            if psku != sku:
                continue
            conn.execute(
                """INSERT INTO product_costs
                   (product_id,supplier_id,currency,unit_cost,cost_includes,source,source_note,is_current)
                   VALUES (?,?,?,?,?,?,?,1)""",
                (pid, sid, ccy, cost, includes, source, note),
            )

        # retail
        if sku in LISTINGS:
            L = LISTINGS[sku]
            conn.execute(
                """INSERT INTO product_retail_prices
                   (product_id,channel,currency,price,tier_code,is_current)
                   VALUES (?,?,'USD',?,NULL,1)""",
                (pid, "etsy", L["price"]),
            )
        elif row.get("price_usd"):
            conn.execute(
                """INSERT INTO product_retail_prices
                   (product_id,channel,currency,price,is_current)
                   VALUES (?,'etsy','USD',?,1)""",
                (pid, row["price_usd"]),
            )

        # tile rack volume tiers
        if sku == "XMAS-3D-TILE-RACK":
            for qty, unit in ((1, 12.99), (2, 11.99), (4, 10.99), (6, 9.99)):
                conn.execute(
                    """INSERT OR IGNORE INTO product_retail_prices
                       (product_id,channel,currency,price,tier_code,qty_min,qty_max,is_current)
                       VALUES (?,'etsy','USD',?,?,?,? ,1)""",
                    (pid, unit, f"qty{qty}", qty, qty),
                )

        # files
        for f in row.get("files_needed") or []:
            conn.execute(
                """INSERT INTO product_files (product_id,file_type,status,notes)
                   VALUES (?,?, 'needed', ?)""",
                (pid, "STL/art/SOP", f),
            )

        # product shipping matrix
        for sid in [x[0] for x in PRODUCT_SUPPLIERS.get(sku, [])]:
            if sid == "MAKR3D":
                leads = M3D_LEAD
            elif sid == "PRINTIE":
                leads = [("US", None, None, "bundled", "")]
            elif sid == "PRODIGI":
                leads = PRODIGI_LEAD
            elif sid == "KUNAKI":
                leads = KUNAKI_LEAD
            elif sid == "DISKCR":
                leads = [("UK", None, None, "Q", ""), ("ROW", None, None, "Q", "")]
            elif sid == "PERSONALISED_PLAYING_CARDS_UK":
                leads = [("UK", 1, 3, "Q", "same-day if by 11am"), ("US", 4, 14, "Q", "intl")]
            else:
                leads = []
            for dest, tmin, tmax, cost, note in leads:
                conn.execute(
                    """INSERT OR IGNORE INTO product_shipping
                       (product_id,supplier_id,hub_region,destination,
                        total_days_min,total_days_max,cost_to_user,customs_note)
                       VALUES (?,?,?,?,?,?,?,?)""",
                    (
                        pid,
                        sid,
                        "US" if sid in ("PRINTIE", "KUNAKI") else ("UK" if sid in ("MAKR3D", "DISKCR", "PERSONALISED_PLAYING_CARDS_UK") else "MULTI"),
                        dest,
                        tmin,
                        tmax,
                        cost,
                        note or None,
                    ),
                )
    return sku_to_id


def seed_channels(conn: sqlite3.Connection, sku_to_id: dict, data: dict) -> None:
    conn.execute(
        """INSERT OR REPLACE INTO shops
           (id,channel,shop_name,external_id,currency,url)
           VALUES ('etsy:67863887','etsy','PogPet','67863887','USD','https://www.etsy.com/shop/pogpet')"""
    )
    conn.execute(
        """INSERT OR REPLACE INTO shop_policies
           (shop_id,free_shipping,free_shipping_threshold_usd,threshold_enforcement,
            addon_sticker_usd,addon_postcard_usd)
           VALUES ('etsy:67863887',1,19.99,'copy_plus_dashboard_guarantee',3.99,2.99)"""
    )
    # Shopify placeholder
    conn.execute(
        """INSERT OR REPLACE INTO shops
           (id,channel,shop_name,external_id,currency)
           VALUES ('shopify:pogpet','shopify','PogPet',NULL,'USD')"""
    )

    for sku, meta in LISTINGS.items():
        pid = sku_to_id.get(sku)
        conn.execute(
            """INSERT INTO listings
               (product_id,shop_id,channel,external_id,title,state,channel_price,
                channel_currency,quantity,taxonomy_id,shipping_profile_id,readiness_state_id,tags)
               VALUES (?,?, 'etsy', ?, ?, 'draft', ?, 'USD', 100, ?, '316299492609', 1518572416146, ?)""",
            (
                pid,
                "etsy:67863887",
                str(meta["etsy_id"]),
                meta.get("title") or sku,
                meta["price"],
                meta.get("tax"),
                meta.get("tags"),
            ),
        )
        lid = conn.execute(
            "SELECT id FROM listings WHERE shop_id=? AND external_id=?",
            ("etsy:67863887", str(meta["etsy_id"])),
        ).fetchone()[0]
        # addons on all listings
        conn.execute(
            """INSERT OR IGNORE INTO listing_addons
               (listing_id,addon_sku,addon_price,usual_price,supplier_id)
               VALUES (?,?,3.99,7.99,'PRODIGI')""",
            (lid, "ADDON-STICKER"),
        )
        conn.execute(
            """INSERT OR IGNORE INTO listing_addons
               (listing_id,addon_sku,addon_price,usual_price,supplier_id)
               VALUES (?,?,2.99,3.99,'PRODIGI')""",
            (lid, "ADDON-POSTCARD"),
        )


def seed_ops(conn: sqlite3.Connection, sku_to_id: dict) -> None:
    for topic, decision, rationale, src in DECISIONS:
        conn.execute(
            """INSERT INTO decisions (topic,decision,rationale,source_doc)
               VALUES (?,?,?,?)""",
            (topic, decision, rationale, src),
        )
    for sid, psku, item, pri in OPEN_QUOTES:
        conn.execute(
            """INSERT INTO open_quotes (supplier_id,item,priority,status)
               VALUES (?,?,?, 'open')""",
            (sid, item, pri),
        )


def main() -> None:
    data = json.loads(SEED_JSON.read_text())
    if DRAFTS_JSON.exists():
        pass  # LISTINGS constant is authoritative for etsy ids
    conn = reset_db()
    seed_suppliers(conn, data)
    sku_to_id = seed_products(conn, data)
    seed_channels(conn, sku_to_id, data)
    seed_ops(conn, sku_to_id)
    conn.commit()

    # sanity
    counts = {}
    for t in (
        "suppliers",
        "products",
        "product_suppliers",
        "product_costs",
        "listings",
        "listing_addons",
        "open_quotes",
        "decisions",
        "supplier_cost_tiers",
        "supplier_lead_times",
    ):
        counts[t] = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print("Seeded", DB_PATH)
    print(json.dumps(counts, indent=2))

    print("\n--- v_products_current ---")
    for r in conn.execute(
        "SELECT sku, section, primary_supplier, current_unit_cost, retail_price FROM v_products_current LIMIT 20"
    ):
        print(r)

    print("\n--- v_open_quotes ---")
    for r in conn.execute("SELECT priority, supplier, item FROM v_open_quotes"):
        print(r)

    conn.close()


if __name__ == "__main__":
    main()

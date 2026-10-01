#!/usr/bin/env python3
"""Seed channel templates (Etsy / Shopify / Pinterest / agent) + sample payloads."""

import json
import sqlite3
from pathlib import Path

DB = Path("/root/oddhobbies/db/oddhobbies.db")

# ---------------------------------------------------------------------------
# TEMPLATES — field contracts adapted from open-source + official platform shapes
# ---------------------------------------------------------------------------

ETSY_FIELDS = {
    "required": ["quantity", "title", "description", "price", "who_made", "when_made", "taxonomy_id"],
    "recommended": [
        "tags", "materials", "processing_min", "processing_max",
        "shipping_profile_id", "readiness_state_id", "is_customizable",
        "who_made", "when_made", "is_supply", "type",
    ],
    "rules": {
        "title_max": 140,
        "tag_count": 13,
        "tag_max_chars": 20,
        "tags_lowercase": True,
        "description_hook_chars": 160,
        "materials_max": 13,
        "no_brand_marks": ["LEGO", "Scrabble", "Rummikub", "Catan", "Magic: The Gathering"],
        "personalization_question_text_max": 45,
        "personalization_max_chars": "1-1024",
        "personalization_max_files": 2,
        "price_min": 0.01,
        "who_made_enum": ["i_did", "someone_else", "collective"],
        "when_made_enum": ["made_to_order", "2020_2026", "2010_2019", "before_2007"],
        "type_enum": ["physical", "download", "both"],
    },
    "copy_blocks": [
        {"key": "hook", "max_chars": 160, "note": "Google snippet / first line"},
        {"key": "how_it_works", "format": "numbered"},
        {"key": "what_you_get", "format": "bullets"},
        {"key": "ip_line", "note": "Original design — not affiliated with any game brand"},
        {"key": "fulfilment", "note": "supplier + dispatch + free ship / threshold"},
        {"key": "addons", "note": "sticker $3.99 / postcard $2.99 if prodigi"},
    ],
    "photo_slots": [
        "hero", "personalisation", "in_use_hand", "detail_engraving",
        "packaging", "size_scale", "lifestyle_table", "occasion_xmas",
        "variants", "bundle_upsell",
    ],
    "api": {
        "create": "POST /v3/application/shops/{shop_id}/listings",
        "state_draft": "draft",
        "shipping_profile_id": 316299492609,
        "readiness_state_id": 1518572416146,
    },
    "source_refs": [
        "https://github.com/silennsong/etsy-listing-helper",
        "https://github.com/eisenheiim/Contentsy",
        "https://github.com/DynamicEndpoints/etsy-mcp",
        "Etsy Open API createDraftListing",
        "Etsy Seller Handbook: 13 tags, title 140, tags 20 chars",
    ],
}

SHOPIFY_FIELDS = {
    "required_csv": [
        "Handle", "Title", "Body (HTML)", "Vendor", "Type", "Tags",
        "Published", "Option1 Name", "Option1 Value",
        "Variant SKU", "Variant Price", "Variant Grams",
        "Variant Inventory Qty", "Variant Inventory Policy",
        "Variant Fulfillment Service", "Variant Requires Shipping",
        "Image Src", "Image Position", "Image Alt Text",
    ],
    "optional_csv": [
        "Template Suffix", "SEO Title", "SEO Description",
        "Cost per item", "Compare At Price",
        "Google Shopping / Product Category",
        "Metafields Global Title Tag", "Metafields Global Description Tag",
        "Variant Weight Unit", "Variant Taxable",
    ],
    "rules": {
        "handle_slug": "lowercase-hyphens",
        "body_html": True,
        "vendor": "OddHobbies",
        "tags_max": 250,
        "image_position": "1 = hero",
        "seo_title_max": 70,
        "seo_description_max": 160,
        "status_field": "draft|active|archived (CSV Status column if present)",
        "fulfillment_service": "manual | shipstation | printful | makr3d",
        "inventory_policy": "deny | continue",
    },
    "csv_reference_headers": [
        "Handle", "Title", "Body (HTML)", "Vendor", "Type", "Tags",
        "Published", "Option1 Name", "Option1 Value",
        "Variant SKU", "Variant Grams", "Variant Inventory Tracker",
        "Variant Inventory Qty", "Variant Inventory Policy",
        "Variant Fulfillment Service", "Variant Price",
        "Variant Compare At Price", "Variant Requires Shipping",
        "Variant Taxable", "Image Src", "Image Position", "Image Alt Text",
        "SEO Title", "SEO Description", "Cost per item", "Status",
    ],
    "source_refs": [
        "https://github.com/Shopify/shopify_transporter",
        "https://github.com/shopifypartners/product-csvs",
        "https://github.com/doeixd/parse-shopify-csv",
        "https://github.com/gauranshahuja/shopify-listing-ai",
        "https://github.com/pandas9/shopify-products",
    ],
}

PINTEREST_FIELDS = {
    "pin": {
        "title_max": 100,
        "description_max": 500,
        "required": ["title", "description", "link", "image"],
        "recommended": ["board", "carousel", "video_pin", "shopping_tag"],
    },
    "creative": {
        "aspect_ratios": ["2:3", "9:16", "1:1"],
        "primary_aspect": "2:3",
        "min_px": [1000, 1500],
        "text_overlay": "optional, keep readable on mobile",
        "cta_examples": ["Shop now", "Learn more", "Get the gift"],
    },
    "ad_slots": [
        {"slot": "hero_pin", "role": "hero", "aspect": "2:3", "score_priority": 1},
        {"slot": "lifestyle_pin", "role": "lifestyle", "aspect": "2:3", "score_priority": 2},
        {"slot": "detail_pin", "role": "detail", "aspect": "2:3", "score_priority": 3},
        {"slot": "xmas_gift_pin", "role": "lifestyle", "aspect": "2:3", "mood": "festive"},
    ],
    "boards": ["game-night", "christmas-gifts", "weddings-couples", "pet-gifts", "hobby-tools"],
    "copy": {
        "title_formula": "{product} | {occasion} | {benefit}",
        "description_formula": "{hook}. {what_it_is}. Perfect for {audience}. {cta} {url}",
        "keyword_style": "long-tail, gift intent, no brand marks",
    },
    "api": {
        "rest": "https://api.pinterest.com/v5",
        "create_pin": "POST /v5/pins",
        "boards": "GET /v5/boards",
    },
    "source_refs": [
        "https://github.com/vijaxx/pinforge",
        "https://github.com/Dagimal/pinterest-pin-creator",
        "https://github.com/arndvs/cast",
        "Pinterest API v5 (pins, boards, ads)",
        "https://github.com/pinterest/api-description",
    ],
}

AGENT_FIELDS = {
    "expose": [
        "agent_sku", "display_name", "summary", "price_tier",
        "gift_occasions", "fulfilment_blurb", "is_orderable", "is_customisable",
    ],
    "never_expose": [
        "unit_cost", "supplier_internal_notes", "api_keys", "open_quotes",
        "production_partner_ids", "listing_draft_state_detail",
    ],
    "tools": [
        "shop.list_products", "shop.get_product", "shop.customise",
        "shop.quote", "assets_pick",
    ],
    "rules": {
        "summary_max_chars": 300,
        "orderable_requires": ["images_live", "production_partner", "stock_policy"],
    },
    "source_refs": [
        "oddhobbies/db/CONSUMER-MCP.md",
        "v_agent_catalog view",
    ],
}

TEMPLATES = [
    {
        "template_key": "etsy_standard_v1",
        "channel": "etsy",
        "version": "1",
        "title": "Etsy standard listing (draft API shape)",
        "description": "Full createDraftListing payload + 13-tag SEO + 10 photo slots + personalization rules.",
        "fields": ETSY_FIELDS,
        "slots": ETSY_FIELDS["photo_slots"],
        "validation": ETSY_FIELDS["rules"],
        "source": "Etsy API + GitHub listing helpers",
    },
    {
        "template_key": "shopify_product_v1",
        "channel": "shopify",
        "version": "1",
        "title": "Shopify product CSV / Admin product",
        "description": "Official Shopify product CSV column contract + SEO fields + variant defaults for POD.",
        "fields": SHOPIFY_FIELDS,
        "slots": ["hero_image", "lifestyle", "detail", "size_chart"],
        "validation": SHOPIFY_FIELDS["rules"],
        "source": "Shopify transporter + partner CSVs + listing-ai",
    },
    {
        "template_key": "pinterest_pin_v1",
        "channel": "pinterest",
        "version": "1",
        "title": "Pinterest pin + ad creative program",
        "description": "Pin copy, 2:3 creative slots, board map, optional promoted-pin fields.",
        "fields": PINTEREST_FIELDS,
        "slots": [s["slot"] for s in PINTEREST_FIELDS["ad_slots"]],
        "validation": PINTEREST_FIELDS["pin"],
        "source": "pinforge + Pinterest API v5 + cast",
    },
    {
        "template_key": "agent_catalog_v1",
        "channel": "agent",
        "version": "1",
        "title": "Consumer agent catalog projection",
        "description": "What ChatGPT/plugin agents may see; cost/internal fields stripped.",
        "fields": AGENT_FIELDS,
        "slots": ["hero_asset", "summary", "personalisation_questions"],
        "validation": AGENT_FIELDS["rules"],
        "source": "CONSUMER-MCP.md + v_agent_catalog",
    },
]

# default generators for filled payloads
def etsy_payload(product: dict) -> dict:
    sku = product["sku"]
    title = product.get("title") or sku
    tags = list(product.get("etsy_tags") or TAGS_BY_SKU.get(sku) or [])[:13]
    while len(tags) < 13:
        tags.append("christmas gift" if len(tags) % 2 == 0 else "personalised gift")
    tags = [t[:20] for t in tags]
    hook = product.get("agent_blurb") or product.get("summary") or title
    return {
        "quantity": 100,
        "title": title[:140],
        "description": (
            f"{hook[:160]}\n\n"
            "HOW IT WORKS:\n1. Order and send personalisation\n2. Approve preview\n"
            "3. We make it to order\n4. Tracked shipping\n\n"
            "WHAT YOU GET:\n- Personalised product\n- Gift-ready packing\n- Preview before print where applicable\n\n"
            "Original design — not affiliated with any game brand.\n"
            "Free shipping. Orders over $19.99 combined ship free.\n"
            "Add-ons: sticker sheet $3.99 · postcard $2.99.\n"
        ),
        "price": float(product.get("retail_price") or product.get("price_usd") or 19.99),
        "who_made": "collective",
        "when_made": "made_to_order",
        "is_supply": False,
        "type": "physical",
        "taxonomy_id": int(product.get("taxonomy_id") or 1552),
        "etsy_listing_id": product.get("etsy_listing_id"),
        "tags": tags,
        "materials": (product.get("material") or "PLA").split(),
        "processing_min": 3,
        "processing_max": 8,
        "shipping_profile_id": 316299492609,
        "readiness_state_id": 1518572416146,
        "is_customizable": True,
        "meta": {
            "template_key": "etsy_standard_v1",
            "sku": sku,
            "photo_slots": ETSY_FIELDS["photo_slots"],
            "source_refs": ETSY_FIELDS["source_refs"],
        },
    }


def shopify_payload(product: dict) -> dict:
    sku = product["sku"]
    title = product.get("title") or sku
    handle = re_slug(sku)
    price = float(product.get("retail_price") or product.get("price_usd") or 19.99)
    alt = (product.get("agent_blurb") or title)[:250]
    body = f"<p>{product.get('agent_blurb') or title}</p><ul><li>Personalised to order</li><li>Free shipping over $19.99 combined</li></ul>"
    return {
        "Handle": handle,
        "Title": title,
        "Body (HTML)": body,
        "Vendor": "OddHobbies",
        "Type": product.get("section") or "Gift",
        "Tags": ",".join([
            handle.replace("-", " "),
            "christmas gift",
            "personalised",
            "game night",
            "odd hobbies",
        ]),
        "Published": "FALSE",
        "Status": "draft",
        "Option1 Name": "Style",
        "Option1 Value": "Default",
        "Variant SKU": sku,
        "Variant Grams": 120,
        "Variant Inventory Tracker": "shopify",
        "Variant Inventory Qty": 100,
        "Variant Inventory Policy": "deny",
        "Variant Fulfillment Service": "manual",
        "Variant Price": f"{price:.2f}",
        "Variant Requires Shipping": "TRUE",
        "Variant Taxable": "TRUE",
        "Image Src": "",
        "Image Position": "1",
        "Image Alt Text": alt,
        "SEO Title": title[:70],
        "SEO Description": (product.get("agent_blurb") or title)[:160],
        "Cost per item": "",
        "meta": {
            "template_key": "shopify_product_v1",
            "sku": sku,
            "csv_headers": SHOPIFY_FIELDS["csv_reference_headers"],
            "source_refs": SHOPIFY_FIELDS["source_refs"],
        },
    }


def pinterest_payload(product: dict) -> dict:
    sku = product["sku"]
    title = product.get("title") or sku
    hook = product.get("agent_blurb") or title
    occasion = "Christmas gift"
    if product.get("section") == "Weddings & Couples":
        occasion = "Wedding & anniversary gift"
    pins = []
    for slot in PINTEREST_FIELDS["ad_slots"]:
        pins.append({
            "slot": slot["slot"],
            "title": f"{title[:60]} | {occasion}"[:100],
            "description": f"{hook[:180]} Perfect for {occasion.lower()} shoppers. Shop now."[:500],
            "link": f"https://www.etsy.com/shop/pogpet?search_query={sku}",
            "board": slot.get("board") or (
                "christmas-gifts" if "xmas" in slot["slot"] or "Christmas" in occasion
                else "weddings-couples" if "Wedding" in occasion
                else "game-night"
            ),
            "aspect": "2:3",
            "creative_role": slot.get("role") or "hero",
            "asset_pick_channel": "pinterest",
            "image_path": "",  # fill from assets_pick
        })
    return {
        "product_sku": sku,
        "primary_aspect": "2:3",
        "min_px": [1000, 1500],
        "pins": pins,
        "cta": "Shop now",
        "meta": {
            "template_key": "pinterest_pin_v1",
            "boards": PINTEREST_FIELDS["boards"],
            "source_refs": PINTEREST_FIELDS["source_refs"],
        },
    }


def agent_payload(product: dict) -> dict:
    return {
        "agent_sku": re_slug(product.get("agent_sku") or product["sku"]),
        "display_name": product.get("display_name") or product.get("title") or product["sku"],
        "summary": (product.get("agent_blurb") or product.get("summary") or product.get("title") or "")[:300],
        "price_tier": product.get("price_tier") or "gift",
        "gift_occasions": product.get("gift_occasions") or "christmas",
        "fulfilment_blurb": product.get("fulfilment_blurb") or "Made to order",
        "is_orderable": 0,
        "is_customisable": 1,
        "personalisation_questions": product.get("personalisation_questions") or [],
        "never_expose": AGENT_FIELDS["never_expose"],
        "meta": {"template_key": "agent_catalog_v1"},
    }


def re_slug(s: str) -> str:
    out = []
    prev = "-"
    for ch in (s or "product").lower():
        if ch.isalnum():
            out.append(ch); prev = ch
        elif prev != "-":
            out.append("-"); prev = "-"
    return "".join(out).strip("-") or "product"


TAGS_BY_SKU = {"XMAS-3D-MAHJONG-READER": ["mahjong gift", "line reader", "mahjong accessory", "personalised mahjong", "custom tile guide", "mahjong player", "christmas gift", "board game", "family game", "personalised gift", "game night", "tabletop gift", "mahjong set"], "XMAS-3D-FIRST-PLAYER": ["first player token", "board game token", "christmas gift", "stocking stuffer", "dragon token", "personalised token", "game night", "tabletop gift", "custom token", "board game gift", "family game", "christmas stocking", "game accessory"], "XMAS-3D-CRIBBAGE-PEGS": ["cribbage pegs", "cribbage gift", "personalised cribbage", "cribbage player", "christmas gift", "magnetic pegs", "card game gift", "game night", "family gift", "cribbage board", "custom pegs", "tabletop gift", "christmas game"], "XMAS-3D-TILE-RACK": ["tile rack", "scrabble rack", "board game accessory", "christmas gift", "game night", "personalised gift", "magnetic rack", "word game", "tile holder", "family gift", "board game gift", "modern rack", "game night gift"], "XMAS-3D-MAHJONG-WINDS": ["mahjong winds", "mahjong accessory", "personalised mahjong", "mahjong gift", "christmas gift", "tile markers", "mahjong player", "board game", "custom mahjong", "game night", "family gift", "mahjong set", "tabletop gift"], "XMAS-3D-ORNAMENT": ["christmas ornament", "custom ornament", "pet ornament", "personalised bauble", "3d printed ornament", "christmas gift", "stocking stuffer", "family ornament", "brick figure", "christmas tree", "pet gift", "dog ornament", "personalised christmas"], "XMAS-3D-TOKEN-TRAY": ["token tray", "board game organizer", "magnetic tray", "hex token", "game night", "christmas gift", "board game accessory", "personalised gift", "token holder", "tabletop", "game organizer", "custom colours", "board game gift"], "XMAS-3D-CRIBBAGE-BOARD": ["cribbage board", "travel cribbage", "cribbage gift", "personalised cribbage", "magnetic pegs", "cribbage player", "christmas gift", "card game", "game night", "family gift", "compact board", "tabletop gift", "christmas game"], "ALBUM-MEMORY-CD": ["personalised album", "custom album", "memory album", "anniversary gift", "birthday gift", "song ep", "digital download", "personalised music", "story album", "gift for her", "gift for him", "keepsake", "christmas gift"], "ALBUM-WEDDING-VIDEO": ["wedding album", "wedding cd", "video album", "anniversary gift", "wedding keepsake", "custom wedding", "personalised wedding", "photo album", "gift for couple", "engagement gift", "wedding gift", "keepsake", "christmas gift"], "PROD-PET-TAG-SET": ["metal pet tag", "custom dog tag", "pet tag", "personalised pet", "christmas gift", "dog lover", "pet gift", "custom tag", "pet accessory", "gift for dog", "keepsake", "pet parent", "christmas pet"], "PROD-BOARDGAME-NOTEBOOK": ["board game notebook", "cribbage notebook", "game scorebook", "custom journal", "game night", "personalised notebook", "christmas gift", "family game", "card game", "notebook", "gift for him", "keepsake", "cribbage gift"], "PROD-COASTER-SET": ["coaster set", "custom coasters", "game night", "house rules", "personalised coasters", "christmas gift", "family game", "coasters", "gift for host", "table decor", "custom gift", "game night gift", "christmas game"], "PROD-TOP-TRUMPS": ["top trumps", "custom card game", "battle cards", "family cards", "game night", "christmas gift", "personalised cards", "playing cards", "custom trumps", "gift for family", "card game", "personalised gift", "christmas game"], "PROD-XMAS-PLAYING-CARDS": ["personalised playing cards", "custom deck", "christmas gift", "family cards", "wedding cards", "gift for couple", "card deck", "personalised gift", "playing cards", "custom cards", "keepsake", "game night", "wedding gift"]}

GENERATORS = {
    "etsy_standard_v1": etsy_payload,
    "shopify_product_v1": shopify_payload,
    "pinterest_pin_v1": pinterest_payload,
    "agent_catalog_v1": agent_payload,
}


def load_products(conn) -> list[dict]:
    rows = conn.execute(
        """
        SELECT p.id, p.sku,
               COALESCE(l.title, p.title) AS title,
               a.agent_sku, a.display_name, a.summary, NULL AS agent_blurb,
               a.price_tier, a.gift_occasions, a.fulfilment_blurb,
               COALESCE(l.channel_price, rp.price) AS retail_price,
               COALESCE(l.taxonomy_id, 1552) AS taxonomy_id,
               l.external_id AS etsy_listing_id
        FROM products p
        LEFT JOIN listings l ON l.product_id = p.id AND l.channel='etsy'
        LEFT JOIN agent_catalog a ON a.product_id = p.id
        LEFT JOIN product_retail_prices rp
          ON rp.product_id = p.id AND rp.is_current = 1 AND rp.channel='etsy'
         AND rp.tier_code IS NULL
        WHERE p.status IN ('draft','live','draft_live')
        """
    ).fetchall()
    out = []
    for r in rows:
        d = dict(r)
        # pull one agent_blurb from assets if missing
        if not d.get("agent_blurb"):
            ab = conn.execute(
                "SELECT agent_blurb FROM assets WHERE product_id=? AND agent_blurb IS NOT NULL LIMIT 1",
                (r["id"],),
            ).fetchone()
            d["agent_blurb"] = ab[0] if ab else None
        qs = conn.execute(
            "SELECT question_key, question_text, question_type, required, max_chars, instructions "
            "FROM personalisation_questions WHERE product_id=? ORDER BY id",
            (r["id"],),
        ).fetchall()
        d["personalisation_questions"] = [dict(q) for q in qs]
        d["etsy_tags"] = TAGS_BY_SKU.get(r["sku"], [])
        out.append(d)
    return out


def main() -> None:
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.executescript(Path("/root/oddhobbies/db/schema_channel_templates.sql").read_text())

    tmpl_ids = {}
    for t in TEMPLATES:
        conn.execute(
            """INSERT INTO channel_templates
               (template_key, channel, version, title, description, fields_json, slots_json, validation_json, source_note)
               VALUES (?,?,?,?,?,?,?,?,?)
               ON CONFLICT(channel, version) DO UPDATE SET
                 title=excluded.title, description=excluded.description,
                 fields_json=excluded.fields_json, slots_json=excluded.slots_json,
                 validation_json=excluded.validation_json, source_note=excluded.source_note""",
            (
                t["template_key"], t["channel"], t["version"], t["title"], t["description"],
                json.dumps(t["fields"]), json.dumps(t["slots"]), json.dumps(t["validation"]),
                t["source"],
            ),
        )
        row = conn.execute(
            "SELECT id FROM channel_templates WHERE template_key=?", (t["template_key"],)
        ).fetchone()
        tmpl_ids[t["template_key"]] = row["id"]

    products = load_products(conn)
    n = 0
    for product in products:
        for key, gen in GENERATORS.items():
            payload = gen(product)
            conn.execute(
                """INSERT INTO channel_payloads
                   (product_id, template_id, channel, status, payload_json)
                   VALUES (?,?,?,?,?)
                   ON CONFLICT(product_id, channel, template_id) DO UPDATE SET
                     payload_json=excluded.payload_json,
                     generated_at=datetime('now')""",
                (
                    product["id"],
                    tmpl_ids[key],
                    {"etsy_standard_v1":"etsy","shopify_product_v1":"shopify",
                     "pinterest_pin_v1":"pinterest","agent_catalog_v1":"agent"}[key],
                    "draft",
                    json.dumps(payload),
                ),
            )
            n += 1

    conn.commit()
    print("templates", conn.execute("SELECT COUNT(*) FROM channel_templates").fetchone()[0])
    print("payloads", conn.execute("SELECT COUNT(*) FROM channel_payloads").fetchone()[0])
    print("products", len(products))
    print("\n--- sample etsy payload (tile rack) ---")
    row = conn.execute(
        """SELECT cp.payload_json FROM channel_payloads cp
           JOIN products p ON p.id=cp.product_id
           WHERE p.sku='XMAS-3D-TILE-RACK' AND cp.channel='etsy'"""
    ).fetchone()
    if row:
        pl = json.loads(row["payload_json"])
        print("title:", pl["title"][:80])
        print("price:", pl["price"], "tags:", len(pl["tags"]), "taxonomy:", pl["taxonomy_id"])
    print("\n--- sample shopify ---")
    row = conn.execute(
        """SELECT cp.payload_json FROM channel_payloads cp
           JOIN products p ON p.id=cp.product_id
           WHERE p.sku='XMAS-3D-ORNAMENT' AND cp.channel='shopify'"""
    ).fetchone()
    if row:
        pl = json.loads(row["payload_json"])
        print("handle:", pl["Handle"], "price:", pl["Variant Price"], "status:", pl["Status"])
    print("\n--- sample pinterest pin count ---")
    row = conn.execute(
        """SELECT cp.payload_json FROM channel_payloads cp
           JOIN products p ON p.id=cp.product_id
           WHERE p.sku='ALBUM-MEMORY-CD' AND cp.channel='pinterest'"""
    ).fetchone()
    if row:
        pl = json.loads(row["payload_json"])
        print("pins:", len(pl["pins"]), "first:", pl["pins"][0]["title"][:60])
    conn.close()


if __name__ == "__main__":
    main()

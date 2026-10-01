#!/usr/bin/env python3
"""Seed agent-readable labels on existing assets (from known source folders + heuristics)."""

import json
import sqlite3
from pathlib import Path

DB = Path("/root/oddhobbies/db/oddhobbies.db")

VOCAB = [
    ("role", "hero", "Main product shot for listing first image"),
    ("role", "lifestyle", "Product in context / with person"),
    ("role", "detail", "Close-up texture / engraving / feature"),
    ("role", "size_chart", "Scale / dimensions graphic"),
    ("role", "mockup", "Generated or flat product card"),
    ("role", "pin", "Pinterest-optimised crop"),
    ("role", "process", "How it's made / personalisation step"),
    ("role", "packaging", "Box / unboxing"),
    ("scene", "xmas_tree", "Christmas tree or festive decor"),
    ("scene", "desk", "Desk / workspace"),
    ("scene", "hand_hold", "Held in hand for scale"),
    ("scene", "couple", "Two people / couple context"),
    ("scene", "flat_lay", "Flat overhead layout"),
    ("scene", "studio_white", "Clean studio background"),
    ("scene", "bokeh_lights", "Festive bokeh lights background"),
    ("product_family", "brick_figure", "Block-style character figure"),
    ("product_family", "pet_chibi", "Chibi pet figurine"),
    ("product_family", "ornament", "Hanging ornament"),
    ("product_family", "game_night", "Board game accessories"),
    ("product_family", "album", "Memory/wedding album products"),
    ("product_family", "flat_print", "Cards, stickers, paper"),
    ("composition", "single_product", "Only the product in frame"),
    ("composition", "person_plus_product", "Person with product"),
    ("composition", "product_in_hand", "Product held, face optional"),
    ("composition", "environment", "Product in scene"),
    ("mood", "festive", "Christmas / holiday"),
    ("mood", "playful", "Fun, gift-like"),
    ("mood", "premium", "Elevated, gift-quality"),
    ("mood", "cosy", "Warm, homey"),
    ("mood", "clean", "Neutral product focus"),
]

# asset_key patterns -> labels
LABELS_BY_PATH = [
    # Etsy brick figure
    (
        "ACTIVE-BRICK-FIGURE",
        {
            "role": "lifestyle",
            "product_family": "brick_figure",
            "scene": "hand_hold",
            "composition": "product_in_hand",
            "mood": "festive",
            "visibility": "product_clear",
            "has_person": 1,
            "has_pet": 0,
            "colour_tags": "blue,white,yellow,green,red",
            "aspect": "1:1",
            "source": "etsy_import",
            "confidence": "high",
            "agent_blurb": "Young man in white tee holding a small LEGO-style brick figure, Christmas tree bokeh behind — scale + gift context for custom brick figures.",
            "agent_keywords": "brick figure,lego style,custom figure,christmas gift,pet figure,hand scale",
            "suitability": {"etsy_hero": True, "etsy_lifestyle": True, "pinterest": True, "shopify_gallery": True, "agent_default": True},
        },
    ),
    (
        "ACTIVE-COUPLE-FIGURE",
        {
            "role": "lifestyle",
            "product_family": "brick_figure",
            "scene": "couple",
            "composition": "person_plus_product",
            "mood": "festive",
            "visibility": "product_clear",
            "has_person": 1,
            "has_pet": 0,
            "colour_tags": "cream,blue,brown,red,gold",
            "aspect": "1:1",
            "source": "etsy_import",
            "confidence": "high",
            "agent_blurb": "Couple holding a two-brick-figure couple on a black base, Christmas gifts in background — weddings/anniversary couple SKU context.",
            "agent_keywords": "couple figure,wedding gift,anniversary,customer photo,brick couple,christmas",
            "suitability": {"etsy_hero": False, "etsy_lifestyle": True, "pinterest": True, "shopify_gallery": True, "weddings_section": True},
        },
    ),
    (
        "ACTIVE-XMAS-ORNAMENT",
        {
            "role": "lifestyle",
            "product_family": "ornament",
            "scene": "xmas_tree",
            "composition": "environment",
            "mood": "festive",
            "visibility": "product_clear",
            "has_person": 0,
            "has_pet": 1,
            "colour_tags": "gold,cream,red,green",
            "aspect": "1:1",
            "source": "etsy_import",
            "confidence": "high",
            "agent_blurb": "Golden chibi puppy Christmas ornament with red ribbon hanging on a lit tree — hero lifestyle for Xmas pet ornament.",
            "agent_keywords": "christmas ornament,pet ornament,dog bauble,tree,hanging loop,stocking stuffer",
            "suitability": {"etsy_hero": True, "etsy_lifestyle": True, "pinterest": True, "shopify_gallery": True, "xmas": True},
        },
    ),
    # Local mockups
    (
        "product_previews_ornament_preview",
        {
            "role": "mockup",
            "product_family": "ornament",
            "scene": "flat_lay",
            "composition": "single_product",
            "mood": "clean",
            "visibility": "product_clear",
            "has_person": 0,
            "has_pet": 0,
            "colour_tags": "orange,brown,white,black",
            "aspect": "1:1",
            "source": "local_mock",
            "confidence": "medium",
            "agent_blurb": "Flat product card: PET ORNAMENT $14.99, 7cm PLA hanging loop — info graphic not photo.",
            "agent_keywords": "mockup,price card,ornament,7cm,plA,product card",
            "suitability": {"etsy_hero": False, "pinterest": False, "shopify_gallery": False, "internal_spec": True},
        },
    ),
    (
        "product_previews_figure_preview",
        {
            "role": "mockup",
            "product_family": "brick_figure",
            "scene": "flat_lay",
            "composition": "single_product",
            "mood": "clean",
            "visibility": "product_clear",
            "has_person": 0,
            "has_pet": 0,
            "colour_tags": "orange,brown,white,black",
            "aspect": "1:1",
            "source": "local_mock",
            "confidence": "medium",
            "agent_blurb": "Flat product card: BRICK FIGURE $19.99, 8cm PLA display base + add-ons — info graphic.",
            "agent_keywords": "mockup,price card,brick figure,8cm,add-on,product card",
            "suitability": {"etsy_hero": False, "pinterest": False, "internal_spec": True},
        },
    ),
]


def main() -> None:
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    schema = Path("/root/oddhobbies/db/schema_asset_labels.sql").read_text()
    # only apply CREATE/VOCAB parts safely; columns already added once
    existing = {r[1] for r in conn.execute("PRAGMA table_info(assets)")}
    for stmt in schema.split(";"):
        s=stmt.strip()
        if not s or s.upper().startswith("PRAGMA"):
            continue
        if s.upper().startswith("ALTER TABLE ASSETS ADD COLUMN"):
            col=s.split("ADD COLUMN",1)[1].split()[0]
            if col in existing:
                continue
        try:
            conn.executescript(s+";")
        except sqlite3.OperationalError as e:
            if "duplicate column" not in str(e).lower():
                raise

    for vocab, value, desc in VOCAB:
        conn.execute(
            "INSERT OR IGNORE INTO asset_vocab (vocab, value, description) VALUES (?,?,?)",
            (vocab, value, desc),
        )

    # default unlabelled
    conn.execute(
        """UPDATE assets SET
             role = COALESCE(role, 'mockup'),
             product_family = COALESCE(product_family, 'brick_figure'),
             scene = COALESCE(scene, 'flat_lay'),
             composition = COALESCE(composition, 'single_product'),
             mood = COALESCE(mood, 'clean'),
             visibility = COALESCE(visibility, 'product_clear'),
             has_person = COALESCE(has_person, 0),
             has_pet = COALESCE(has_pet, 0),
             source = COALESCE(source, CASE WHEN asset_key LIKE 'etsy-%' THEN 'etsy_import' ELSE 'local_mock' END),
             confidence = COALESCE(confidence, 'low'),
             needs_review = 1
           WHERE role IS NULL"""
    )

    labelled = 0
    for row in conn.execute("SELECT id, asset_key, path_or_url FROM assets").fetchall():
        key = row["asset_key"] or ""
        path = row["path_or_url"] or ""
        blob = None
        for needle, labels in LABELS_BY_PATH:
            if needle.lower() in key.lower() or needle.lower() in path.lower():
                blob = labels
                break
        if not blob:
            continue
        conn.execute(
            """UPDATE assets SET
                 role=?, product_family=?, scene=?, composition=?, mood=?, visibility=?,
                 has_person=?, has_pet=?, colour_tags=?, aspect=?, source=?, confidence=?,
                 agent_blurb=?, agent_keywords=?, suitability_json=?, needs_review=0
               WHERE id=?""",
            (
                blob["role"],
                blob["product_family"],
                blob["scene"],
                blob["composition"],
                blob["mood"],
                blob["visibility"],
                blob["has_person"],
                blob["has_pet"],
                blob["colour_tags"],
                blob["aspect"],
                blob["source"],
                blob["confidence"],
                blob["agent_blurb"],
                blob["agent_keywords"],
                json.dumps(blob["suitability"]),
                row["id"],
            ),
        )
        labelled += 1

    conn.commit()
    print("vocab", conn.execute("SELECT COUNT(*) FROM asset_vocab").fetchone()[0])
    print("labelled high/med", labelled)
    print("needs_review", conn.execute("SELECT COUNT(*) FROM assets WHERE needs_review=1").fetchone()[0])
    print("\n--- agent catalog sample ---")
    for r in conn.execute(
        """SELECT sku, role, scene, agent_blurb FROM v_asset_catalog
           WHERE agent_blurb IS NOT NULL LIMIT 8"""
    ):
        print(f"  [{r['role']}/{r['scene']}] {r['sku']}: {r['agent_blurb'][:80]}")
    print("\n--- pick scores ---")
    for r in conn.execute(
        """SELECT asset_key, etsy_score, pinterest_score FROM v_asset_pick
           WHERE product_family IN ('brick_figure','ornament') ORDER BY etsy_score DESC LIMIT 6"""
    ):
        print(f"  {r['asset_key']}: etsy={r['etsy_score']} pin={r['pinterest_score']}")
    conn.close()


if __name__ == "__main__":
    main()

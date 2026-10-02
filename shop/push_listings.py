#!/usr/bin/env python3
"""Push listing packs to a channel for a store.

Usage:
  python3 shop/push_listings.py --store pogpet --channel shopify --dry-run
  python3 shop/push_listings.py --store pogpet --channel shopify --sku XMAS-3D-ORNAMENT
  python3 shop/push_listings.py --list --store pogpet --channel shopify

Reads stores/<store_id>/listings/*.json (not legacy shop/listings).
Writes shopify_product_id back into the pack when create succeeds.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_VERSION = "2026-10"


def vault(key: str) -> str:
    try:
        return subprocess.check_output(
            ["agent-vault", "vault", "credential", "get", key, "--vault", "oracle"],
            text=True,
        ).strip()
    except Exception:
        return os.environ.get(key, "").strip()


def load_env_file(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.exists():
        return out
    for line in path.read_text().splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def shopify_config() -> tuple[str, str]:
    domain = vault("SHOPIFY_SHOP_DOMAIN")
    token = vault("SHOPIFY_ACCESS_TOKEN")
    env_file = Path.home() / ".config" / "oddhobbies" / "shopify.env"
    file_env = load_env_file(env_file)
    domain = domain or file_env.get("SHOPIFY_SHOP_DOMAIN", "")
    token = token or file_env.get("SHOPIFY_ACCESS_TOKEN", "")
    if not domain or not token:
        raise SystemExit("Missing SHOPIFY_SHOP_DOMAIN or SHOPIFY_ACCESS_TOKEN")
    if "://" not in domain:
        domain = f"https://{domain}"
    return domain.rstrip("/"), token


def api(method: str, path: str, token: str, domain: str, body: dict | None = None):
    url = f"{domain}/admin/api/{API_VERSION}{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "X-Shopify-Access-Token": token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode()
            return resp.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {"error": raw[:500]}


def slug(s: str) -> str:
    out, prev = [], "-"
    for ch in (s or "product").lower():
        if ch.isalnum():
            out.append(ch)
            prev = ch
        elif prev != "-":
            out.append("-")
            prev = "-"
    return "".join(out).strip("-") or "product"


def pack_to_shopify(pack: dict, store: dict, status: str = "draft") -> dict:
    title = pack.get("etsy_title") or pack.get("sku")
    desc = pack.get("description") or ""
    body = "<p>" + desc.replace("\n\n", "</p><p>").replace("\n", "<br>") + "</p>"
    tags = pack.get("tags") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    price = pack.get("price") or 19.99
    sku = pack.get("sku")
    channel_ccy = (store.get("channel_currencies") or {}).get("shopify") or store.get("currency") or "USD"
    # packs store display price in store currency; do not auto-convert
    grams = 120
    if "CRIBBAGE-BOARD" in sku or "TOKEN-TRAY" in sku:
        grams = 400
    elif "ALBUM" in sku:
        grams = 100
    elif "TILE-RACK" in sku or "WINDS" in sku:
        grams = 150
    elif pack.get("make") == "digital":
        grams = 0
    vendor = store.get("shopify_store_name") or store.get("store_name") or "OddHobbies"
    return {
        "product": {
            "title": title,
            "body_html": body,
            "vendor": vendor,
            "product_type": pack.get("section") or "Gift",
            "tags": ", ".join(tags),
            "status": status,
            "handle": slug(sku),
            "variants": [
                {
                    "option1": "Default Title",
                    "price": f"{float(price):.2f}",
                    "sku": sku,
                    "grams": grams,
                    "inventory_management": "shopify" if pack.get("make") != "digital" else None,
                    "inventory_policy": "continue",
                    "fulfillment_service": "manual",
                    "requires_shipping": pack.get("make") != "digital",
                    "taxable": True,
                }
            ],
            "metafields": [
                {
                    "namespace": "commerce",
                    "key": "store_id",
                    "value": store.get("store_id"),
                    "type": "single_line_text_field",
                },
                {
                    "namespace": "commerce",
                    "key": "sku",
                    "value": sku,
                    "type": "single_line_text_field",
                },
            ],
        },
        "_currency_note": channel_ccy,
    }


def load_store(store_id: str) -> dict:
    path = ROOT / "stores" / store_id / "store.json"
    if not path.exists():
        raise SystemExit(f"missing store pack: {path}")
    return json.loads(path.read_text())


def load_packs(store_id: str, skus: list[str] | None) -> list[Path]:
    listing_dir = ROOT / "stores" / store_id / "listings"
    if not listing_dir.exists():
        return []
    paths = []
    for path in sorted(listing_dir.glob("*.json")):
        if path.name.startswith("_") or path.name == "TEMPLATE-SKU.json":
            continue
        pack = json.loads(path.read_text())
        if pack.get("sku") == "TEMPLATE-SKU":
            continue
        if skus and pack.get("sku") not in skus:
            continue
        paths.append(path)
    return paths


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", default="pogpet")
    ap.add_argument("--channel", default="shopify", choices=["shopify"])
    ap.add_argument("--sku", action="append", dest="skus")
    ap.add_argument("--status", default="draft", choices=["draft", "active"])
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    store = load_store(args.store)
    print(f"store={args.store} brand={store.get('brand_id')} currency={store.get('currency')}")

    if args.channel == "shopify":
        domain, token = shopify_config()
        print(f"Shop: {domain}")
        if args.list:
            st, body = api("GET", "/products.json?limit=250&fields=id,title,handle,status", token, domain)
            print("status", st)
            for p in body.get("products", []):
                print(f"  {p['id']} [{p.get('status')}] {p.get('handle')} | {p.get('title')[:60]}")
            return 0 if st < 400 else 1
        paths = load_packs(args.store, args.skus)
        print(f"Packs: {len(paths)} status={args.status}")
        if not paths:
            print("No packs found")
            return 1
        created = 0
        for path in paths:
            pack = json.loads(path.read_text())
            payload = pack_to_shopify(pack, store, status=args.status)
            sku = pack["sku"]
            if args.dry_run:
                print("DRY", sku, payload["product"]["title"][:50], payload["product"]["variants"][0]["price"])
                continue
            # skip if already has shopify id unless force later
            st, body = api("POST", "/products.json", token, domain, payload)
            pid = body.get("product", {}).get("id") if isinstance(body, dict) else None
            handle = body.get("product", {}).get("handle") if isinstance(body, dict) else None
            print(f"{st} {sku} -> id={pid} handle={handle}")
            if st >= 400:
                print("  ", body)
            else:
                created += 1
                pack["store_id"] = args.store
                pack["shopify_product_id"] = pid
                pack["shopify_handle"] = handle
                pack["shopify_status"] = args.status
                path.write_text(json.dumps(pack, indent=2, ensure_ascii=False) + "\n")
        print(f"Created: {created}/{len(paths)}")
        return 0 if created or args.dry_run else 1

    print("Only shopify channel implemented for push_listings.py")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Push listing packs to Shopify as draft products (Admin API).

Setup (Shopify admin):
1. Settings → Apps and sales channels → Develop apps → Create app
2. Name: oddhobbies-api
3. Configure Admin API scopes: read_products, write_products
4. Install app → reveal Admin API access token (shpat_...)
5. Store domain: your-store.myshopify.com

Put in agent-vault (preferred):
  SHOPIFY_SHOP_DOMAIN
  SHOPIFY_ACCESS_TOKEN
Or export env vars / write ~/.config/oddhobbies/shopify.env (not git).

Usage:
  python3 shopify_push.py                 # all listing packs
  python3 shopify_push.py --sku XMAS-3D-TILE-RACK
  python3 shopify_push.py --list          # list existing products
  python3 shopify_push.py --status active # push as active (default draft)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKS = ROOT / "shop" / "listings"
API_VERSION = "2026-10"


def vault(key: str) -> str:
    try:
        return subprocess.check_output(
            ["agent-vault", "vault", "credential", "get", key, "--vault", "oracle"],
            text=True,
        ).strip()
    except Exception:
        return os.environ.get(key, "").strip()


def load_config() -> tuple[str, str]:
    domain = vault("SHOPIFY_SHOP_DOMAIN")
    token = vault("SHOPIFY_ACCESS_TOKEN")
    env_file = Path.home() / ".config" / "oddhobbies" / "shopify.env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                k, v = k.strip(), v.strip().strip('"').strip("'")
                if k == "SHOPIFY_SHOP_DOMAIN" and not domain:
                    domain = v
                if k == "SHOPIFY_ACCESS_TOKEN" and not token:
                    token = v
    if not domain or not token:
        raise SystemExit(
            "Missing SHOPIFY_SHOP_DOMAIN or SHOPIFY_ACCESS_TOKEN.\n"
            "Create a custom app in Shopify Admin → Develop apps → Admin API token (shpat_...).\n"
            "Set vault keys or ~/.config/oddhobbies/shopify.env"
        )
    if "://" not in domain:
        domain = f"https://{domain}"
    domain = domain.rstrip("/")
    return domain, token


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


def pack_to_shopify_product(pack: dict, status: str = "draft") -> dict:
    title = pack.get("etsy_title") or pack.get("sku")
    desc = pack.get("description") or ""
    # light HTML
    body = "<p>" + desc.replace("\n\n", "</p><p>").replace("\n", "<br>") + "</p>"
    tags = pack.get("tags") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    price = pack.get("price") or 19.99
    sku = pack.get("sku")
    grams = 120
    if "CRIBBAGE-BOARD" in sku or "TOKEN-TRAY" in sku:
        grams = 400
    elif "ALBUM" in sku:
        grams = 100
    elif "TILE-RACK" in sku or "WINDS" in sku:
        grams = 150
    return {
        "product": {
            "title": title,
            "body_html": body,
            "vendor": "OddHobbies",
            "product_type": pack.get("shop_section_target") or pack.get("section") or "Gift",
            "tags": ", ".join(tags),
            "status": status,
            "handle": slug(sku),
            "variants": [
                {
                    "option1": "Default Title",
                    "price": f"{float(price):.2f}",
                    "sku": sku,
                    "grams": grams,
                    "inventory_management": "shopify",
                    "inventory_policy": "continue",
                    "fulfillment_service": "manual",
                    "requires_shipping": True,
                    "taxable": True,
                }
            ],
            "metafields": [
                {
                    "namespace": "oddhobbies",
                    "key": "sku",
                    "value": sku,
                    "type": "single_line_text_field",
                }
            ],
        }
    }


def load_packs(skus: list[str] | None) -> list[dict]:
    packs = []
    for path in sorted(PACKS.glob("*.json")):
        if path.name.startswith("_"):
            continue
        try:
            pack = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue
        if not isinstance(pack, dict) or "sku" not in pack:
            continue
        if skus and pack.get("sku") not in skus:
            continue
        packs.append(pack)
    return packs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sku", action="append", dest="skus")
    ap.add_argument("--status", default="draft", choices=["draft", "active"])
    ap.add_argument("--list", action="store_true", help="list products only")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    domain, token = load_config()
    print(f"Shop: {domain}")

    if args.list:
        st, body = api("GET", "/products.json?limit=250&fields=id,title,handle,status", token, domain)
        print("status", st)
        for p in body.get("products", []):
            print(f"  {p['id']} [{p.get('status')}] {p.get('handle')} | {p.get('title')[:60]}")
        return 0 if st < 400 else 1

    packs = load_packs(args.skus)
    print(f"Packs to push: {len(packs)} status={args.status}")
    if not packs:
        print("No packs found in", PACKS)
        return 1

    created = 0
    for pack in packs:
        payload = pack_to_shopify_product(pack, status=args.status)
        sku = pack["sku"]
        if args.dry_run:
            print("DRY", sku, payload["product"]["title"][:50], payload["product"]["variants"][0]["price"])
            continue
        st, body = api("POST", "/products.json", token, domain, payload)
        pid = body.get("product", {}).get("id") if isinstance(body, dict) else None
        handle = body.get("product", {}).get("handle") if isinstance(body, dict) else None
        print(f"{st} {sku} -> id={pid} handle={handle}")
        if st >= 400:
            print("  ", body)
        else:
            created += 1
            # record
            pack["shopify_product_id"] = pid
            pack["shopify_handle"] = handle
            pack["shopify_status"] = args.status
            (PACKS / f"{sku}.json").write_text(json.dumps(pack, indent=2))
    print(f"Created/updated: {created}/{len(packs)}")
    return 0 if created else 1


if __name__ == "__main__":
    sys.exit(main())

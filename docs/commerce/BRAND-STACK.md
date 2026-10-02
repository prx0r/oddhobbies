# Brand stack — how commerce + cmail + stevejobless fit

> Domains live on Cloudflare. Products live in the commerce graph.
> Mail lands in cmail. Desired-vs-observed lives in stevejobless.
> Influence runs social/content passports on the same identity rails.

---

## One sentence

Each store is an **identity** (domain + email + socials + channel accounts) plus a **product graph** (catalog + assets + listings + ads + sales); cmail is the **inbox bus**, stevejobless is the **setup reconciler**, commerce is the **truth for what we sell**, influence is the **ops/content plane**.

---

## Stack map

```
                    CLOUDFLARE (identity + edge)
         zones · DNS · Email Routing · R2 · Workers · tunnels
                    │
        ┌───────────┼───────────┬─────────────────┐
        ▼           ▼           ▼                 ▼
   oddhobb.com  grimoirer.com  stonedoorway.com  pog.pet
   hello@       hello@         hello@            hello@
   orders@      orders@        orders@           orders@
        │           │           │                 │
        └───────────┴─────┬─────┴─────────────────┘
                          ▼
                   CMAIL (edge bus)
              MX → Worker → D1 drafts → MCP
              quarantine · classify · human confirm
                          │
              ┌───────────┼──────────────┐
              ▼           ▼              ▼
        stevejobless   influence      commerce MCP
        passports      content/ads    products/orders
        reconcile      order tasks    assets/sales
              │           │              │
              └───────────┴──────┬───────┘
                                 ▼
                    SHOP / ETSY / ADS (doors)
                    Shopify · Etsy · Pinterest
```

---

## Per-store identity (definitive)

| Store | Primary domain | Zone | Email | Commerce store_id |
|-------|----------------|------|-------|-------------------|
| **OddHobb** | **oddhobb.com** | active | hello@oddhobb.com · orders@oddhobb.com | `oddhobb` |
| **Grimoirer** | **grimoirer.com** | active | hello@grimoirer.com · orders@grimoirer.com | `grimoirer` |
| **StoneDoorway** | **stonedoorway.com** | active | hello@stonedoorway.com · orders@stonedoorway.com | `stonedoorway` |

MX: `route1/2/3.mx.cloudflare.net` · Email Routing **ready** on all three  
Forward: `tradesprior@gmail.com` → cmail later  
**Shared phone:** `+44 7822 000802` (Telnyx · all brands) — `docs/commerce/SHARED-PHONE.md`

**No PogPet store. No Ochemy store.** Legacy Etsy draft IDs may remain in channel rows as `etsy:legacy_pogpet` — public brand is OddHobb.

Full CF dump: `docs/commerce/CF-EMAIL-ROUTING.json` · NS: `CF-NAMESERVERS.md` · Socials: `SOCIALS.md`


---

## What each system owns

| System | Owns | Does not own |
|--------|------|--------------|
| **Cloudflare** | Zones, NS, DNS, Email Routing, R2 assets, tunnels | Product truth |
| **Commerce core** (`oddhobbies/db/commerce.db`) | Products, packs, listings, assets labels, ads, sales, agent catalog | Social posts, email bodies |
| **cmail** | Inbound mail, quarantine, drafts queue, MCP email tools | Catalog prices |
| **stevejobless** | Studio passport per project/domain, reconcile READY/MISSING, human task queue | Product manufacturing |
| **influence** | Content passports, gated publish, storefront order-queue patterns, identity slots | Unit costs |
| **Shopify / Etsy** | Checkout + channel listings | Our graph |

---

## Dependency graph (influence L0–L7 → our stores)

```
L0  law / grants / receipts          (qprivately / qp)
L1  observe  zone.read · domain.verify · mailbox.check · social.read
L2  acquire  zone.move · mailbox.create · social.claim   [human-gated]
L3  make     listing drafts · image renders · pin copy
L4  send     mail.send · post.publish · ads launch       [human-gated]
L5  judge    listing quality · ad creative · price sanity
L6  learn    margin · conversion · content performance
L7  endpoints  store() · brand() · agent() · customer()
```

**We just did L1–L2 for three brands:** zones active, NS set, MX + hello@ rules live.  
Next L2 pieces: social handle claims, Shopify stores for ochema/stonedoorway, Etsy OAuth for PogPet.  
L3–L4: photos, listing push, first ads — all gated human confirms.

---

## stevejobless passport shape (one per store)

Steve’s model: **desired state vs observed state** → human queue.

```json
{
  "version": 1,
  "product": {"name": "Ochema", "store_id": "ochema"},
  "resources": [
    {"key": "domain", "kind": "domain", "label": "Domain owned",
     "desired": {"domain": "grimoirer.com", "cloudflare_zone_id": "3b0d…"}},
    {"key": "email", "kind": "email", "label": "hello@ live",
     "desired": {"address": "hello@grimoirer.com", "forward": "operator"}},
    {"key": "website", "kind": "website", "label": "Site up",
     "desired": {"url": "https://grimoirer.com"}},
    {"key": "shopify", "kind": "integration", "label": "Shopify store",
     "desired": {"status": "missing"}},
    {"key": "etsy", "kind": "integration", "label": "Etsy shop",
     "desired": {"status": "missing"}},
    {"key": "pinterest", "kind": "social", "label": "Pinterest",
     "desired": {"handle": "@ochema"}},
    {"key": "catalog", "kind": "commerce", "label": "5 SKUs in graph",
     "desired": {"store_id": "ochema", "min_products": 5}}
  ]
}
```

Reconcile should say:

| Resource | Expected observation |
|----------|----------------------|
| domain | NS = gina+pete, zone active |
| email | MX present + rule `hello@…` enabled |
| website | HTTP(S) or pending deploy |
| shopify / etsy | channel row + credentials |
| catalog | `v_stores.product_count` from commerce.db |

Human tasks stay small: “claim Pinterest”, “create Shopify”, “upload photos”, “approve ad spend”.

---

## cmail role (inbox bus)

**Today (good enough):**  
Cloudflare Email Routing → forward to operator Gmail.  
You can reply as `hello@grimoirer.com` from Gmail (Gmail “send as” optional later).

**Tomorrow (cmail cut-over):**

```
hello@brand.com
  → CF Email Routing → cmail.tradesprior.workers.dev
  → quarantine → classify → draft reply
  → human confirm → send
```

Rules from influence AGENTS.md still hold:
- Untrusted mail never calls tools directly  
- Drafts everywhere; sends need human confirm  
- Quarantine can only downgrade  

Per-brand routing = same cmail worker, different `to` addresses → business slug / store_id in the payload.

---

## How it comes together (the product loop)

```
1. IDENTITY
   domain + hello@ + socials + brand voice     [CF + passport]

2. CATALOG
   packs in stores/<id>/ → commerce.db         [oddhobbies engine]
   assets in R2 commerce/stores/<id>/...

3. DOORS
   Shopify / Etsy listings from packs
   custom domain: oddhobb.com → Shopify
   grimoirer.com / stonedoorway.com → placeholder → store later

4. DEMAND
   Pinterest + brand content (influence)
   ads from ad_creatives bound to product_id

5. INBOX
   orders@ + hello@ → cmail → order tasks / support drafts

6. MONEY
   orders in commerce.db → margin vs product_costs
   payouts later under money-proof grants

7. LEARN
   sales_summary + ad_spend_ledger + content analytics
   kill or scale per store
```

---

## Parallel 3-store build (same rails)

| Track | pogpet | ochema | stonedoorway |
|-------|--------|--------|--------------|
| Domain | oddhobb.com ✅ | grimoirer.com ✅ | stonedoorway.com ✅ |
| Email | hello@ ✅ | hello@ ✅ | hello@ ✅ |
| Products | 15 packs ✅ | 4 packs ✅ | 0 (thesis) |
| Channel | Shopify drafts | create Shopify/Etsy | wait |
| Photos | blocker | blocker | wait thesis |
| Content | gift/Pinterest | grimoire explainers | — |
| Ads | after photos | after photos | — |

**Do not** build three cmails, three commerce DBs, or three passport engines.

---

## Immediate next steps (in order)

1. **Claim socials** — X `@oddhobb` · `@ochemahq` · `@stonedoorway` (API-available); browser-check IG/Pinterest — see `docs/commerce/SOCIALS.md` + `stores/*/SOCIALS.md`  
2. **Confirm email** — send test to hello@ on each domain  
3. **Placeholder sites** — CF Worker/Pages per domain  
4. **Shopify** — connect oddhobb.com as custom domain  
5. **stevejobless seed** — three passports (domain/email/socials/catalog)  
6. **cmail cut-over** — Gmail forward → cmail when ready  
7. **Photos + first ads** on pogpet and ochema only  


---

## Hard rules

1. Secrets stay in vault — never in passports, packs, or chat logs  
2. Sends/spends always human-gated  
3. Commerce graph is product truth; passports are setup truth  
4. Email addresses are identity endpoints, not authority  
5. stonedoorway stays non-commerce until thesis + packs exist  
6. One CF account, one vault, many brands — no per-brand token sprawl  

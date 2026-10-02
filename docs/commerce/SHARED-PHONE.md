# Shared phone + guaranteed hello@ emails

Date: 2026-10-02

---

## Email — all three stores READY

Cloudflare Email Routing **enabled + status=ready** on:

| Domain | hello@ | orders@ | MX | Forward |
|--------|--------|---------|-----|---------|
| **oddhobb.com** | hello@oddhobb.com | orders@oddhobb.com | route1/2/3.mx.cloudflare.net | tradesprior@gmail.com |
| **grimoirer.com** | hello@grimoirer.com | orders@grimoirer.com | route1/2/3.mx.cloudflare.net | tradesprior@gmail.com |
| **stonedoorway.com** | hello@stonedoorway.com | orders@stonedoorway.com | route1/2/3.mx.cloudflare.net | tradesprior@gmail.com |

**Guaranteed working path:**

```
someone@ → MX Cloudflare → routing rule → tradesprior@gmail.com
you reply as hello@brand.com from Gmail (Settings → Accounts → Send mail as)
```

### Test (do this once per brand)

1. Send mail **to** `hello@oddhobb.com` (and grimoirer / stonedoorway)
2. Confirm it lands in **tradesprior@gmail.com**
3. Reply **from** hello@… (add “Send mail as” in Gmail if not already)

If mail doesn’t arrive: check Gmail spam + Cloudflare dashboard → Email Routing → Logs.

### Later cut-over (cmail)

When cmail is wired for brands, change forward target from Gmail → cmail worker.
Same addresses — only the destination changes.

---

## Shared phone — one number for all three brands

| Field | Value |
|-------|--------|
| Provider | Telnyx |
| **Number** | **+44 7822 000802** |
| Type | GB mobile |
| Connection | QuickCall SIP `3030047971774301870` |
| Messaging profile | QuickCall `4001a0d8-bd38-4c90-98e9-79fc8d6fc01a` |
| Tags on number | `shared` · `oddhobb` · `grimoirer` · `stonedoorway` |
| Customer ref | brand-family-shared |
| **Status** | **`requirement-info-exception`** — KYC/info may be required in Telnyx portal before SMS/voice fully activate |

### How brands share it

| Brand | Contact on site / socials |
|-------|---------------------------|
| OddHobb | +44 7822 000802 · hello@oddhobb.com |
| Grimoirer | +44 7822 000802 · hello@grimoirer.com |
| StoneDoorway | +44 7822 000802 · hello@stonedoorway.com |

One ops inbox + one phone = three brand identities on the public surface.
Dispatch/routing by email domain or order notes (which store the customer contacted).

### Vault keys

| Key | Where |
|-----|--------|
| `TELNYX_API_KEY` | agent-vault oracle |
| `SHARED_PHONE_NUMBER` | set → `+447822000802` |
| `TELNYX_CONNECTION_ID` | `3030047971774301870` |
| `TELNYX_MESSAGING_PROFILE_ID` | `4001a0d8-bd38-4c90-98e9-79fc8d6fc01a` |

### Human blocker

Telnyx number status **`requirement-info-exception`** — open Telnyx Mission Control → Numbers / Account → complete any required business info so the number activates for SMS/voice.

Connection is already assigned. Tags mark it as brand-family shared.

---

## Public contact pattern (copy per store)

```
Email:  hello@<domain>
Phone:  +44 7822 000802
Site:   https://<domain>
```

---

## Related

- `docs/commerce/BRAND-STACK.md`
- `stores/*/IDENTITY.md`
- `docs/commerce/CF-EMAIL-ROUTING.json`

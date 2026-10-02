# Spaceship → Cloudflare nameservers

Account: `954612afb5a97bb15dddcdc70176813d`  
Zones created 2026-10-02 · status **pending** until NS set at Spaceship.

---

## Paste these in Spaceship (most likely domains)

### grimoirer.com
```text
gina.ns.cloudflare.com
pete.ns.cloudflare.com
```

### stonedoorway.com
```text
gina.ns.cloudflare.com
pete.ns.cloudflare.com
```

### Already active on Cloudflare (if you use these instead)

| Domain | Nameservers |
|--------|-------------|
| **grimoirer.com** | `gina.ns.cloudflare.com` · `pete.ns.cloudflare.com` |
| **oddhobb.com** | `gina.ns.cloudflare.com` · `pete.ns.cloudflare.com` |
| **pog.pet** | `gina.ns.cloudflare.com` · `pete.ns.cloudflare.com` |

---

## Extra zones created (only if you bought these TLDs)

| Domain | Nameservers |
|--------|-------------|
| grimoirer.co | `ariadne.ns.cloudflare.com` · `burt.ns.cloudflare.com` |
| stonedoorway.co | `ariadne.ns.cloudflare.com` · `burt.ns.cloudflare.com` |
| grimoirer.xyz | `ariadne.ns.cloudflare.com` · `burt.ns.cloudflare.com` |
| stonedoorway.xyz | `ariadne.ns.cloudflare.com` · `burt.ns.cloudflare.com` |

Use **only** the pair for the domain you actually bought in Spaceship.

---

## Zone IDs

| Domain | zone_id |
|--------|---------|
| grimoirer.com | `3b0ddcea9c15b0de55a8b349dd31c89d` |
| stonedoorway.com | `fb5d6107f3ba0ec36985b046d4c91570` |
| grimoirer.co | `75691574ab3a9fedff60c4d78feaf010` |
| stonedoorway.co | `540a76f3c6f32073134f7edd561b8b55` |
| grimoirer.xyz | `20450c2f217d2c207e1042ca71331587` |
| stonedoorway.xyz | `030984f922d0781246044103a3224680` |

---

## Status after setup (2026-10-02)

| Domain | Zone | NS | Email hello@/orders@ |
|--------|------|----|----------------------|
| grimoirer.com | **active** | gina + pete | ✅ rules live |
| stonedoorway.com | **active** | gina + pete | ✅ rules live |
| oddhobb.com | **active** | gina + pete | ✅ rules live |
| grimoirer.com | **active** | gina + pete | ✅ rules live |
| pog.pet | **active** | gina + pete | ✅ rules live |

Forward target today: operator Gmail (vault).  
Cut over to cmail later: `docs/commerce/BRAND-STACK.md`.

See also: `CF-EMAIL-ROUTING.json`, `stores/*/IDENTITY.md`.

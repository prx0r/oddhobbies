# Stores — definitive brand family

**Three stores only. No PogPet. No Ochemy as store names.**

| store_id | Brand | Domain | Email | Socials |
|----------|-------|--------|-------|---------|
| **oddhobb** | OddHobb | oddhobb.com | hello@oddhobb.com | @oddhobb |
| **grimoirer** | Grimoirer | grimoirer.com | hello@grimoirer.com | @grimoirerhq |
| **stonedoorway** | StoneDoorway | stonedoorway.com | hello@stonedoorway.com | @stonedoorway |

## Pack layout

```
stores/<store_id>/
  store.json       identity + channels + style lock
  IDENTITY.md      human map
  SOCIALS.md       handle claim matrix
  listings/        one JSON pack per SKU
```

## Hard rules

1. **store_id ∈ {oddhobb, grimoirer, stonedoorway}** — nothing else
2. Brand voice never mixes across stores
3. No secrets in packs
4. Legacy Etsy draft IDs may exist under old shop rows — public brand is OddHobb
5. Grimoirer SKUs are `GRIMOIRER-*`
6. StoneDoorway stays empty until thesis

## Seed / graph

```bash
python3 db/seed_store.py --reset
python3 db/export_graph.py
```

## Docs

- Architecture: `docs/commerce/COMMERCE-GRAPH.md`
- System map: `docs/commerce/BRAND-STACK.md`
- Socials: `docs/commerce/SOCIALS.md`
- CF NS/email: `docs/commerce/CF-NAMESERVERS.md`
- Agent playbook: `docs/commerce/AGENT-PLAYBOOK.md`

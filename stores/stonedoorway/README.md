# StoneDoorway — placeholder store

**Status:** empty · **Not ready for listing packs until thesis exists.**

## What this store is

Unknown. This directory is the multi-store scaffold so StoneDoorway can plug into
the same commerce engine as PogPet and Ochema the moment the brand is defined.

## Blockers (in order)

1. **Thesis** — one line: who it's for + what we sell
2. **Sections** — buying occasions, not a copy of another store
3. **Style lock** — background, light, props, avoid list
4. **First SKUs** — 1–3 packs under `listings/` (delete `TEMPLATE-SKU.json`)
5. **Channels** — Etsy/Shopify only when credentials exist
6. **Seed + graph**

```bash
# after real packs exist:
python3 db/seed_store.py --store stonedoorway
python3 db/export_graph.py --store stonedoorway
```

## Do not

- Invent products without a thesis
- Copy PogPet Christmas energy or Ochema occult voice
- Push to any channel with placeholder copy

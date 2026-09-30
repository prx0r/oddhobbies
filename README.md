# OddHobbies

> Accessories that fix the friction in the things you love.

## What This Is

OddHobbies makes accessories for hobbies that have gaps — where the branded standard doesn't quite work, where accessibility is an afterthought, or where the only option is a mass-produced thing that doesn't fit your setup.

We don't make the hobby. We make the thing that makes the hobby better.

## The Pattern

Every product starts with a complaint:

| Pattern | Example | What We Build |
|---------|---------|---------------|
| **Fixing a branded flaw** | "The original holder is slippery" | Better holder |
| **A play problem** | "Someone keeps peeking at my tiles" | Cover with sliding lid |
| **Accessibility** | "I can't hold cards with arthritis" | Hands-free holder |
| **Themed hobby tools** | "All the trays look the same" | Occult/witchy tray skins |

## Brands (Keep Separate)

| Brand | Audience | Products |
|-------|----------|----------|
| **OddHobbies** | Hobbyists, crafters, gamers | Functional accessories, themed tools |
| **Ochema** | Occult, witchy, spiritual | Celestial/occult-themed hobby tools |
| **DivergentJoy** | Neurodivergent adults | Energy trackers, sensory tools |

**Cross-sell rule:** OddHobbies and Ochema share the same hobby audience. DivergentJoy shares the neurodivergent audience with OddHobbies (spoonie crafters exist). But products stay in their own shops.

## Pilot: Cross-Stitch

### Why Cross-Stitch First
1. **Proven need** — floss drops, needle minders, parking bobbins are all bestsellers
2. **Adult buyers** — no kids' safety certification needed
3. **Small products** — print fast, ship cheap
4. **Needle minders = natural Meshy fit** — sculpted toppers on magnetic bases
5. **+173% search growth** in diamond painting (adjacent craft, same audience)

### The Fix
- **Needle minders** — standard ones are flat metal clips. We make sculpted 3D toppers that swap on a magnetic base.
- **Floss drops** — standard ones have no label slot. Ours have ID slots and house-shaped designs.

## IP Guardrails

| Don't | Do |
|-------|-----|
| Put "DMC" in titles | "Fits thread up to 8-strand" |
| Put "Scrabble" in titles | "Fits tiles up to 15mm" |
| Copy competitor geometry | Design from scratch, measure from complaints |
| Use brand logos | Use dimensions and compatibility language |

**Etsy's rule:** Your listing must be your own original design. Unmodified factory products don't qualify.

## Revenue Model

| Product | Price | COGS (3D print) | Margin |
|---------|-------|-----------------|--------|
| Needle minder (1) | $8.99 | ~$1.50 | ~83% |
| Needle minder set (3) | $22.99 | ~$4.00 | ~83% |
| Floss drop set (10) | $12.99 | ~$2.50 | ~81% |
| Floss drop + minder bundle | $18.99 | ~$3.50 | ~81% |
| Diamond painting tray | $14.99 | ~$3.00 | ~80% |
| Themed tray set (3) | $34.99 | ~$7.00 | ~80% |

## File Structure

```
oddhobbies/
├── docs/           — brand, products, research
├── products/
│   ├── cross-stitch/  — needle minders, floss drops
│   ├── diamond-painting/  — trays, towers, pens
│   └── card-games/  — holders, racks, accessories
├── templates/
│   ├── cad/        — OpenSCAD/FreeCAD parametric models
│   └── meshy/      — Meshy generation prompts
├── shop/           — Etsy setup, listing templates
└── assets/         — branding, photos
```

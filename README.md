# OddHobbies

> Micro-infrastructure for obsessive hobbies.
> Little physical things enthusiasts repeatedly need, where injection molding is uneconomic but CAD + 3D printing is perfect.

## The Thesis

The best signal is somebody sitting in front of:
- 20 bobbins
- 30 ink bottles
- 15 bonsai wire gauges
- piles of coins
- 50 paper colors
- dozens of miniature tack items
- tiny watch screws
- 20 stained-glass fragments
- game pieces rolling everywhere

Every object needs to be **held, sorted, measured, positioned, protected, counted or displayed.** That's our product surface.

## The Rule

Don't search for "weird hobbies." Search for:

**"Hobbies where practitioners have a table covered in shit."**

Then build the **whole physical operating system for that hobby**, not just one random accessory.

## Hobby Lines

### Tier 1 — Launch First (Excellent signal)

| Hobby | Core Problem | Flagship Product |
|-------|-------------|------------------|
| **Cross-Stitch** | Needles roll, floss tangles | Modular needle minder + floss drops |
| **Stained Glass** | Holding odd angles, different glass thicknesses | Adjustable angle jig system |
| **Bonsai** | Wire management, expensive accessories | Modular wire-spool kit |
| **Quilling** | 100+ strips become a storage nightmare | Vertical color library |
| **Crokinole** | Powder, scoring, board-edge organization | Powder sweeper + disc towers |

### Tier 2 — Month 2-3 (Strong signal)

| Hobby | Core Problem | Flagship Product |
|-------|-------------|------------------|
| **Diamond Painting** | Tray management, drill organization | Tray tower + alignment ruler |
| **Model-Horse Showing** | 1:9 scale stable/show environments | Parametric tack-room system |
| **Coin-Roll Hunting** | Sorting hundreds/thousands of coins | Multi-denomination sorting workstation |
| **Bobbin Lace** | Managing 50-100+ bobbins around a pillow | Clip-on parking comb system |

### Tier 3 — Month 4+ (Proven demand, more competitive)

| Hobby | Core Problem | Flagship Product |
|-------|-------------|------------------|
| **Card & Board Games** | Accessibility, peeking, token management | Universal card holder, tile racks |
| **Slot-Car Racing** | Track maintenance, pit workflow | Pit caddy, track cleaner |
| **Watch Repair** | Microscopic parts, different movements | Movement cradles, project trays |
| **Metal Detecting** | Field finds protection/classification | Finds case, coin cradle |

### Tier 4 — Specialty (Low volume, high margin)

| Hobby | Core Problem | Flagship Product |
|-------|-------------|------------------|
| **Ant Keeping** | Test tubes, feeding, heating mess | Modular tube rack, feeder dock |
| **Carnivorous Plants** | Constant-moisture watering | Species-specific reservoir pots |
| **Stamp Collecting** | Display, storage, classification | Custom album pages, display cases |
| **Rubik's Cubes** | Display, competition setup | Cube stands, timer docks, collection display |

## Brand Separation

| Brand | What | Why Separate |
|-------|------|-------------|
| **OddHobbies** | Functional hobby accessories (secular) | Broadest audience |
| **Ochema** | Occult-themed hobby tools | Different aesthetic, same craft audience |
| **DivergentJoy** | Neurodivergent tools | Different need, some cross-sell with craft |

## Revenue Model

| Product Type | Avg Price | COGS | Margin |
|-------------|-----------|------|--------|
| Small accessory (minder, clip, tray) | $8-15 | $0.50-2.00 | 85-95% |
| Medium tool (jig, holder, rack) | $15-30 | $2.00-4.00 | 80-87% |
| System/kit (workstation, library) | $30-60 | $5.00-10.00 | 75-83% |
| Personalized/custom | +$5-15 | +$0.50-1.00 | 90%+ |

## IP Guardrails

- **Don't use brand names in titles** — "Fits tiles up to 15mm" not "Scrabble-compatible"
- **Design from scratch** — Don't copy competitor geometry
- **Etsy requires original design** — Unmodified factory products don't qualify
- **Dimensions over brands** — "Fits standard 6-strand floss" not "DMC-compatible"

## File Structure

```
oddhobbies/
├── docs/                     — brand, master product list
├── products/
│   ├── cross-stitch/         — needle minders, floss drops
│   ├── stained-glass/        — jigs, assembly systems
│   ├── bonsai/               — wire management, tools
│   ├── quilling/             — color library, dispensers
│   ├── crokinole/            — powder tools, disc organizers
│   ├── diamond-painting/     — trays, towers, pens
│   ├── model-horse/          — 1:9 scale stable systems
│   ├── coin-roll/            — sorting workstations
│   ├── bobbin-lace/          — pillow organization
│   ├── card-games/           — holders, racks, accessories
│   ├── slot-car/             — pit caddy, track tools
│   ├── watch-repair/         — movement cradles, parts storage
│   ├── metal-detecting/      — finds cases, field tools
│   ├── ant-keeping/          — tube racks, feeder docks
│   ├── carnivorous-plants/   — reservoir pots
│   ├── stamp-collecting/     — display, album pages
│   └── rubiks-cube/          — display stands, collection cases
├── templates/
│   ├── cad/                  — OpenSCAD/FreeCAD parametric models
│   └── meshy/                — Meshy generation prompts
├── shop/                     — Etsy setup, listing templates
└── assets/                   — branding, photos
```

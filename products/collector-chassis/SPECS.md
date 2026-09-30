# Collector Chassis System

> One weighted base. Infinite adapters. Swap the shell, change the listing.

## Architecture

```
┌─────────────────────────────┐
│     MESHY SCULPTURAL SHELL  │  ← Swappable aesthetic (gothic, space, tavern, etc.)
├─────────────────────────────┤
│     ADAPTER INSERT          │  ← Holds the specific object (card, dice, mini, etc.)
├─────────────────────────────┤
│     WEIGHTED BASE           │  ← Universal, USB-C LED cavity, magnetic nameplate
└─────────────────────────────┘
```

## Base Unit

| Spec | Value |
|------|-------|
| **Size** | 120mm x 120mm x 15mm (compact) / 150mm x 150mm x 20mm (standard) |
| **Weight** | 150g (compact) / 280g (standard) — weighted with steel plate |
| **Material** | PLA+ shell, steel weight, felt bottom |
| **LED** | USB-C powered, warm white, brightness adjustable |
| **Nameplate** | Magnetic front panel, interchangeable |
| **Finish** | Matte black (default), white, wood grain |

### Base Features
- **USB-C LED cavity** — warm white light from below/behind
- **Magnetic nameplate slot** — 40x15mm, slides in/out
- **Universal adapter socket** — 80mm diameter circle, 5mm deep
- **Anti-slip felt bottom** — won't scratch surfaces
- **Weighted** — feels premium, won't tip

## Adapter System

Each adapter is a snap-fit insert that sits in the universal socket.

### Card Adapters
| Adapter | Holds | Size |
|---------|-------|------|
| **Raw card** | Single TCG card (unsleeved) | 63.5x88mm |
| **Toploader** | Card in toploader | 70x95mm |
| **Graded slab** | PSA/BGS/CGC slab | 80x130mm |
| **Favourite-9** | 9-card display frame | 200x200mm (no base needed) |

### Object Adapters
| Adapter | Holds | Size |
|---------|-------|------|
| **Dice socket** | 7-dice polyhedral set | 60mm diameter |
| **Mini plinth** | 25-60mm miniature | 40mm diameter, magnetic |
| **Keycap mount** | MX artisan keycap | 18mm, magnetic MX stem |
| **Coin capsule** | Standard coin capsule | 30-40mm diameter |
| **Pen cradle** | Fountain pen | 100mm length |
| **Car bay** | 1:64 diecast car | 75x35mm |
| **Cube stand** | Rubik's cube | 60mm cube |

### Adapter Pricing
| Type | Price | Material Cost |
|------|-------|---------------|
| Single adapter | $6.99 | $0.80 |
| 3-adapter pack | $16.99 | $2.00 |
| Full adapter set (8) | $39.99 | $5.00 |

## Meshy Shell System

Each shell is a sculptural surround that clips onto the base, transforming the aesthetic.

### Shell Collection

| Shell | Theme | Mood | Best For |
|-------|-------|------|----------|
| **Gothic Arch** | Medieval cathedral | Dark, dramatic | D&D, horror, dark fantasy |
| **Wizard Observatory** | Magical tower | Mystical, cozy | D&D, fantasy, magic |
| **Japanese Garden** | Zen temple | Calm, elegant | Go, bonsai, Asian games |
| **Museum Marble** | Classical museum | Clean, premium | Cards, coins, collectibles |
| **Space Station** | Sci-fi corridor | Futuristic, clean | Sci-fi collectibles |
| **Dark Forest** | Enchanted woods | Organic, mysterious | Fantasy, nature |
| **Ancient Ruins** | Greek/Roman ruins | Timeless, grand | Chess, history |
| **Cyberpunk Alley** | Neon-lit street | Edgy, modern | Tech, gaming |
| **Cosy Tavern** | Medieval inn | Warm, inviting | D&D, board games |
| **Victory Podium** | Sports champion | Celebratory | Tournaments, achievements |

### Shell Pricing
| Type | Price | Material Cost |
|------|-------|---------------|
| Single shell | $12.99 | $2.00 |
| 3-shell pack (themed) | $29.99 | $5.00 |
| 10-shell collection | $79.99 | $15.00 |

## Bundles

### Starter Kit ($34.99)
- 1 base (compact)
- 1 adapter (choice)
- 1 shell (choice)
- 1 magnetic nameplate

### Collector Kit ($59.99)
- 1 base (standard)
- 3 adapters (choice)
- 3 shells (choice)
- 3 nameplates

### Full Arsenal ($99.99)
- 2 bases (1 compact + 1 standard)
- 8 adapters (full set)
- 5 shells (choice)
- 10 nameplates

## Listing Strategy

### Same product, different listings

**Base unit:**
- "Collector Display Base — Magnetic LED Stand for Cards, Dice, Minis"
- "Card Display Base — Graded Card Shrine with LED"
- "Miniature Plinth Base — LED Display for Painted Models"

**Adapters:**
- "PSA Slab Display Adapter — Fits Collector Display Base"
- "Dice Display Socket — Wizard Observatory Shell"
- "Miniature Plinth Adapter — Magnetic, 25-60mm"

**Shells:**
- "Wizard Observatory Shell — For Collector Display Base"
- "Gothic Arch Shell — For Collector Display Base"
- "Japanese Garden Shell — For Collector Display Base"

**Bundles:**
- "D&D Gift Set — Wizard Observatory + Dice Socket + Nameplate"
- "Card Collector Set — Museum Marble + Slab Adapter + Nameplate"
- "Miniature Painter Kit — Gothic Arch + Plinth + Nameplate"

## CAD Specs

### Base (OpenSCAD)
```openscad
// Collector Base - Standard
base_width = 150;
base_depth = 150;
base_height = 20;
socket_diameter = 80;
socket_depth = 5;
nameplate_width = 40;
nameplate_height = 15;
led_slot = 10; // USB-C LED strip cavity

module base() {
    difference() {
        // Outer shell
        cube([base_width, base_depth, base_height]);
        // Socket
        translate([base_width/2, base_depth/2, base_height - socket_depth])
            cylinder(d=socket_diameter, h=socket_depth + 1);
        // LED cavity
        translate([10, 10, 5])
            cube([base_width - 20, base_depth - 20, 5]);
    }
}
```

### Adapter (OpenSCAD)
```openscad
// Card Adapter - fits in universal socket
adapter_outer = 78; // 2mm clearance from socket
adapter_height = 15;
card_width = 63.5;
card_height = 88;
card_slot_depth = 1;

module card_adapter() {
    difference() {
        cylinder(d=adapter_outer, h=adapter_height);
        // Card slot
        translate([0, 0, adapter_height - card_slot_depth])
            cube([card_width, card_height, card_slot_depth + 1], center=true);
    }
}
```

### Shell (Meshy prompt template)
```
A sculpted decorative shell surround for a collector display base. [THEME: gothic arch / wizard observatory / etc.]. 150mm x 150mm, clips onto weighted base. Sculptural, detailed, [MOOD: dark and dramatic / mystical and cozy / etc.]. 3D printable with minimal supports. Original design, not based on any existing franchise.
```

## Manufacturing Notes

### Base
- Print time: ~4-6 hours
- Material: ~$2.50 (PLA+)
- Weight: steel plate insert ($0.80)
- LED: USB-C strip ($1.50)
- Felt: adhesive pad ($0.20)
- Assembly: snap-fit, no glue

### Adapter
- Print time: ~30-60 min
- Material: ~$0.80
- Snap-fit to base socket

### Shell
- Print time: ~3-8 hours (depending on detail)
- Material: ~$2.00
- Clips to base via 4 snap tabs

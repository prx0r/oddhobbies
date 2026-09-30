# OddHobb — Google AI + Pinterest Playbook

> Build for agents first. Game both platforms from day one.

---

## GOOGLE AI SEARCH (AI Overviews, AI Mode, Gemini)

### The 8 Product Feed Attributes

Google explicitly connects these 8 attributes to AI-driven results. Most merchants are missing them.

| # | Attribute | What It Does | OddHobb Example |
|---|-----------|-------------|-----------------|
| 1 | **Product Highlight** | Key selling benefits (not specs) | "Handmade, 3D printed, personalized, magnetic" |
| 2 | **Product Detail** | Structured specs (Section:Name:Value) | "Material: PLA+ | Size: 80mm | Color: Black" |
| 3 | **Variant Option** | Non-standard variant dimensions | "Theme: Dragon Egg, Owl, Moon" |
| 4 | **Item Group Title** | Shared title for variant family | "First-Player Token Collection" |
| 5 | **Related Products** | Accessories, cross-sells | "Often bought with: token tray, dice tower" |
| 6 | **Question & Answer** | FAQ pairs for conversational AI | Q: "What size are the tiles?" A: "Fits standard 19mm tiles" |
| 7 | **Document Link** | PDFs AI can crawl | Companion guides, build instructions |
| 8 | **Popularity Rank** | Tell Google what sells | Sales data |

### Q&A Pairs (The Goldmine)

**Up to 30 Q&A pairs per product.** Google uses these to answer shopper questions in AI Mode.

**For Mahjong Line Reader:**
```
Q: What is a mahjong line reader?
A: A slim guide that helps organize and read mahjong tile sequences during play.

Q: Does it work with all mahjong sets?
A: Yes, fits standard American and Chinese mahjong tiles.

Q: Is it personalized?
A: Yes, add your name for a custom engraved line reader.

Q: What is it made from?
A: Premium PLA+ 3D printed on a Bambu print farm in the UK.

Q: How long does shipping take?
A: 1-3 business days production, 5-10 days worldwide shipping.
```

**For Cyberdeck Shell Kit:**
```
Q: What is a cyberdeck?
A: A DIY personal computer built in the cyberpunk aesthetic, typically using a Raspberry Pi.

Q: What comes in the kit?
A: 3D printed shell, Pi mounting bracket, cable management dock.

Q: Does it fit a Raspberry Pi 5?
A: Yes, fits Pi 3, 4, and 5 models.

Q: Can I customize the design?
A: Yes, we offer multiple shell themes and custom engraving options.

Q: Is the STL file included?
A: Yes, every purchase includes downloadable STL files.
```

### Document Links (Underused Opportunity)

**Up to 5 PDF links per product.** Google crawls these and uses them to answer questions in AI Mode.

**For each product, create:**
1. Companion guide PDF (historical context, symbolism)
2. Build/assembly guide PDF
3. Care and maintenance PDF
4. FAQ PDF
5. Supplier transparency PDF

**These PDFs are the content that makes AI agents recommend you.**

### Product Feed Structure (OddHobb)

```csv
id,title,description,product_highlight,product_detail,variant_option,item_group_title,related_products,question_and_answer,document_link,price,availability
mahjong_line_reader,Mahjong Line Reader Personalized,A slim guide that organizes mahjong tile sequences,"Handmade;3D printed;Personalized;Magnetic","Material:PLA+|Size:80mm|Color:Black|Weight:15g","Theme:Standard|Theme:Personalized|Theme:Gift Set",Mahjong Accessories,"Often bought with:Wind Markers,Tile Organizer|Accessory:Travel Case","What is a line reader?;Does it fit all mahjong sets?;Is it personalized?;What is it made from?;How long is shipping?",https://oddhobb.com/guides/mahjong-line-reader.pdf,8.99,in_stock
```

### Google Merchant Center Setup

| Step | Action |
|------|--------|
| 1 | Create Merchant Center account (free) |
| 2 | Verify website |
| 3 | Build product feed with 8 AI attributes |
| 4 | Submit feed via API or CSV |
| 5 | Enable AI performance insights |
| 6 | Monitor "Top terms" and "Popular attributes" |

### The Game

**Write Q&A pairs that match how people actually ask AI:**

| People Ask AI | Your Q&A Pair |
|---------------|---------------|
| "What do I need for cross-stitch?" | "What tools do I need for cross-stitch?" → needle minder, floss drops |
| "Best gift for a mahjong player" | "What gifts do mahjong players like?" → line reader, wind markers |
| "How to build a cyberdeck" | "What is a cyberdeck?" → DIY computer, Raspberry Pi |
| "What is a protection spell kit?" | "What's in a protection spell kit?" → candle, oil, herbs, sigil card |

**The goal:** When someone asks Google AI "what do I need for cross-stitch?", your products appear in the answer.

---

## PINTEREST (Visual Search Engine)

### The 4 Ranking Signals

| Signal | Weight | How to Optimize |
|--------|--------|-----------------|
| **Domain quality** | High | Claim website, consistent branding |
| **Pin quality** | High | Vertical 2:3, clear focal point, high-res |
| **Topic relevance** | High | Keywords in title, description, board name |
| **Engagement** | Medium | Saves, clicks, close-ups |

### Pinterest SEO Formula

**Pin Title (100 chars max):**
- Primary keyword first
- Benefit second
- Example: "Mahjong Line Reader — Personalized Gift for Mahjong Players"

**Pin Description (500 chars max):**
- 2-3 related keywords in natural language
- Write for humans first
- Example: "A slim guide that helps organize mahjong tile sequences during play. Perfect personalized gift for mahjong players. 3D printed, magnetic base, custom engraving available. Handmade in the UK."

**Board Name:**
- Keyword-rich
- Example: "Mahjong Accessories & Gifts"

**Board Description:**
- 2-3 sentences with keywords
- Example: "Personalized mahjong accessories, line readers, wind markers, and tile organizers. Handmade gifts for mahjong players."

### Pin Design Rules

| Element | Spec |
|---------|------|
| **Aspect ratio** | 2:3 (vertical) |
| **Resolution** | 1000x1500 minimum |
| **Text on pin** | Keyword-rich, readable |
| **Focal point** | Product clearly visible |
| **Background** | Clean, not cluttered |
| **Variations** | 3-5 designs per product |

### The Pinterest Game

**1. Consistency beats volume.** Pin daily. Pinterest rewards active accounts.

**2. Freshness boost.** Pins under 7 days old get ranking boost. Keep pinning new designs.

**3. Topic alignment.** Pinterest checks if your pin title/description matches the landing page. Keep them consistent.

**4. Keyword research.** Pinterest has 20M+ official keywords in its Interest Taxonomy. Use the search bar to find them.

**5. Multiple designs per product.** One product → 5 different pin designs → 5 different keyword angles.

### Pinterest Product Pins

**Catalog feed → auto product pins:**

| Attribute | What to Include |
|-----------|----------------|
| **title** | Product name + primary keyword |
| **description** | 2-3 keywords in natural language |
| **price** | Exact price |
| **availability** | in_stock |
| **image_link** | High-quality product photo |
| **additional_image_link** | 3-5 more photos |
| **product_type** | "Mahjong Accessories" |
| **brand** | OddHobb |

### Pinterest Content Calendar

| Day | Pin Type | Example |
|-----|----------|---------|
| Monday | Product pin | Mahjong Line Reader |
| Tuesday | Idea pin | "5 Gifts for Mahjong Players" |
| Wednesday | Product pin | First-Player Token |
| Thursday | Lifestyle pin | "Game Night Setup" |
| Friday | Product pin | Dice Tower |
| Saturday | Collection pin | "OddHobb Gift Guide" |
| Sunday | How-to pin | "How to Build a Cyberdeck" |

**7 pins per day minimum.** Pinterest rewards daily activity.

---

## The Agent Discovery Play (How to Game Both)

### Google AI Discovery

```
1. Create structured product feed with 8 AI attributes
2. Write 30 Q&A pairs per product
3. Create 5 companion guide PDFs per product
4. Submit to Google Merchant Center
5. Enable AI performance insights
6. Monitor "Top terms" and optimize

RESULT: When someone asks Google AI about your niche,
your products appear in the answer.
```

### Pinterest Discovery

```
1. Claim website + install Pinterest tag
2. Build product catalog feed
3. Create 5 pin designs per product
4. Pin daily with keyword-rich titles/descriptions
5. Use Pinterest Trends for keyword research
6. Monitor pin performance and double down on winners

RESULT: Your pins appear in Pinterest search for your niche.
```

### The Combined Flywheel

```
Google AI: "What do I need for cross-stitch?"
  → Your product appears in AI Overview
  → User clicks to your Etsy listing
  → Buys needle minder

Pinterest: User searches "cross stitch gifts"
  → Your pin appears in search
  → User clicks to your Etsy listing
  → Buys needle minder

Both channels → Etsy sales → more data → better AI/Pinterest ranking → more traffic
```

---

## Implementation Priority

### Week 1: Etsy + Google Merchant Center
| Task | Time |
|------|------|
| Set up Etsy shop (OddHobb) | 1 day |
| List 5 products with photos | 2 days |
| Set up Google Merchant Center | 1 day |
| Build product feed with 8 AI attributes | 2 days |
| Write 30 Q&A pairs per product | 2 days |

### Week 2: Pinterest + Document Links
| Task | Time |
|------|------|
| Set up Pinterest Business | 1 day |
| Build product catalog feed | 2 days |
| Create 5 pin designs per product | 2 days |
| Create 5 companion guide PDFs per product | 3 days |
| Submit Document Links to Google | 1 day |

### Week 3: Knowledge Graphs + MCP
| Task | Time |
|------|------|
| Build product knowledge graph (JSON) | 2 days |
| Build hobby knowledge graph (JSON) | 2 days |
| Build MCP server | 3 days |
| Test agent discovery | 2 days |
| Connect MCP to Google/Pinterest | 2 days |

**The key insight:** Write Q&A pairs and companion guides that AI agents can read. That's how you get recommended in Google AI Overviews. Pinterest rewards consistent, keyword-rich pinning. Both consume the same structured data from your MCP/knowledge graph.

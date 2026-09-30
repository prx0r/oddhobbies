# Tutorial Content Pipeline

> IKEA-style tutorials + AI generation = content machine.
> Agnes Video Generator (free, open-source) for production.

---

## The Format

**IKEA-style:** Clear, step-by-step, visual, no jargon.
**Target audience:** Beginners who want to try but don't know where to start.

**Structure per tutorial:**
```
1. Hook: "What we're building today"
2. Materials: What you need (with product links)
3. Steps: 5-10 clear steps, one per scene
4. Result: What it looks like finished
5. Outro: "Get the kit at OddHobb"
```

## AI Video Generation Tools

### Agnes Video Generator (PRIMARY)

| Field | Value |
|-------|-------|
| **URL** | https://github.com/lcy362/agnes-video-generator |
| **Cost** | Free (MIT license) |
| **GPU needed** | No (cloud API) |
| **Features** | Text → multi-scene video, TTS, subtitles, digital anchor |
| **Output** | 9:16, 16:9, 1:1 |
| **Watermark** | None |
| **Rate limit** | 16 req/min |

**Pipeline:**
```
1. Write script (text)
2. Paste into Agnes
3. Agnes generates: scenes + narration + subtitles
4. Download MP4
5. Add OddHobb logo + product outro
6. Upload to YouTube
```

### Other Tools

| Tool | Use For | Cost |
|------|---------|------|
| **AI Video Tutorial Generator** | Character animation + slides | Free |
| **repo-to-video** | Code tutorials from GitHub | Free |
| **CogVideoX** | Text → video (Colab T4) | Free |
| **Wan 2.2** | Text/image → video | Free |
| **edge_tts** | Voice narration only | Free |
| **MiniMax H3 Max** | High-quality video generation | Free tier |

## Tutorial Topics by Campaign

### Cyberdecks
| Tutorial | Length | Products |
|----------|--------|----------|
| How to Build Your First Cyberdeck | 15 min | Shell kit, Pi case |
| Raspberry Pi Setup for Beginners | 12 min | Pi case, cable dock |
| Mechanical Keyboard Basics | 10 min | Keyboard shrine, switch tester |
| Terminal for Non-Programmers | 12 min | Terminal accessories |
| Cable Management | 8 min | Cable dock, combs |

### Needlepoint
| Tutorial | Length | Products |
|----------|--------|----------|
| Your First Needlepoint Project | 15 min | Project valet, needle minder |
| Reading Needlepoint Patterns | 10 min | Thread card carousel |
| Finishing Your Needlepoint | 12 min | Display frame |
| Needlepoint on the Go | 8 min | Travel case inserts |

### Mahjong
| Tutorial | Length | Products |
|----------|--------|----------|
| How to Play Mahjong | 15 min | Line reader |
| Mahjong Tile Care | 8 min | Tile organizer |
| Mahjong Scorekeeping | 10 min | Score sticks |
| Setting Up a Mahjong Night | 12 min | Hostess gift box |

### Chess
| Tutorial | Length | Products |
|----------|--------|----------|
| Chess Pieces Explained | 10 min | Piece holder |
| Basic Chess Rules | 12 min | Chess accessories |
| Chess Board Setup | 8 min | Board accessories |
| Capturing in Chess | 10 min | Capture tray |

## Production Pipeline (Per Tutorial)

### Step 1: Write Script (30 min)
```
[HOOK — 10s]
"What we're building today is..."

[MATERIALS — 30s]
"You'll need: [product] from OddHobb, [tool], [component]"

[STEPS — 8-12 min]
"Step 1: [clear action]"
"Step 2: [clear action]"
... (5-10 steps)

[RESULT — 30s]
"And there it is. A finished [product]."

[OUTRO — 15s]
"Get the kit at OddHobb. Link in the description."
```

### Step 2: Generate Video (15 min)
1. Open Agnes Video Generator
2. Paste script
3. Select format (16:9 for YouTube)
4. Generate
5. Download MP4

### Step 3: Edit (15 min)
1. Add OddHobb logo intro (2s)
2. Add product outro (10s)
3. Add end screen
4. Add captions (Agnes auto-generates)

### Step 4: Upload (10 min)
1. YouTube: title, description, tags, thumbnail
2. Link to Etsy products
3. Pin comment with product links
4. Share on social media

**Total per tutorial: ~1 hour**

## Content Calendar (Week 1)

| Day | Tutorial | Campaign | Products |
|-----|----------|----------|----------|
| Monday | How to Build Your First Cyberdeck | Cyberdecks | Shell kit |
| Tuesday | Your First Needlepoint Project | Needlepoint | Project valet |
| Wednesday | How to Play Mahjong | Mahjong | Line reader |
| Thursday | Raspberry Pi Setup | Cyberdecks | Pi case |
| Friday | Reading Needlepoint Patterns | Needlepoint | Thread carousel |
| Saturday | Mechanical Keyboard Basics | Cyberdecks | Keyboard shrine |
| Sunday | Mahjong Scorekeeping | Mahjong | Score sticks |

**7 tutorials in week 1. 30+ per month.**

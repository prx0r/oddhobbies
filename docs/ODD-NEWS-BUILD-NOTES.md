# Odd News — Build Notes & Pipeline

> Repeatable pipeline for daily 2-hour episodes. $0 cost. Infinite content.

---

## The Pipeline (Daily)

```
1. PICK countries/topics (20 per episode)
2. PULL data (World Bank API, Global Voices, Wikimedia)
3. WRITE script (~900 words per country, ~21,000 words total)
4. RECORD voiceover (calm, warm, 0.7x pace)
5. ADD visuals (Wikimedia slideshow, OddHobb logo)
6. EDIT (intro + content + outro + product mention)
7. UPLOAD (YouTube + Spotify)
8. PROMOTE (social media, description links)
```

## Time Budget

| Step | Time |
|------|------|
| Pull data | 30 min |
| Write script | 2-3 hours |
| Record voiceover | 2-3 hours |
| Edit video | 1-2 hours |
| Upload + promote | 30 min |
| **Total** | **~6-8 hours/day** |

## Data Sources (All Free)

| Source | What It Provides | API |
|--------|-----------------|-----|
| **World Bank** | GDP, poverty, life expectancy, population | `api.worldbank.org` |
| **Global Voices** | Native journalism, cultural context | RSS feed |
| **Wikimedia Commons** | Photos of daily life | API |
| **OpenFoodFacts** | Food data | API |
| **GDELT** | What's in the news | API (1 req/5s) |
| **Numbeo** | Cost of living | Scrape (cache 24h) |
| **AllAfrica** | African stories | RSS feed |

## Country Rotation

191 countries available. Each country can appear multiple times with different data angles:
- Economy & wages
- Food & daily life
- Culture & traditions
- Progress & challenges
- Geography & environment

**191 countries × 5 angles = 955 possible episodes**

## Script Template

### Intro (200 words)
- Welcome to Odd News
- Tonight's theme/region
- What we'll explore
- "This isn't news. It's texture."

### Country Section (900 words each)
1. Basic facts (population, GDP, life expectancy)
2. What people earn (teacher salary)
3. What things cost (rent, food)
4. Economy composition
5. Progress trends (poverty reduction, life expectancy gains)
6. Cultural detail (from Global Voices)
7. Why it matters
8. "Sleep well."

### Outro (200 words)
- Recap of countries visited
- OddHobb product mention
- "Goodnight. Sleep well."

## Recording

| Element | Spec |
|---------|------|
| **Voice** | Calm, warm, 0.7x pace |
| **Tool** | edge_tts (free) or human voice |
| **Voice name** | "Daniel" (en-GB, calm) or custom |
| **Background** | Low ambient (rain, night sounds) |
| **Music** | None (keep it quiet) |

## Editing

| Element | Spec |
|---------|------|
| **Intro** | OddHobb logo (2s) |
| **Visuals** | Wikimedia slideshow, one image per story |
| **Outro** | OddHobb logo + product mention (10s) |
| **End screen** | Subscribe + product link |
| **Format** | 16:9 YouTube, 1:1 Spotify (audio only) |

## Upload

| Platform | Format | Notes |
|----------|--------|-------|
| **YouTube** | MP4, 16:9, 1080p | Full video with visuals |
| **Spotify** | Audio only | Same audio, no visuals |
| **Podcast** | MP3 | Same audio, via anchor/spotify |

## Description Template

```
[Episode description — 2-3 sentences about tonight's countries]

If you want something beautiful to wake up to:
🔗 OddHobb — [link]

Subscribe for more goodnight news.

#OddHobb #GoodNews #WorldNews #Sleep #GoodNight
```

## Pinned Comment

```
Tonight's countries: [list]. Data from World Bank. 
OddHobb gifts: [link]
```

---

## Content Volume

| Metric | Value |
|--------|-------|
| Countries available | 191 |
| Data points per country | 50+ |
| Episodes possible | 955+ (191 × 5 angles) |
| Words per episode | ~21,000 |
| Episodes per day | 1 (2-hour format) |
| Episodes per month | 30 |
| Years of content | 26+ (without repeating) |

## Kill Criteria

| Signal | Threshold | Action |
|--------|-----------|--------|
| Views | Below 500 after 14 days | Adjust format |
| Retention | Below 30% average | Shorten episodes |
| Subscribers | Below 50 after 30 days | Change approach |
| Etsy clicks | Zero after 20 episodes | Fix product tie-in |
| Spotify follows | Below 100 after 30 days | Audio format issue |

---

## Other Series (Pilot Concepts)

| Series | Content | Audience | Product Tie-In |
|--------|---------|----------|---------------|
| **Odd Etymology** | Word histories | Curious, intellectual | Journals, writing tools |
| **Odd Minds** | Philosophy, AGI, science | Nerdy, ADHD | Neurodivergent tools |
| **Odd Stories** | Fairy tales, folklore | Storytelling lovers | Personalized gifts |
| **Odd Sleep** | Sleep stories, ambient | Sleep-deprived | Sleep tools |
| **Neuro News** | ADHD/autism research | Neurodivergent | Neurodivergent products |
| **Odd Trades** | "Become an electrician in your sleep" | Practical, nerdy | Hobby tools |
| **Odd Nature** | Weird animals, ecology | Nature lovers | Nature-themed products |
| **Odd History** | Forgotten historical events | History buffs | Historical prints |

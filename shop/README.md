# Launch listing packs

> Organised listing data for PogPet. No OAuth required to read these.  
> Etsy API push blocked until tokens are refreshed (manual re-auth).

## Structure

```
shop/listings/
  _INDEX.json           # master index
  PROMPT-PACK.md        # ChatGPT image prompts per SKU
  image_prompts.json    # machine-readable prompts
  <SKU>.json            # full pack: title, tags, desc, personalisation
shop/LAUNCH-READY.md    # priority table
shop/STORE-STRUCTURE.md # sections (no Xmas section)
shop/IMAGE-PROMPTS.md   # prompt system
shop/ETSY-OAUTH.md      # re-auth later
db/                     # SQLite + MCP + templates
```

## Featured (brand)
| SKU | Etsy ID | Price |
|-----|---------|-------|
| ALBUM-MEMORY-CD | 4586678882 | $34.99 |
| ALBUM-WEDDING-VIDEO | 4586678898 | $59.99 |
| Brick couple (live) | 4584658234 | $34.99+ |

## Sections
Featured · Couples & Weddings · Game Night · Physical Media · Add-Ons  
(Christmas is NOT a section — whole store is Xmas.)

## Blockers
1. Product photos / ChatGPT images  
2. Etsy OAuth re-auth (browser) for API writes  
3. Production partners in dashboard (Makr3D, Prodigi, Kunaki)  

# Etsy OAuth — get working again

> Tokens expired (access ~1h, refresh ~90d).  
> You need a **new browser authorisation** to mint a fresh refresh token.

---

## Credentials (already known)

| Item | Value |
|------|-------|
| App keystring | `YOUR_ETSY_KEYSTRING` |
| Shared secret | `YOUR_ETSY_SHARED_SECRET` |
| Shop ID | `67863887` |
| User ID | `1287193524` |
| Shop | https://www.etsy.com/shop/pogpet |

**Scopes you want (all of these):**
```
listings_r listings_w listings_d shops_r shops_w
```
- `listings_w` — create/edit drafts  
- `listings_d` — **delete** ZZ CUT drafts  
- `shops_w` — sections + shop updates  

---

## Step 1 — Etsy developer app

1. Open https://etsy.com/developers/your-apps  
2. Edit your app (or create one)  
3. **Redirect URI** must match **exactly** what you use below  
   Example that works locally:
   ```
   http://127.0.0.1:8765/etsy/callback
   ```
   (or `http://localhost:8765/etsy/callback` — pick one and stick to it)  
4. Note **keystring** + **shared secret** (already have them)

---

## Step 2 — Open authorisation URL in browser

Replace `YOUR_REDIRECT` with the exact URI registered on the app:

```
https://www.etsy.com/oauth/connect?
response_type=code
&redirect_uri=YOUR_REDIRECT
&scope=listings_r%20listings_w%20listings_d%20shops_r%20shops_w
&client_id=YOUR_ETSY_KEYSTRING
&state=oddhobbies
```

(All on one line; spaces → `%20`.)

1. Log into Etsy as the shop owner (PogPet)  
2. Click **Allow**  
3. Browser lands on YOUR_REDIRECT with `?code=XXXX&state=oddhobbies`  
4. **Copy the `code` value**

---

## Step 3 — Exchange code → tokens

```bash
# local listener (run in a terminal you can watch)
python3 -m http.server 8765
```
Or use any callback URL you registered and read the code from the address bar.

```bash
curl -s -X POST "https://openapi.etsy.com/v3/public/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=PASTE_CODE_HERE" \
  -d "redirect_uri=YOUR_REDIRECT" \
  -d "client_id=YOUR_ETSY_KEYSTRING" \
  -d "client_secret=YOUR_ETSY_SHARED_SECRET"
```

**Response includes:**
- `access_token` (short-lived)
- `refresh_token` (**save this — ~90 days**)
- `scope`, `user_id`

Save JSON to `/tmp/etsy_token.json` (same shape as before).

---

## Step 4 — Store refresh token safely

Preferred:
```bash
agent-vault vault credential set ETSY_REFRESH_TOKEN --vault oracle
# paste token when prompted (or use vault CLI as you normally do)
```

Also keep a copy only on the primary VPS (not in git):
```bash
umask 077
# already at /tmp/etsy_token.json — better: ~/.config/oddhobbies/etsy_token.json
```

---

## Step 5 — Use it

```bash
# refresh when access expires
python3 - <<'PY'
import json, urllib.request, urllib.parse
KEY="YOUR_ETSY_KEYSTRING:YOUR_ETSY_SHARED_SECRET"
# read refresh from vault or file
import subprocess
rt=subprocess.check_output(["agent-vault","vault","credential","get","ETSY_REFRESH_TOKEN","--vault","oracle"], text=True).strip()
body=urllib.parse.urlencode({"grant_type":"refresh_token","refresh_token":rt,"client_id":"YOUR_ETSY_KEYSTRING"}).encode()
req=urllib.request.Request("https://openapi.etsy.com/v3/public/oauth/token", data=body, headers={"Content-Type":"application/x-www-form-urlencoded"})
print(json.load(urllib.request.urlopen(req)))
PY
```

Always send:
- `x-api-key: YOUR_ETSY_KEYSTRING:YOUR_ETSY_SHARED_SECRET`
- `Authorization: Bearer <access_token>`

---

## What you get after re-auth

| Capability | Scope |
|------------|-------|
| Create/edit draft listings | `listings_w` |
| Read listings | `listings_r` |
| Delete ZZ CUT drafts | `listings_d` |
| Shop sections + policies | `shops_w` |
| Read shop info | `shops_r` |

Then:
1. Create sections (Featured, Couples, Game Night, Physical Media, Add-Ons)  
2. Delete `ZZ CUT` / `ZZ KILLED` drafts  
3. Create keychain drafts if still missing  
4. Upload images when ready  

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `redirect_uri` mismatch | Must match app **exactly** (http vs 127.0.0.1, port, path) |
| `invalid_client` | keystring / secret wrong |
| `invalid_grant` on refresh | refresh expired → full re-auth (Step 2) |
| `insufficient_scope` | authorise with all 5 scopes listed |
| 401 on API | access expired → refresh; if refresh dead → re-auth |

---

## One-liner checklist

1. Register redirect URI on Etsy app  
2. Open browser OAuth URL (scopes above)  
3. Copy `code` from callback  
4. POST code → token endpoint  
5. Save `refresh_token` to vault  
6. Refresh → hit API with Bearer + x-api-key  

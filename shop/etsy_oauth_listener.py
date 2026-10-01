#!/usr/bin/env python3
"""Etsy OAuth callback listener — run this, then open the connect URL."""

import json
import urllib.parse
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

KEY_ID = "YOUR_ETSY_KEYSTRING"  # paste from vault/Etsy app
SECRET = "YOUR_ETSY_SHARED_SECRET"  # paste from vault/Etsy app
# MUST match Etsy app redirect URI exactly
REDIRECT = "http://127.0.0.1:8765/etsy/callback"
OUT = Path("/tmp/etsy_token.json")
RESULT = Path("/tmp/etsy_oauth_result.json")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        code = (qs.get("code") or [None])[0]
        if not code:
            body = (
                b"<html><body><h2>No code</h2>"
                b"<p>Path must be <code>/etsy/callback</code> with a <code>?code=</code> query.</p>"
                b"</body></html>"
            )
            self.send_response(400)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(body)
            return

        data = urllib.parse.urlencode(
            {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT,
                "client_id": KEY_ID,
                "client_secret": SECRET,
            }
        ).encode()
        req = urllib.request.Request(
            "https://openapi.etsy.com/v3/public/oauth/token",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        try:
            with urllib.request.urlopen(req) as resp:
                tok = json.load(resp)
        except urllib.error.HTTPError as e:
            tok = {"error": e.read().decode()[:500], "status": e.code}

        RESULT.write_text(json.dumps({"token": tok}, indent=2))
        if isinstance(tok, dict) and tok.get("access_token"):
            OUT.write_text(json.dumps(tok, indent=2))
            Path("/tmp/etsy_refresh_token.txt").write_text(tok.get("refresh_token", ""))
            body = (
                f"<html><body><h2>OAuth OK</h2>"
                f"<p>scope: {tok.get('scope')}</p>"
                f"<p>refresh saved to /tmp/etsy_token.json</p>"
                f"<p>Close this tab.</p></body></html>"
            ).encode()
            self.send_response(200)
        else:
            body = (
                f"<html><body><h2>Token error</h2><pre>{json.dumps(tok, indent=2)}</pre></body></html>"
            ).encode()
            self.send_response(500)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    httpd = HTTPServer(("127.0.0.1", 8765), Handler)
    print("READY http://127.0.0.1:8765/etsy/callback")
    print("Open OAuth URL in a browser on THIS machine, log into Etsy, Allow.")
    print("Waiting 180s...")
    httpd.timeout = 180
    httpd.handle_request()
    if RESULT.exists():
        tok = json.loads(RESULT.read_text())["token"]
        if isinstance(tok, dict) and tok.get("access_token"):
            print("SUCCESS", tok.get("scope"), "user", tok.get("user_id"))
        else:
            print("FAIL", tok)
    else:
        print("No callback received in time")


if __name__ == "__main__":
    main()

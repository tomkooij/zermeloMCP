#!/usr/bin/env python3
"""Controleer of een Zermelo-token werkt.

Gebruik:
    python check_zermelo_token.py
    python check_zermelo_token.py --verwacht kj

Of eerst een koppelcode (uit Zermelo Portal > Koppel externe applicatie)
omzetten naar een token en dat meteen controleren:
    python check_zermelo_token.py --koppelcode
    python check_zermelo_token.py --koppelcode "123456789012"

Het token wordt gelezen uit de omgevingsvariabele ZERMELO_TOKEN, of anders
verborgen gevraagd (het wordt niet op het scherm getoond of opgeslagen).
"""
import argparse
import getpass
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta


def api_get(school, path, token, params=None):
    url = f"https://{school}.zportal.nl/api/v3/{path}"
    if params:
        url += "?" + "&".join(f"{k}={v}" for k, v in params.items())
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {token}", "Accept": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.load(resp)["response"]


def exchange_koppelcode(school, code):
    """Zet een koppelcode om naar een access token (koppelcode is eenmalig bruikbaar)."""
    code = "".join(code.split())  # spaties verwijderen
    body = urllib.parse.urlencode({"grant_type": "authorization_code", "code": code}).encode()
    req = urllib.request.Request(
        f"https://{school}.zportal.nl/api/v3/oauth/token", data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.load(resp)["access_token"]
    except urllib.error.HTTPError as e:
        if e.code in (400, 401, 403):
            sys.exit(f"✗ Koppelcode geweigerd (HTTP {e.code}): al gebruikt, verlopen of onjuist.")
        if e.code == 404:
            sys.exit(f"✗ HTTP 404: klopt de schoolnaam '{school}'?")
        sys.exit(f"✗ HTTP-fout {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        sys.exit(f"✗ Geen verbinding met {school}.zportal.nl: {e.reason}")


def main():
    ap = argparse.ArgumentParser(description="Controleer een Zermelo-token")
    ap.add_argument("--school", default="coornhert-gymnasium",
                    help="Zermelo-instantie, het deel voor .zportal.nl (standaard: coornhert-gymnasium)")
    ap.add_argument("--verwacht", help="Verwachte gebruikerscode (bijv. 'kj')")
    ap.add_argument("--koppelcode", nargs="?", const="", metavar="CODE",
                    help="Zet eerst een koppelcode om naar een token. "
                         "Zonder waarde wordt er verborgen om gevraagd.")
    args = ap.parse_args()

    if args.koppelcode is not None:
        code = args.koppelcode or getpass.getpass("Koppelcode: ")
        token = exchange_koppelcode(args.school, code)
        print("✓ Koppelcode omgezet. Je token (bewaar deze, hij wordt niet opnieuw getoond):")
        print(f"  {token}\n")
    else:
        token = os.environ.get("ZERMELO_TOKEN") or getpass.getpass("Zermelo-token: ")
    token = token.strip()
    if not token:
        sys.exit("Geen token opgegeven.")
    print(f"Token: {token[:4]}…{token[-4:]} (lengte {len(token)})")

    # 1. Wie ben ik?
    try:
        resp = api_get(args.school, "users/~me", token)
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            sys.exit(f"✗ Token geweigerd (HTTP {e.code}): ongeldig, ingetrokken of verlopen.")
        if e.code == 404:
            sys.exit(f"✗ HTTP 404: klopt de schoolnaam '{args.school}'?")
        sys.exit(f"✗ HTTP-fout {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        sys.exit(f"✗ Geen verbinding met {args.school}.zportal.nl: {e.reason}")

    data = resp.get("data") or []
    if not data:
        sys.exit("✗ Token geaccepteerd, maar geen gebruiker teruggekregen.")
    me = data[0]
    naam = " ".join(filter(None, [me.get("firstName"), me.get("prefix"), me.get("lastName")]))
    code = me.get("code")
    print(f"✓ Token geldig voor: {naam} (code: {code})")

    if args.verwacht and code != args.verwacht:
        print(f"⚠ Let op: verwachte code '{args.verwacht}', maar token hoort bij '{code}'.")

    # 2. Kan ik het rooster van deze week ophalen?
    maandag = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    maandag -= timedelta(days=maandag.weekday())
    start = int(maandag.timestamp())
    end = int((maandag + timedelta(days=7)).timestamp())
    try:
        resp = api_get(args.school, "appointments", token,
                       {"user": "~me", "start": start, "end": end, "valid": "true"})
        print(f"✓ Rooster op te halen: {len(resp.get('data', []))} afspraken deze week")
    except urllib.error.HTTPError as e:
        print(f"⚠ Rooster ophalen mislukt (HTTP {e.code}): token heeft mogelijk geen roosterrechten.")


if __name__ == "__main__":
    main()

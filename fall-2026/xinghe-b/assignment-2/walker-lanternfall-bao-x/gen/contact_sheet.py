#!/usr/bin/env python3
"""Contact sheet of every thumbnail for an asset, stamped ACCEPT/MODIFY/REJECT/PENDING.

    python gen/contact_sheet.py ART-PC-01      -> gen/rejected/ART-PC-01-contact.png
"""
import json, sys
from PIL import Image, ImageDraw
from common import ROOT

asset = sys.argv[1]
sides = sorted((ROOT / "gen" / "log" / asset).glob("*.json"))
tiles = []
for s in sides:
    m = json.loads(s.read_text())
    th = ROOT / m["thumbnail"]
    im = Image.open(th).convert("RGB").resize((256, 256)) if th.exists() else Image.new("RGB", (256, 256), "gray")
    verdict = (m.get("decision") or {}).get("verdict", "pending").upper()
    d = ImageDraw.Draw(im)
    color = {"ACCEPT": "#2E8B57", "MODIFY": "#F2B84B", "REJECT": "#B5523B"}.get(verdict, "#6E7FA3")
    d.rectangle([0, 226, 255, 255], fill=color)
    d.text((6, 232), f"{verdict}  seed {m['settings'].get('seed')}", fill="white")
    tiles.append(im)
cols = min(4, max(1, len(tiles)))
rows = (len(tiles) + cols - 1) // cols
sheet = Image.new("RGB", (cols * 260, max(1, rows) * 260), "#14121C")
for i, t in enumerate(tiles):
    sheet.paste(t, ((i % cols) * 260 + 2, (i // cols) * 260 + 2))
out = ROOT / "gen" / "rejected" / f"{asset}-contact.png"
out.parent.mkdir(parents=True, exist_ok=True)
sheet.save(out, optimize=True)
print(out)

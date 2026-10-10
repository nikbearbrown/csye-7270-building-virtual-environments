#!/usr/bin/env python3
"""Re-run the logged edit chain for one ART-PC-01 frame (walk_contact, seed 11) with the project's own functions in
gen/art_process.py, save every stage, and check that the last stage equals the shipped frame in pc_sheet.png.

    gen/.venv-art/bin/python youtube/claude-liam-walker-lanternfall-bao-x-gamedev/tools/asset_trace_stages.py
"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image

REEL = Path(__file__).resolve().parents[1]
ROOT = REEL.parents[1]
sys.path.insert(0, str(ROOT / "gen"))
from art_process import fit_normalized, key_background, lock_palette, rgb  # noqa: E402

OUT = REEL / "images" / "trace"
spec = json.loads((ROOT / "gen/mappings/ART-PC-01.json").read_text())
frame = next(f for f in spec["frames"] if f["name"] == "walk_contact")
index = [f["name"] for f in spec["frames"]].index("walk_contact")
palette = [rgb(c) for c in json.loads((ROOT / "godot/assets/art/palettes.json").read_text())[spec["palette"]]]
fw, fh = spec["frame"]
k = spec["supersample"]

raw = Image.open(ROOT / frame["src"]).convert("RGBA")
keyed = key_background(raw, spec["bg_threshold"])
mirrored = keyed.transpose(Image.FLIP_LEFT_RIGHT) if frame["mirror"] else keyed
fitted, lamp = fit_normalized(mirrored, fw * k, fh * k, spec["normalize_lamp_px"] * k, 2 * k)
locked = lock_palette(fitted, palette, rgb("#14121C"), spec.get("ink_below_l", 14.0), supersample=k)
shipped = Image.open(ROOT / spec["out"]).convert("RGBA").crop((index * fw, 0, (index + 1) * fw, fh))
same = np.array_equal(np.array(locked), np.array(shipped))

for name, im in [("1-raw", raw), ("2-keyed", keyed), ("3-mirrored", mirrored), ("4-fitted-128", fitted), ("5-locked-32", locked)]:
    im.save(OUT / f"walk_contact-{name}.png")
locked.resize((fw * 16, fh * 16), Image.NEAREST).save(OUT / "walk_contact-5-locked-32-x16.png")
report = {"run": frame["run"], "src": frame["src"], "index_in_sheet": index, "mirror": frame["mirror"],
          "lamp_px": round(lamp / k, 2), "supersample": k, "palette": spec["palette"],
          "colours_used": sorted({"#%02X%02X%02X" % tuple(p[:3]) for p in np.array(locked).reshape(-1, 4) if p[3]}),
          "equals_shipped_frame": bool(same)}
(OUT / "walk_contact-stages.json").write_text(json.dumps(report, indent=1))
print(json.dumps(report, indent=1))

#!/usr/bin/env python3
"""compare_routes.py <direct log> <4K-route log>: do the nineteen captures give the same probes on both capture routes?

The film's Godot captures are rendered on the 4K route (a 3840 x 2160 SubViewport over a 1280 x 720 canvas). Some shader inputs count
physical pixels (FRAGCOORD, SCREEN_PIXEL_SIZE, LIGHT_POSITION, LIGHT_VERTEX) and change with that route; this film's shaders read only
SCREEN_UV (a fraction of the screen), so the probes should not move. This compares every RESULT line of run-11 (direct route, 1280 x 720,
scale 1) with the same probe in run-11b (4K route, scale 3):
  * three-sprite window scenes: every zone label (stage / A / B / C / black) must be identical;
  * pond scenes: player position identical, the colour read at the reflection centre and at open water within 0.015 per channel, the
    count of mask-coloured pixels equal (or within 5 %), the pixels the reflection changes within 3 % (edge anti-aliasing at 3x differs).
Prints one line per probe (OK / DIFFERENT) and a summary. Stdlib only. Exit code 1 if any probe is DIFFERENT.
"""
import json
import sys
from pathlib import Path


def load(path):
    out = {}
    for line in Path(path).read_text().splitlines():
        if not line.startswith("RESULT "):
            continue
        d = json.loads(line[7:])
        if "t" in d and "capture" in d:
            out[(d["capture"], round(d["t"], 2))] = d
    return out


def close(a, b, tol):
    return all(abs(x - y) <= tol for x, y in zip(a, b))


def rel(a, b, frac, floor):
    return abs(a - b) <= max(floor, frac * max(a, b))


def compare(a, b):
    notes = []
    if "main" in a:
        for part in ("main", "w1", "w2"):
            if part in a or part in b:
                if a.get(part) != b.get(part):
                    notes.append(f"{part}: {a.get(part)} vs {b.get(part)}")
    else:
        if abs(a["player_x"] - b["player_x"]) > 0.01 or abs(a["player_y"] - b["player_y"]) > 0.01:
            notes.append("player position")
        if not close(a["pixel_at_reflection_centre"], b["pixel_at_reflection_centre"], 0.015):
            notes.append(f"reflection centre {a['pixel_at_reflection_centre']} vs {b['pixel_at_reflection_centre']}")
        if not close(a["open_water_pixel_100_600"], b["open_water_pixel_100_600"], 0.015):
            notes.append(f"open water {a['open_water_pixel_100_600']} vs {b['open_water_pixel_100_600']}")
        if not rel(a["mask_coloured_pixels"], b["mask_coloured_pixels"], 0.05, 100):
            notes.append(f"mask pixels {a['mask_coloured_pixels']} vs {b['mask_coloured_pixels']}")
        if not rel(a["reflection_pixels_changed"], b["reflection_pixels_changed"], 0.03, 200):
            notes.append(f"reflection pixels {a['reflection_pixels_changed']} vs {b['reflection_pixels_changed']}")
    return notes


def main():
    direct, sv = load(sys.argv[1]), load(sys.argv[2])
    keys = sorted(direct)
    bad = 0
    missing = 0
    caps = set()
    for k in keys:
        if k not in sv:
            print(f"MISSING  {k[0]} t={k[1]}: no 4K-route probe")
            missing += 1
            continue
        caps.add(k[0])
        notes = compare(direct[k], sv[k])
        if notes:
            bad += 1
            print(f"DIFFERENT {k[0]} t={k[1]}: " + "; ".join(notes))
        else:
            print(f"OK        {k[0]} t={k[1]}")
    print(f"\n{len(keys)} probes over {len(caps)} captures: {len(keys) - bad - missing} identical within tolerance, {bad} different, {missing} missing")
    sys.exit(1 if bad or missing else 0)


if __name__ == "__main__":
    main()

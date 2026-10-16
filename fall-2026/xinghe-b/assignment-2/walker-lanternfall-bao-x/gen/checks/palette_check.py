#!/usr/bin/env python3
"""Check 4: shipped sprites use only their declared palette, binary alpha and exact frame geometry.

    python gen/checks/palette_check.py [--allow-missing]
"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "godot" / "assets" / "art"


def rgb(h: str) -> tuple:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminance(path: Path) -> float:
    a = np.asarray(Image.open(path).convert("RGBA")).astype(float) / 255
    opaque = a[..., 3] > 0.5
    lin = np.where(a[..., :3] <= 0.04045, a[..., :3] / 12.92, ((a[..., :3] + 0.055) / 1.055) ** 2.4)
    return float((lin[opaque] @ np.array([0.2126, 0.7152, 0.0722])).mean())


def main() -> int:
    allow_missing = "--allow-missing" in sys.argv
    manifest = json.loads((ART / "manifest.json").read_text())
    palettes = {k: {rgb(c) for c in v} for k, v in json.loads((ART / "palettes.json").read_text()).items()}
    results, ok_all = [], True
    for name, spec in manifest.items():
        path = ART / name
        r = {"file": name, "id": spec["id"]}
        if not path.exists():
            r["status"] = "MISSING"
            ok_all = ok_all and allow_missing
            results.append(r)
            continue
        im = Image.open(path).convert("RGBA")
        fw, fh = spec["frame"]
        want = (fw * spec["frames"], fh)
        pal = palettes[spec["palette"]]
        px = [tuple(int(v) for v in p) for p in np.asarray(im).reshape(-1, 4)]
        bad_alpha = sum(1 for p in px if p[3] not in (0, 255))
        bad_color = sum(1 for p in px if p[3] == 255 and p[:3] not in pal)
        opaque = sum(1 for p in px if p[3] == 255)
        ok = im.size == want and bad_alpha == 0 and bad_color == 0 and opaque > 0
        ok_all = ok_all and ok
        r.update(status="PASS" if ok else "FAIL", size=list(im.size), want=list(want), bad_alpha=bad_alpha, bad_color=bad_color, opaque=opaque)
        results.append(r)
    # prediction 4: enemies must stand out from the ground (moth gated; wraith recorded for the muted playtest)
    ground = ART / "env_ground_tile.png"
    if ground.exists():
        g = luminance(ground)
        for name, need in (("enemy_moth.png", 0.25), ("enemy_wraith.png", None), ("pc_sheet.png", None)):
            if (ART / name).exists():
                diff = abs(luminance(ART / name) - g)
                ok = need is None or diff >= need
                ok_all = ok_all and ok
                results.append({"file": name, "id": "contrast-vs-ground", "status": "PASS" if ok else "FAIL",
                                "luminance_diff": round(diff, 3), "required": need})
    (ROOT / "evidence").mkdir(exist_ok=True)
    (ROOT / "evidence" / "palette-check.json").write_text(json.dumps(results, indent=2) + "\n")
    for r in results:
        print(r["status"], r["id"], r["file"], {k: v for k, v in r.items() if k not in ("status", "id", "file")})
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())

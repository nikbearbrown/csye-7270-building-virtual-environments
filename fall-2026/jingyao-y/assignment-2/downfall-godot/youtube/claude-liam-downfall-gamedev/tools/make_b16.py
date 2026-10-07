"""Render images/B16-test-output.png from the real run_all.ps1 logs of two fresh clones.

  python tools/make_b16.py <log of f770e26 clone> <log of 111bf6e clone>

Only lines that actually appear in the logs are drawn (suite result lines and
the failing error); nothing is typed in by hand.
"""
import re, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
RESULT = re.compile(r"(RESULT|checks|passed|failures|SCRIPT ERROR|Failed:|audio:|no errors)", re.I)


def pick(path, limit):
    text = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
    keep = [l.strip() for l in text if RESULT.search(l) and len(l.strip()) < 110 and not l.strip().startswith("+")]
    return keep[-limit:]


before = pick(sys.argv[1], 6)
after = pick(sys.argv[2], 17)
W, H = 3840, 2160
o = Image.new("RGB", (W, H), "#FAF9F5")
d = ImageDraw.Draw(o)
mono = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 40)
ui = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 56)
d.text((210, 100), "run_all.ps1 -Visual on fresh git clones", font=ImageFont.truetype("C:/Windows/Fonts/georgia.ttf", 92), fill="#2f2b26")


def panel(x, y, w, title, lines, colour):
    h = 140 + 58 * len(lines)
    d.rectangle([x, y, x + w, y + h], fill="#202531")
    d.text((x + 36, y + 30), title, font=ui, fill=colour)
    for i, line in enumerate(lines):
        bad = re.search(r"FAIL |ERROR|Failed", line) and "0 fail" not in line.lower()
        d.text((x + 36, y + 120 + 58 * i), line, font=mono, fill="#ff8a7a" if bad else "#d7e4ef")
    return y + h


y = panel(210, 300, 3420, "f770e26 (before the ignore-rule fix): last lines", before, "#ff8a7a")
panel(210, y + 60, 3420, "111bf6e (submitted source): suite results, capture_v1 flaky once, clean on both reruns", after, "#9fe08a")
o.save(REEL / "images" / "B16-test-output.png")
print(len(before), len(after))

#!/usr/bin/env python3
"""make_contact_sheet.py: one picture of the planning stills (png/), labelled with the beat each one serves.
Writes contact-sheet.png next to this file. Needs Pillow only; run after run_lab_checks.py.
"""
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
TILES = [
    ("A1-signed-slope-0.5", "B08 signed test, slope 0.5"),
    ("A2-signed-slope-1.0", "B09 slope 1.0"),
    ("C-02-angle-30", "B11 angle 30 (climbs right)"),
    ("I-radians-30", "B12 with / without radians"),
    ("G-signed-slope-89.9", "B14 slope form at 89.9"),
    ("G-signed-slope-90", "B14 slope form at 90"),
    ("D-step-order", "B16 band, angle 45"),
    ("D-raw-45", "B17 raw band at 45"),
    ("D-raw-75", "B17 raw band at 75"),
    ("D-true-45", "B20 true band at 45"),
    ("I-bands-45", "B21 old | new at 45"),
    ("I-bands-85", "B21 old | new at 85"),
    ("E-slide-35-0.5", "B22 offset 0.5 at 35"),
    ("I-center-0.6", "B23 centre shift | offset"),
    ("F-leak-0.0", "B24/B25 first attempt (leak)"),
    ("I-leak--0.1", "B26 leak | fixed"),
    ("F-fixed-0.3", "B29 finished shine"),
    ("I-wide-45", "B30 wide | fixed"),
    ("G-dir-30", "B34 direction form at 30"),
    ("I-seam-90.0", "B35 slope form | direction form at 90"),
]
TW, TH, COLS = 320, 180, 4
rows = (len(TILES) + COLS - 1) // COLS
sheet = Image.new("RGB", (COLS * (TW + 6) + 6, rows * (TH + 24) + 6), (250, 249, 245))
d = ImageDraw.Draw(sheet)
for i, (name, label) in enumerate(TILES):
    im = Image.open(HERE / "png" / f"{name}.png").convert("RGB").resize((TW, TH))
    x = 6 + (i % COLS) * (TW + 6)
    y = 6 + (i // COLS) * (TH + 24)
    sheet.paste(im, (x, y + 18))
    d.text((x, y + 3), f"{label}  [{name}]", fill=(61, 57, 41))
sheet.save(HERE / "contact-sheet.png")
print("wrote", HERE / "contact-sheet.png", sheet.size)

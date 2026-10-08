#!/usr/bin/env python3
"""Put the step 5 screenshots beside the design they were made for, for TEST-REPORT.md.

    python3 design/tools/compare_sheets.py <revision>

Reads capture step 5's files in evidence/5/ (run it twice, the second time with
--debug-collisions) and writes, in evidence/5/:
- 5-storyboard-vs-slice.jpg: each storyboard blockout (design/storyboard/)
  beside the in-engine moment of the same panel;
- 5-character-vs-sheet-default.jpg and 5-character-vs-sheet-sword.jpg: each
  of Rudy's game poses as CHARACTER-SHEET.md draws it (design/character/
  poses.png, the blockout), beside the in-engine crops facing right and left,
  and the same crops with the collision shapes drawn.
<revision> is the commit the screenshots were taken from; it is printed on the
sheets. Code written by Claude Code.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
_spec = importlib.util.spec_from_file_location("make_blockouts", HERE / "make_blockouts.py")
bo = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bo)

EVIDENCE = ROOT / "evidence" / "5"
BG = (244, 241, 234)
FRAME = "#B9AEA0"

PANELS = [
    ("01-first-sight", "Panel 1: first sight, the title over the opening of play"),
    ("02-core-action", "Panel 2: core action, over the spikes, onto a goblin"),
    ("03-success", "Panel 3: success, the sword and shield"),
    ("04-failure", "Panel 4: failure, a hit knocks the gear away"),
    ("05-recovery", "Panel 5: recovery, back at the waystone"),
    ("06-teleport-circle", "Panel 6: the end, the teleport circle"),
    ("07-level-complete", "Panel 7: level complete, the road to the castle"),
]

# poses.png: four columns of cells, numbered left to right, top to bottom.
SHEET_COLS = [(10, 420), (440, 850), (870, 1280), (1300, 1710)]
SHEET_ROWS = [(130, 580), (600, 1050), (1070, 1520), (1540, 1990)]
DEFAULT_FORM = [("CHAR-IDLE", 2), ("CHAR-RUN-A", 3), ("CHAR-RUN-B", 4), ("CHAR-RISE", 5), ("CHAR-FALL", 6),
                ("CHAR-HURT", 7), ("CHAR-DEFEAT", 8), ("CHAR-RESPAWN", 9), ("CHAR-CELEBRATE", 10)]
SWORD_FORM = [("CHAR-SWORD-IDLE", 11), ("CHAR-SWORD-RUN-A", 3), ("CHAR-SWORD-RUN-B", 4),
              ("CHAR-SWORD-RISE", 5), ("CHAR-SWORD-FALL", 6), ("CHAR-SWORD-SLASH", 12)]


def fit(im: Image.Image, w: int, h: int) -> Image.Image:
    scale = min(w / im.width, h / im.height)
    return im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)


def sheet_cell(number: int) -> Image.Image:
    poses = Image.open(ROOT / "design" / "character" / "poses.png").convert("RGB")
    x0, x1 = SHEET_COLS[(number - 1) % 4]
    y0, y1 = SHEET_ROWS[(number - 1) // 4]
    return poses.crop((x0, y0, x1, y1))


def storyboard(revision: str) -> None:
    w, h = 860, 484
    head, row_h = 70, h + 60
    out = Image.new("RGB", (40 + 2 * w + 20, head + len(PANELS) * row_h + 30), BG)
    d = ImageDraw.Draw(out)
    d.text((20, 18), "Storyboard against the slice: the blockout (left) and the same moment in the game (right)",
           font=bo.font(24), fill=bo.rgb(bo.LINE))
    for i, (name, label) in enumerate(PANELS):
        y = head + i * row_h
        d.text((20, y), label, font=bo.font(18), fill=bo.rgb(bo.LINE))
        board = fit(Image.open(ROOT / "design" / "storyboard" / f"{name}.png").convert("RGB"), w, h)
        game = fit(Image.open(EVIDENCE / f"5-panel-{i + 1}.jpg").convert("RGB"), w, h)
        for j, im in enumerate([board, game]):
            x = 20 + j * (w + 20)
            out.paste(im, (x, y + 30))
            d.rectangle([x - 1, y + 29, x + im.width, y + 30 + im.height], outline=bo.rgb(FRAME))
    d.text((20, out.height - 24), f"left: design/storyboard/ blockouts (code-drawn, design-v1); right: "
           f"evidence/5/5-panel-N.jpg, capture step 5 at revision {revision}, 1920 x 1080",
           font=bo.font(13, bold=False), fill=bo.rgb(bo.LINE))
    path = EVIDENCE / "5-storyboard-vs-slice.jpg"
    out.save(path, quality=88)
    print("wrote", path.relative_to(ROOT))


def character(form: str, poses: list, revision: str) -> None:
    crop_w, crop_h = 390, 285
    cell_w = 262
    columns = ["character sheet (blockout)", "in-engine, facing right", "facing left",
               "facing right, collisions", "facing left, collisions"]
    head, row_h = 96, crop_h + 44
    width = 20 + cell_w + 20 + 4 * (crop_w + 16) + 4
    out = Image.new("RGB", (width, head + len(poses) * row_h + 34), BG)
    d = ImageDraw.Draw(out)
    d.text((20, 18), f"Character against the sheet: Rudy's {form}", font=bo.font(24), fill=bo.rgb(bo.LINE))
    xs = [20] + [20 + cell_w + 20 + k * (crop_w + 16) for k in range(4)]
    for x, title in zip(xs, columns):
        d.text((x, 62), title, font=bo.font(15), fill=bo.rgb(bo.LINE))
    for i, (pose, number) in enumerate(poses):
        y = head + i * row_h
        d.text((20, y), f"{pose}  (sheet pose #{number})", font=bo.font(16), fill=bo.rgb(bo.LINE))
        cell = fit(sheet_cell(number), cell_w, crop_h)
        out.paste(cell, (xs[0], y + 26))
        d.rectangle([xs[0] - 1, y + 25, xs[0] + cell.width, y + 26 + cell.height], outline=bo.rgb(FRAME))
        for k, suffix in enumerate(["right", "left", "right-collisions", "left-collisions"]):
            path = EVIDENCE / f"5-{pose}-{suffix}.jpg"
            x = xs[k + 1]
            if not path.exists():
                d.rectangle([x - 1, y + 25, x + crop_w, y + 26 + crop_h], outline=bo.rgb(FRAME))
                d.text((x + 16, y + 26 + crop_h // 2 - 10), "not in the game: he always gets up facing right",
                       font=bo.font(14, bold=False), fill=bo.rgb(bo.LINE))
                continue
            im = fit(Image.open(path).convert("RGB"), crop_w, crop_h)
            out.paste(im, (x, y + 26))
            d.rectangle([x - 1, y + 25, x + im.width, y + 26 + im.height], outline=bo.rgb(FRAME))
    d.text((20, out.height - 24), f"sheet: design/character/poses.png (blockout, design-v1); in-engine: "
           f"evidence/5/, capture step 5 at revision {revision}, crops 520 x 380 px at game size shown at 3/4",
           font=bo.font(13, bold=False), fill=bo.rgb(bo.LINE))
    path = EVIDENCE / f"5-character-vs-sheet-{form.split()[0]}.jpg"
    out.save(path, quality=88)
    print("wrote", path.relative_to(ROOT))


if __name__ == "__main__":
    rev = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    storyboard(rev)
    character("default form", DEFAULT_FORM, rev)
    character("sword form", SWORD_FORM, rev)

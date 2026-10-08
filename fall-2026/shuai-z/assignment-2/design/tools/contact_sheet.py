#!/usr/bin/env python3
"""Make a contact sheet of small thumbnails, so rejected outputs are kept without full-size files.

    python3 design/tools/contact_sheet.py -o generated/rejected/CHAR-REF-01-03.png \
        --title "CHAR-REF, round 1: not chosen" \
        "_raw/CHAR-REF-01.jpg::CHAR-REF-01 · base, plain robe" "_raw/CHAR-REF-02.jpg::CHAR-REF-02 · too ornate"

Each argument is "path::label". --footer replaces the note at the bottom, for sheets whose
full-size files are kept, such as the greybox screenshots in evidence/. Code written by Claude Code.
"""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("make_blockouts", HERE / "make_blockouts.py")
bo = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bo)

THUMB_W = 420


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("items", nargs="+", help='"path::label"')
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--title", default="")
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--footer", default="full-size files are not kept in git")
    args = ap.parse_args()
    items = []
    for it in args.items:
        path, _, label = it.partition("::")
        im = Image.open(path).convert("RGB")
        im = im.resize((THUMB_W, round(im.height * THUMB_W / im.width)), Image.LANCZOS)
        items.append((im, label or Path(path).name))
    cols = min(args.cols, len(items))
    th = max(im.height for im, _ in items)
    lines = max(len(label.split("\n")) for _, label in items)
    cell_h = th + 20 + 20 * lines
    rows = (len(items) + cols - 1) // cols
    W, H = 20 + cols * (THUMB_W + 20), 60 + rows * (cell_h + 10) + 30
    out = Image.new("RGB", (W, H), (244, 241, 234))
    d = ImageDraw.Draw(out)
    d.text((20, 18), args.title, font=bo.font(22), fill=bo.rgb(bo.LINE))
    for i, (im, label) in enumerate(items):
        x, y = 20 + (i % cols) * (THUMB_W + 20), 60 + (i // cols) * (cell_h + 10)
        out.paste(im, (x, y))
        d.rectangle([x - 1, y - 1, x + im.width, y + im.height], outline=bo.rgb("#B9AEA0"))
        for j, line in enumerate(label.split("\n")):
            d.text((x, y + im.height + 8 + 20 * j), line, font=bo.font(15, bold=(j == 0)), fill=bo.rgb(bo.LINE))
    d.text((20, H - 24), f"thumbnails {THUMB_W} px wide; {args.footer}",
           font=bo.font(12, bold=False), fill=bo.rgb(bo.LINE))
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    out.save(args.output)
    print("wrote", args.output)


if __name__ == "__main__":
    main()

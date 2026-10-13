#!/usr/bin/env python3
"""analyze_padding.py: reads the renders of verify_a_padding.gd (the trimmed disc with 0, 2, 4 and 6 pixels of padding, and the original art with its own padding, all with
lab-shaders/08-loop at thickness 4, scale 1) and measures the outline: width along the four axes and the number of outline pixels. Writes padding-summary.txt."""
from pathlib import Path
import ol_measure as M
HERE = Path(__file__).resolve().parent
L = ["== P1  the padding trap: 08-loop at thickness 4 on the trimmed 77 x 77 disc, by padding (scale 1)"]
for name, label in (("pad-tight-t4", "padding 0 (trimmed)"), ("pad-padded2-t4", "padding 2"), ("pad-padded4-t4", "padding 4"), ("pad-padded6-t4", "padding 6"),
                    ("pad-original-t4", "the original art, 128 x 128 with its own empty border")):
    im = M.load(HERE / f"png/{name}.png")
    c = M.classes(im)
    n_line = int((c["line"] | c["over"]).sum())
    L.append(f"  {label:58s} axis widths {M.axis_widths(im)}   outline pixels {n_line:5d}")
print("\n".join(L))
(HERE / "padding-summary.txt").write_text("\n".join(L) + "\n")

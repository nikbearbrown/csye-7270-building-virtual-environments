#!/usr/bin/env python3
"""embed_real_lines.py ACT — print the Python literal of the REAL source lines a scene file embeds (Gate A runs scenes.py from a folder
that holds only scenes.py, so a scene cannot open evidence/ at construct time). The scene files carry the output as A5_REAL / A7_REAL.
`verify_embedded.py` re-reads the frozen sources and fails if any embedded line differs.   python3 evidence/act5/embed_real_lines.py 5|7"""
import sys, pprint
WANT = {
 "5": {"surface.gdshader": range(1, 15), "gate-color.png.import": (16, 18, 24, 26), "gate-roughness.png.import": (18, 24, 26),
       "matte.tres": range(9, 13), "coated.tres": range(9, 13), "garden-textures.py": (2, 11, 12, 15)},
 "7": {"signal.gdshader": (1, 3), "surface.gdshader": (1, 3, 12), "hint.gdshader": (1, 3, 4, 9, 10),
       "standard_generated.gdshader": (3, 4, 6, 7, 19, 20, 35, 43, 46), "standard-source.tres": (6, 7, 10, 13)},
}
SRC = "evidence/example/sources/"
out = {}
for f, ns in WANT[sys.argv[1]].items():
    L = open(SRC + f).read().split("\n")
    out[f] = {n: L[n - 1] for n in ns}
print(f"A{sys.argv[1]}_REAL = " + pprint.pformat(out, width=150, sort_dicts=False))

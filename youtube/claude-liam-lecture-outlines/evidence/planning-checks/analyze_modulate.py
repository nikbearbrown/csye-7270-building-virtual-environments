#!/usr/bin/env python3
"""analyze_modulate.py: reads the black/white renders of verify_m_modulate.gd (three sprites, each with modulate alpha 0.5), solves the alpha the shader wrote
at the sprite's centre and at the outline, and writes modulate-summary.txt."""
from pathlib import Path
import numpy as np
import ol_measure as M
HERE = Path(__file__).resolve().parent
b = M.load(HERE / "png/modulate-on-black.png").astype(float); w = M.load(HERE / "png/modulate-on-white.png").astype(float)
a = np.clip(1.0 - (w - b).mean(axis=2) / 255.0, 0, 1)
L = ["== M1  modulate alpha 0.5 on three identical sprites (hard-edged disc, scale 1.5, thickness 2): the alpha each one actually draws"]
for k, name in enumerate(["no shader", "06-pixel-steps (COLOR assigned from the texture)", "14-modulate (vertex COLOR passed on as a varying)"]):
    x0 = 20 + k * 200
    sub = a[116:116 + 192, x0:x0 + 192]
    cy, cx = 96, 96
    L.append(f"  {name:52s} alpha at the sprite centre {sub[cy, cx]:.2f}; at the outline, 59 px right of the centre {sub[cy, cx + 59]:.2f}")
print("\n".join(L))
(HERE / "modulate-summary.txt").write_text("\n".join(L) + "\n")

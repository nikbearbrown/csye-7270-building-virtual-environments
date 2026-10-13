#!/usr/bin/env python3
"""make_crops.py — Act VII: crop the REAL evidence images (pantry/ev_*.png) into the a7_* stills the Manim scenes show.
Crops only: no pixel is drawn, retouched or recoloured. Boxes are pixels of the source PNG (x0, y0, x1, y1); the Blender
boxes come from evidence/gui/NOTES.md. A crop that is shown on a new path is never overwritten under the same name
(Manim caches by file path): bump the suffix instead.
Run from anywhere:  python3 evidence/act7/make_crops.py
"""
from pathlib import Path
import shutil
from PIL import Image

REEL = Path(__file__).resolve().parents[2]
P = REEL / "pantry"

CROPS = {
    # B61A tiles (aspect 2.9 / 2.1 = 1.381)
    "a7_godot_tile.png":       ("ev_godot_showcase.png",      (400, 120, 1850, 1170)),   # the three assets in the running Godot scene
    "a7_bl_session_tile.png":  ("ev_bl_object_mode.png",      (0, 0, 2432, 1761)),        # Blender window: toolbar, viewport, sidebar (Object Mode)
    "a7_hand_before_tile.png": ("ev_bl_hand_edit_before.png", (0, 500, 1300, 1441)),      # lantern, flame selected, before the edit (illustrative); sidebar left out
    "a7_hand_after_tile.png":  ("ev_bl_hand_edit_after.png",  (0, 500, 1300, 1441)),      # same box after: flame up 0.02 m, colour blue (illustrative)
    # B61B / B69: the Godot scene, wide (16:9)
    "a7_godot_wide.png":       ("ev_godot_showcase.png",      (300, 100, 1950, 1028)),
    # B62: a real Blender screenshot tile (viewport with the lantern)
    "a7_bl_view_tile.png":     ("ev_bl_object_mode.png",      (0, 500, 1300, 1441)),
    # B68: the sidebar's Transform panel, two real crops (Location; Scale + Dimensions)
    "a7_bl_location.png":      ("ev_bl_object_mode.png",      (1350, 345, 2320, 690)),
    "a7_bl_scale_dims.png":    ("ev_bl_object_mode.png",      (1350, 1096, 2320, 1765)),
}

# GATE T pass (2026-10-06): the first crops of ev_godot_showcase.png and the lantern viewport tile failed GATE T's per-blob contrast
# (the dark lantern roof / shadow read as low-contrast "text"). Look A of the SAME logged capture run (evidence/godot/capture_showcase.log:
# "look A: sun 1.2 fov 40.0 -> .../godot_showcase_A.png (2400, 1350)") passes, so it is copied into pantry and used instead.
LOOK_A = Path("/private/tmp/claude-501/a3film/godot_cap/godot_showcase_A.png")
if LOOK_A.exists() and not (P / "a7_godot_lookA.png").exists():
    shutil.copyfile(LOOK_A, P / "a7_godot_lookA.png")
CROPS.update({
    "a7_godot_tile2.png":      ("a7_godot_lookA.png",         (400, 150, 1850, 1200)),   # B61A frame 1 (replaces a7_godot_tile.png)
    "a7_bl_view_tile2.png":    ("ev_bl_object_mode.png",      (0, 300, 1310, 1250)),      # B62 screenshot tile (replaces a7_bl_view_tile.png; the lantern base is cropped off: it failed GATE T on the tile edge)
    "a7_godot_lookA_wide.png": ("a7_godot_lookA.png",         (400, 200, 1700, 931)),     # B61B and B69 (replaces a7_godot_wide.png)
})

for out, (src, box) in CROPS.items():
    im = Image.open(P / src).convert("RGB").crop(box)
    im.save(P / out)
    print(f"{out:26s} <- {src} {box}  {im.size[0]}x{im.size[1]}  aspect {im.size[0] / im.size[1]:.3f}")

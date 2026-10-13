#!/usr/bin/env python3
"""crop_a5.py - crops of the REAL Blender 5.1.2 window shots (Blender's own screenshot operator, by script; see ../gui/NOTES.md)
into pantry/a5_*.png for Act V. Crops only: no pixel is altered. Boxes are pixels in the 3456 x 2006 originals (origin top-left).
  a5_viewport_lantern.png       ev_bl_object_mode.png, the viewport around the finished lantern (no interface text in the box)   B46
  a5_hand_before_flame.png      ev_bl_hand_edit_before.png, roof + flame + top of the glass (illustrative pair)                  B47
  a5_hand_after_flame.png       ev_bl_hand_edit_after.png,  same box
  a5_hand_before_location.png   ev_bl_hand_edit_before.png, the sidebar Location panel, no lock icons                            B47
  a5_hand_after_location.png    ev_bl_hand_edit_after.png,  same box (Z 0.34 m)
"""
from pathlib import Path
from PIL import Image
P = Path(__file__).resolve().parents[2] / "pantry"
CROPS = [
    ("ev_bl_object_mode.png",      "a5_viewport_lantern.png",     (380, 520, 1060, 1450)),
    ("ev_bl_hand_edit_before.png", "a5_hand_before_flame.png",    (590, 520, 900, 1010)),
    ("ev_bl_hand_edit_after.png",  "a5_hand_after_flame.png",     (590, 520, 900, 1010)),
    ("ev_bl_hand_edit_before.png", "a5_hand_before_location.png", (1350, 350, 2110, 680)),
    ("ev_bl_hand_edit_after.png",  "a5_hand_after_location.png",  (1350, 350, 2110, 680)),
]
for src, dst, box in CROPS:
    im = Image.open(P / src).convert("RGB")
    assert im.size == (3456, 2006), (src, im.size)
    im.crop(box).save(P / dst)
    print(dst, box, Image.open(P / dst).size)

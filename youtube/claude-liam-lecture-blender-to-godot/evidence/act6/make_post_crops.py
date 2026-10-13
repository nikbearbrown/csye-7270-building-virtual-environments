#!/usr/bin/env python3
"""make_post_crops.py — crops the real Blender renders (pantry/post_visual.png, post_collider_only.png; Blender's Workbench engine, same camera)
into the two images Act V part 2 shows, with no re-drawing:
  pantry/a6_post_visual.png   the post, cropped to its bounding box + margin
  pantry/a6_post_overlay.png  the same crop with the real collider render laid over it at 40 % (the invisible collision around the pole)
Run from the REEL folder:  python3 evidence/act6/make_post_crops.py
"""
from pathlib import Path
from PIL import Image
P = Path(__file__).resolve().parents[2] / "pantry"
vis = Image.open(P / "post_visual.png").convert("RGBA")
col = Image.open(P / "post_collider_only.png").convert("RGBA")
assert vis.size == col.size
bb = vis.getbbox(); cb = col.getbbox(); print("post bbox", bb, "collider bbox", cb)
x0, y0, x1, y1 = min(bb[0], cb[0]) - 40, min(bb[1], cb[1]) - 40, max(bb[2], cb[2]) + 40, max(bb[3], cb[3]) + 40
box = (x0, y0, x1, y1)
v = vis.crop(box); c = col.crop(box)
v.save(P / "a6_post_visual.png")
r, g, b, a = c.split(); a = a.point(lambda p: int(p * 0.40))
cg = Image.merge("RGBA", (r, g, b, a))
o = Image.new("RGBA", v.size, (0, 0, 0, 0)); o.alpha_composite(v); o.alpha_composite(cg)
o.save(P / "a6_post_overlay.png")
print("crop", box, v.size)

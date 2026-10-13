# Crops the 2x Blender renders (render_a5.py) into the pantry files and rewrites the anchors in crop pixel space.
# Run: python3 crop_a5.py <render_dir>     (reads a5_post_full.png, a5_box_full.png, post_anchors_full.json)
import json, sys, os
from PIL import Image
src = sys.argv[1]
here = os.path.dirname(os.path.abspath(__file__))
pantry = os.path.abspath(os.path.join(here, "..", "..", "pantry"))
post = Image.open(os.path.join(src, "a5_post_full.png")); box = Image.open(os.path.join(src, "a5_box_full.png")); bop = Image.open(os.path.join(src, "a5_boxopaque_full.png"))
bb = post.split()[3].getbbox(); bb2 = box.split()[3].getbbox()
x0 = min(bb[0], bb2[0]); y0 = min(bb[1], bb2[1]); x1 = max(bb[2], bb2[2]); y1 = max(bb[3], bb2[3])
# the crop window: post silhouette plus room for dimension marks on both sides (fixed, so every a5_* image shares it)
CX0, CY0, CX1, CY1 = x0 - 330, y0 - 90, x1 + 330, y1 + 90
print("silhouette", (x0, y0, x1, y1), "crop", (CX0, CY0, CX1, CY1), "size", (CX1 - CX0, CY1 - CY0))
post.crop((CX0, CY0, CX1, CY1)).save(os.path.join(pantry, "a5_post.png"))
box.crop((CX0, CY0, CX1, CY1)).save(os.path.join(pantry, "a5_box.png"))
bop.crop((CX0, CY0, CX1, CY1)).save(os.path.join(pantry, "a5_boxopaque.png"))
A = json.load(open(os.path.join(src, "post_anchors_full.json")))
pts = {k: [round(v[0] - CX0, 1), round(v[1] - CY0, 1)] for k, v in A["pts"].items()}
json.dump({"crop_size": [CX1 - CX0, CY1 - CY0], "crop_origin_in_render": [CX0, CY0], "render_res": A["res"], "camera": A["camera"], "pts": pts},
          open(os.path.join(here, "post_anchors.json"), "w"), indent=1)

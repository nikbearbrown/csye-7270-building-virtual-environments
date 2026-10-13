#!/usr/bin/env python3
"""Act II pantry crops (pure PIL, no new content): a2_lab_warning.png = the Security Warning box of the real blender.org/lab/mcp-server capture;
a2_post.png = the real Blender render of the checkpoint post (pantry/post_visual.png) cropped to its own bounding box."""
from PIL import Image
import pathlib
HERE = pathlib.Path(__file__).resolve().parent
REEL = HERE.parent.parent
PUB = pathlib.Path("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/lecture-blender-to-godot")
page = Image.open(PUB / "a2_lab_page.png").convert("RGB")
# css box of the warning card (x 255-1345, y 416-583) x2.4 device scale, with a little margin
page.crop((600, 985, 3240, 1415)).save(REEL / "pantry" / "a2_lab_warning.png")
post = Image.open(REEL / "pantry" / "post_visual.png")
bb = post.getbbox()
post.crop((bb[0] - 20, bb[1] - 20, bb[2] + 20, bb[3] + 20)).save(REEL / "pantry" / "a2_post.png")
print("ok")

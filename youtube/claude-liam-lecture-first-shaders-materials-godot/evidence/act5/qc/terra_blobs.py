import sys
sys.path.insert(0, "/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/scripts")
import numpy as np
from PIL import Image
import type_check as tc
img = Image.open(sys.argv[1]).convert("RGB"); arr = np.array(img)
m = tc.ink_mask(arr, tc.hex_to_rgb(tc.ACC_HEX), tol=40)
lab, n = tc.labeled_blobs(m)
raw = tc.blob_bboxes(lab, n)
print("terracotta blobs", len(raw))
for b in tc.text_run_bboxes(raw, img.height):
    x0,y0,x1,y1,px=b
    print("FLAGGED bbox px:", b, " in scene units: x %.2f..%.2f y %.2f..%.2f" % ((x0-1920)/270,(x1-1920)/270,(1080-y1)/270,(1080-y0)/270))

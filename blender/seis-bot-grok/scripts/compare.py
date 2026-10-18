import sys
from PIL import Image, ImageDraw
# compare.py out.png render.png ref.png [label]
out, a, b = sys.argv[1:4]
A = Image.open(a).convert('RGB'); Bm = Image.open(b).convert('RGB')
H = 900
A = A.resize((int(A.width * H / A.height), H)); Bm = Bm.resize((int(Bm.width * H / Bm.height), H))
C = Image.new('RGB', (A.width + Bm.width + 10, H + 40), (20, 20, 20))
C.paste(A, (0, 40)); C.paste(Bm, (A.width + 10, 40))
d = ImageDraw.Draw(C); d.text((10, 12), 'v3 render', fill=(255, 255, 255)); d.text((A.width + 20, 12), 'reference', fill=(255, 255, 255))
C.save(out)

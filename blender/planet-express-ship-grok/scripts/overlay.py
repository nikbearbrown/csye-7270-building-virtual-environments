# 50/50 overlay of reference and render + render silhouette edge (magenta) on the reference
import sys,os
from PIL import Image,ImageChops,ImageFilter,ImageOps
R=sys.argv[1]; views=sys.argv[2:]; H='/workspace/ships/planet-express'
os.makedirs(f'{H}/analysis',exist_ok=True)
for v in views:
    a=Image.open(f'{H}/refs/{v}.png').convert('RGB'); b=Image.open(f'{H}/renders/{R}/{v}.png').convert('RGB').resize(a.size)
    bg=Image.new('RGB',b.size,(0xD9,0xDA,0xDB))
    hsv=b.convert('HSV').split()[1]
    m=ImageChops.lighter(hsv.point(lambda p:255 if p>40 else 0),ImageChops.difference(b,bg).convert('L').point(lambda p:255 if p>40 else 0))
    m=m.filter(ImageFilter.MedianFilter(5))
    e=m.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(3))
    o=Image.blend(a,b,0.5); o.paste((255,0,255),mask=e)
    o.save(f'{H}/analysis/{R}_{v}_overlay.jpg',quality=90)

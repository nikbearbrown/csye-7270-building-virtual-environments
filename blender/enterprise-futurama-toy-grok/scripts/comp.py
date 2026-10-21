# composite transparent renders over studio grey gradient: python3 comp.py renders/rN
import sys,glob,os
from PIL import Image
for f in glob.glob(sys.argv[1]+'/*.png'):
    if f.endswith('_c.jpg'): continue
    im=Image.open(f).convert('RGBA'); w,h=im.size
    bg=Image.new('RGBA',(w,h))
    top=(236,236,236); bot=(212,212,212)
    grad=Image.linear_gradient('L').resize((w,h))
    bg=Image.composite(Image.new('RGBA',(w,h),bot+(255,)),Image.new('RGBA',(w,h),top+(255,)),grad)
    bg.alpha_composite(im); bg.convert('RGB').save(f[:-4]+'.jpg',quality=92)

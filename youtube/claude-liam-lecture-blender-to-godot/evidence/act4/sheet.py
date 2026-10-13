# contact sheet of the preflight last-frame stills: python3 sheet.py out.png Class1 Class2 ...
import sys
from PIL import Image, ImageDraw
D="/private/tmp/claude-501/lecture-blender-act4/stills/"
names=sys.argv[2:]
ims=[Image.open(D+n+".png").convert("RGB") for n in names]
w,h=ims[0].size
cols=2; rows=(len(ims)+1)//2
S=Image.new("RGB",(w*cols,h*rows),(255,255,255))
for i,im in enumerate(ims):
    S.paste(im,((i%cols)*w,(i//cols)*h)); ImageDraw.Draw(S).text(((i%cols)*w+6,(i//cols)*h+4),names[i],fill=(200,0,0))
S.save(sys.argv[1])

# Original procedural approximation of the circular rocket logo (no copied artwork).
from PIL import Image, ImageDraw, ImageFont
import math
S=1024; im=Image.new('RGBA',(S,S),(0,0,0,0)); d=ImageDraw.Draw(im); c=S/2
d.ellipse([4,4,S-4,S-4],fill=(20,20,20,255))
d.ellipse([22,22,S-22,S-22],fill=(245,244,236,255))
d.ellipse([c-300,c-300,c+300,c+300],fill=(20,20,20,255))
d.ellipse([c-286,c-286,c+286,c+286],fill=(205,45,40,255))
try: f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',120)
except: f=ImageFont.load_default()
def arc(text,start,end,r,flip=False):
    n=len(text)
    for i,ch in enumerate(text):
        a=math.radians(start+(end-start)*(i+0.5)/n)
        g=Image.new('RGBA',(150,150),(0,0,0,0)); ImageDraw.Draw(g).text((75,75),ch,font=f,fill=(20,20,20,255),anchor='mm')
        rot=-math.degrees(a)-90 if not flip else -math.degrees(a)+90
        g=g.rotate(rot,resample=Image.BICUBIC)
        x=c+r*math.cos(a); y=c+r*math.sin(a)
        im.alpha_composite(g,(int(x-75),int(y-75)))
arc('PLANET',-150,-30,405)
arc('EXPRESS',150,30,405,flip=True)
# rocket, diagonal
rk=Image.new('RGBA',(S,S),(0,0,0,0)); r=ImageDraw.Draw(rk)
r.ellipse([c-70,c-260,c+70,c+200],fill=(60,150,140,255),outline=(20,20,20,255),width=10)
r.polygon([(c-70,c+60),(c-170,c+250),(c-60,c+170)],fill=(60,150,140,255),outline=(20,20,20,255))
r.polygon([(c+70,c+60),(c+170,c+250),(c+60,c+170)],fill=(60,150,140,255),outline=(20,20,20,255))
r.ellipse([c-35,c-140,c+35,c-70],fill=(240,240,230,255),outline=(20,20,20,255),width=8)
r.line([(c,c+200),(c,c+330)],fill=(240,240,230,255),width=26)
rk=rk.rotate(-35,resample=Image.BICUBIC,center=(c,c))
im.alpha_composite(rk)
im.save('logo.png')

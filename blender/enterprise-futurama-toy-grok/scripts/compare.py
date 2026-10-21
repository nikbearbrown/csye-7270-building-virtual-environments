# python3 compare.py rN  -> compare/rN_*.jpg
import sys,os
from PIL import Image,ImageDraw,ImageFont
R=sys.argv[1]; H='/workspace/ships/enterprise-futurama'; os.makedirs(f'{H}/compare',exist_ok=True)
try: F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
except: F=ImageFont.load_default()
def lab(im,t):
    d=ImageDraw.Draw(im); w=d.textlength(t,font=F); d.rectangle([0,0,w+16,32],fill='black'); d.text((8,4),t,fill='white',font=F)
def stack(a,b,la,lb,out,horiz=False,W=1024):
    a=a.convert('RGB'); b=b.convert('RGB')
    if horiz:
        hh=600; a=a.resize((int(a.width*hh/a.height),hh)); b=b.resize((int(b.width*hh/b.height),hh))
        c=Image.new('RGB',(a.width+b.width+6,hh),'black'); c.paste(a,(0,0)); c.paste(b,(a.width+6,0))
        lab(a,la); lab(b,lb); c.paste(a,(0,0)); c.paste(b,(a.width+6,0))
    else:
        a=a.resize((W,int(a.height*W/a.width))); b=b.resize((W,int(b.height*W/b.width)))
        lab(a,la); lab(b,lb)
        c=Image.new('RGB',(W,a.height+b.height+6),'black'); c.paste(a,(0,0)); c.paste(b,(0,a.height+6))
    c.save(out,quality=90); return c
r=f'{H}/renders/{R}'
stack(Image.open(f'{H}/refs/concept.jpg'),Image.open(f'{r}/hero.jpg'),'CONCEPT (style target)',f'GROK BOT {R} - 3/4 hero',f'{H}/compare/{R}_hero_vs_concept.jpg')
def bpify(p):  # render as light line-ish image for blueprint comparison
    im=Image.open(p).convert('RGBA'); bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im); return bg
stack(Image.open(f'{H}/refs/bp_side.png'),bpify(f'{r}/side.png'),'BLUEPRINT side',f'GROK BOT {R} side',f'{H}/compare/{R}_side_vs_blueprint.jpg')
stack(Image.open(f'{H}/refs/bp_top.png'),bpify(f'{r}/top.png'),'BLUEPRINT top',f'GROK BOT {R} top',f'{H}/compare/{R}_top_vs_blueprint.jpg')
stack(Image.open(f'{H}/refs/bp_front.png'),bpify(f'{r}/front.png'),'BLUEPRINT front',f'GROK BOT {R} front',f'{H}/compare/{R}_front_vs_blueprint.jpg',horiz=True)
print('ok')

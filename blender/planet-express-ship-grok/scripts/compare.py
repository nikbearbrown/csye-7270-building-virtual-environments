import sys,os,glob
from PIL import Image,ImageDraw
R=sys.argv[1]; H='/workspace/ships/planet-express'
os.makedirs(f'{H}/compare',exist_ok=True)
for f in sorted(glob.glob(f'{H}/renders/{R}/ref*.png')):
    n=os.path.basename(f)[:-4]
    a=Image.open(f'{H}/refs/{n}.png').convert('RGB'); b=Image.open(f).convert('RGB').resize(a.size)
    c=Image.new('RGB',(a.width,a.height*2+4),'black'); c.paste(a,(0,0)); c.paste(b,(0,a.height+4))
    d=ImageDraw.Draw(c); d.rectangle([0,0,120,18],fill='black'); d.text((4,3),f'REFERENCE {n}',fill='white')
    d.rectangle([0,a.height+4,120,a.height+22],fill='black'); d.text((4,a.height+7),f'GROK {R}',fill='white')
    c.save(f'{H}/compare/{R}_{n}.jpg',quality=90)

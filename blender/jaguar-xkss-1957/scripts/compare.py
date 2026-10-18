import sys
from PIL import Image, ImageDraw, ImageFont
R = sys.argv[1]; note = sys.argv[2] if len(sys.argv) > 2 else ''
B = '/workspace/cars/xkss/'
try: F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
except Exception: F = ImageFont.load_default()
for nm, ref in [('side', 'side.jpg'), ('front', 'front.jpg'), ('rear34', 'rear34.jpg')]:
    try: r = Image.open(B+f'renders/r{R}_{nm}.png').convert('RGB')
    except Exception: continue
    a = Image.open(B+'refs/'+ref).convert('RGB')
    h = 520; a = a.resize((int(a.width*h/a.height), h)); r = r.resize((int(r.width*h/r.height), h))
    c = Image.new('RGB', (a.width+r.width+10, h+40), 'white'); c.paste(a, (0, 40)); c.paste(r, (a.width+10, 40))
    d = ImageDraw.Draw(c)
    d.text((10, 8), 'Reference: Jaguar Classic XKSS photo', fill='black', font=F)
    d.text((a.width+20, 8), f'Grok Bot render - round {R} {note}', fill='black', font=F)
    c.save(B+f'compare/r{R}_{nm}_compare.jpg', quality=88)
print('ok')

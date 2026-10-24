"""Side-by-side composites: reference LEFT, render RIGHT. Captions must be correct."""
from PIL import Image, ImageDraw
import os

REF = {
    'side':    '/home/hatch/workspace/user/media_library/image/4c/4cfe58ed086d24707a6567ed7055f93def19bae94455e65d646446882da9fcb4.jpg',
    'rear34':  '/home/hatch/workspace/user/media_library/image/13/1321eae504d5c5c5bb3a558f09570e6fd6e169d769445cf7af86e5267aee5711.jpg',
    'front34': '/home/hatch/workspace/user/media_library/image/c7/c7a2f8edd289b1923ef8aa33db398bedaff7ec0f2ced60b9df5489d34714faa9.jpg',
}
REN = {
    'side':    '/home/hatch/workspace/xkss-publish/stage-renders/xkss_side.png',
    'rear34':  '/home/hatch/workspace/xkss-publish/stage-renders/xkss_rear34.png',
    'front34': '/home/hatch/workspace/xkss-publish/stage-renders/xkss_front34.png',
}
CAPTIONS = {
    'side':    'Side profile',
    'rear34':  'Rear three-quarter',
    'front34': 'Front three-quarter',
}
OUT = '/home/hatch/workspace/xkss-publish/stage-compare'
os.makedirs(OUT, exist_ok=True)
H = 720
CAP_H = 44

for k in ('side', 'rear34', 'front34'):
    ref = Image.open(REF[k]).convert('RGB')
    ren = Image.open(REN[k]).convert('RGB')
    ref = ref.resize((int(ref.width * H / ref.height), H))
    ren = ren.resize((int(ren.width * H / ren.height), H))
    W = ref.width + ren.width
    sheet = Image.new('RGB', (W, H + CAP_H), 'white')
    sheet.paste(ref, (0, 0))
    sheet.paste(ren, (ref.width, 0))
    d = ImageDraw.Draw(sheet)
    d.rectangle([0, H, W, H + CAP_H], fill=(24, 24, 24))
    d.text((12, H + 12), 'LEFT: Jaguar Classic XKSS reference photo (comparison only)', fill=(235, 235, 235))
    d.text((ref.width + 12, H + 12), 'RIGHT: jaguar-xkss-1957-muse render (v5)', fill=(235, 235, 235))
    # divider
    d.rectangle([ref.width - 2, 0, ref.width + 2, H], fill='white')
    out = os.path.join(OUT, f'compare_{k}.jpg')
    sheet.save(out, quality=88)
    print('wrote', out, sheet.size)

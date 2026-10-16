"""Sample each listed beat at 15/50/85% and tile into _qc/sheet_<first>_<last>.jpg."""
import json, subprocess, sys
from PIL import Image
s = json.load(open('beat_sheet.json', encoding='utf-8'))
d = {b['beat_id']: b.get('render_duration_s') or b['actual_duration_s'] for b in s['beats']}
ids = sys.argv[1:]
ims = []
for bid in ids:
    for f in (0.15, 0.5, 0.85):
        out = f'_qc/{bid}_{int(f*100)}.png'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{d[bid]*f:.2f}', '-i', f'media/{bid}.mp4',
                        '-frames:v', '1', '-vf', 'scale=960:-1', out], check=True)
        ims.append(Image.open(out))
sh = Image.new('RGB', (960*3, 540*len(ids)))
for i, im in enumerate(ims):
    sh.paste(im, ((i % 3)*960, (i//3)*540))
sh.save(f'_qc/sheet_{ids[0]}_{ids[-1]}.jpg', quality=88)

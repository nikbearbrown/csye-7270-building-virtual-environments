"""Sample the compiled film at 2 fps plus every beat's start, midpoint and end.

Keep native-resolution PNG evidence; make review pages after exact decoded-pixel
deduplication. Identical held frames need only one visual inspection, but retain
every timestamp and pixel hash in the manifest. No approximate-image dedup.
"""
import argparse,hashlib,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
sheet=json.loads((ROOT/'beat_sheet.json').read_text())
ap=argparse.ArgumentParser();ap.add_argument('--review',action='store_true');args=ap.parse_args()
suffix='-slate' if args.review else ''
source=ROOT/f"{sheet['metadata']['slug']}{suffix}.mp4"
folder=ROOT/'_qc'/('previz-sweep' if args.review else 'master-sweep');folder.mkdir(exist_ok=True)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),'-vf','fps=2','-compression_level','1',str(folder/'sample-%05d.png')],check=True)
records=[{'path':p.name,'seconds':(int(p.stem.split('-')[1])-1)/2,'kind':'2fps'} for p in sorted(folder.glob('sample-*.png'))]
at=0
for b in sheet['beats']:
    d=b['actual_duration_s']
    for label,relative in [('start',0),('mid',d/2),('end',max(0,d-1/24))]:
        out=folder/f"{b['beat_id']}-{label}.png";t=at+relative
        subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{t:.6f}','-i',str(source),'-frames:v','1',str(out)],check=True)
        records.append({'path':out.name,'seconds':t,'kind':label,'beat':b['beat_id']})
    at+=d
unique={};representatives=[]
font=ImageFont.truetype('/Users/bear/Library/Fonts/EBGaramond-Regular.ttf',24)
for item in sorted(records,key=lambda r:r['seconds']):
    p=folder/item['path'];im=Image.open(p).convert('RGB');assert im.size==(3840,2160)
    digest=hashlib.sha256(im.tobytes()).hexdigest();item['pixel_sha256']=digest
    if digest not in unique:
        unique[digest]=item['path'];representatives.append(item)
    item['review_representative']=unique[digest]
for start in range(0,len(representatives),24):
    page=Image.new('RGB',(2400,2160),'#FAF9F5');draw=ImageDraw.Draw(page)
    for i,item in enumerate(representatives[start:start+24]):
        im=Image.open(folder/item['path']).convert('RGB');im.thumbnail((590,332));x=i%4*600+5;y=i//4*360+28
        page.paste(im,(x,y));draw.text((x,y-26),f"{item['seconds']:.2f}s · {item['path']}",font=font,fill='#3D3929')
    page.save(folder/f'page-{start//24+1:03}.jpg',quality=95)
(folder/'manifest.json').write_text(json.dumps({'source':str(source),'samples':len(records),'unique_pixel_frames':len(representatives),'records':records},indent=2)+'\n')
print(json.dumps({'samples':len(records),'unique_pixel_frames':len(representatives),'pages':(len(representatives)+23)//24,'folder':str(folder)}),flush=True)

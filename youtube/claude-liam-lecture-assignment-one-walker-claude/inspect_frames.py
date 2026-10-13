import sys, subprocess, json, hashlib
from pathlib import Path
from PIL import Image, ImageDraw
R=Path(__file__).resolve().parent
mode=sys.argv[1]
out=R/'_qc'/mode
out.mkdir(parents=True,exist_ok=True)
if mode=='preflight':
    files=sorted((R/'_qc/preflight').glob('*-*.png'))
else:
    master=Path(sys.argv[2]); frames=out/'frames';frames.mkdir(exist_ok=True)
    subprocess.run(['ffmpeg','-v','error','-i',str(master),'-vf','fps=2,scale=640:360','-q:v','3',str(frames/'%05d.jpg')],check=True)
    raw=sorted(frames.glob('*.jpg')); files=[]; seen={}; mapping=[]
    for p in raw:
        digest=hashlib.sha256(p.read_bytes()).hexdigest()
        if digest not in seen:
            seen[digest]=p.name; files.append(p)
        mapping.append({'sample':p.name,'same_pixels_as':seen[digest],'sha256':digest})
    (out/'sample-map.json').write_text(json.dumps({'sample_fps':2,'raw_sample_count':len(raw),'unique_sample_count':len(files),'samples':mapping},indent=2)+'\n')
    sheet=json.loads((R/'beat_sheet.json').read_text()); t=0
    for b in sheet['beats']:
        d=b['actual_duration_s']
        for f in [.15,.5,.85]:
            p=out/f"{b['beat_id']}-{int(f*100)}.png"
            subprocess.run(['ffmpeg','-v','error','-ss',str(t+d*f),'-i',str(master),'-frames:v','1','-vf','scale=960:540',str(p)],check=True)
        t+=d
    files+=sorted(out.glob('B*.png'))
cols=3 if mode=='preflight' else 4
width=640; height=360; per=cols*4
for start in range(0,len(files),per):
    canvas=Image.new('RGB',(cols*width,4*(height+28)),(255,255,255));draw=ImageDraw.Draw(canvas)
    for i,p in enumerate(files[start:start+per]):
        im=Image.open(p).convert('RGB');im.thumbnail((width,height))
        x=(i%cols)*width;y=(i//cols)*(height+28)
        canvas.paste(im,(x,y+28));draw.text((x+8,y+6),p.name,fill='black')
    canvas.save(out/f'contact-{start//per+1:03}.jpg',quality=92)
print(len(files),'frames;', (len(files)+per-1)//per,'contact pages',out)

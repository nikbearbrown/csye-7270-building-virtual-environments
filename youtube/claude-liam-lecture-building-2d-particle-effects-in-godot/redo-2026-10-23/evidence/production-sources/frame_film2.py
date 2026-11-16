from pathlib import Path
import subprocess,json,sys
from PIL import Image,ImageDraw,ImageFont
r=Path(sys.argv[1]);cap=r/'captures';rows=json.loads((cap/'timeline.json').read_text());(r/'media').mkdir(exist_ok=True)
im=Image.new('RGB',(1920,1080),'#faf9f5');d=ImageDraw.Draw(im);font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',28)
d.text((96,62),'Scripted actions · Real Godot · Synchronized crops',font=font,fill='#3d3929');d.text((96,132),'Viewport',font=font,fill='#3d3929')
plate=cap/'native-panel-plate.png';im.save(plate)
retake=r/'capture-retake-bursts/captures'
overrides={row['beat_id']:row for row in json.loads((retake/'timeline.json').read_text())} if (retake/'timeline.json').exists() else {}
receipts=[]
for row in rows:
 source=cap/'native-editor-take-01.mov'
 if row['beat_id'] in overrides:row=overrides[row['beat_id']];source=retake/'native-editor-take-01.mov'

 bid=row['beat_id'];out=r/'media'/f'{bid}.mp4'
 if out.exists():continue
 if bid in ['B01','B02','B18','B23']:
  filt='crop=3456:2070:68:68,scale=1624:972,pad=1920:1080:148:54:color=0xfaf9f5,fps=30'
  args=['-vf',filt]
 elif bid=='B17':
  filt='crop=1800:1000:990:830,scale=1728:960,pad=1920:1080:96:60:color=0xfaf9f5,fps=30';args=['-vf',filt]
 elif bid in ['B19','B20','B21','B22']:
  filt='crop=2304:1296:642:523,scale=1728:972,pad=1920:1080:96:54:color=0xfaf9f5,fps=30';args=['-vf',filt]
 else:
  filt='[0:v]split=2[v][i];[v]crop=2160:1530:700:370,scale=1188:842,fps=30[vv];[i]crop=585:1150:2940:295,scale=468:920,fps=30[ii];[1:v][vv]overlay=96:180[a];[a][ii]overlay=1356:96,format=yuv420p[out]'
  args=['-loop','1','-i',str(plate),'-filter_complex',filt,'-map','[out]']
 subprocess.run(['ffmpeg','-v','error','-ss',str(row['start_s']),'-i',str(source),*args,'-t',str(row['duration_s']),'-an','-c:v','libx264','-preset','fast','-crf','16','-y',str(out)],check=True)
 receipts.append({'beat':bid,'source_start_s':row['start_s'],'duration_s':row['duration_s'],'filter':filt,'source':str(source)});print(bid,'framed',flush=True)
 (cap/'framing.json').write_text(json.dumps(receipts,indent=2))
# Signoff remains moving native trail footage, at original speed.
sheet=json.loads((r/'beat_sheet.json').read_text());dur=next(b['actual_duration_s'] for b in sheet['beats'] if b['beat_id']=='BSIGN')
subprocess.run(['ffmpeg','-v','error','-ss','3','-i',str(r/'media/B30.mp4'),'-t',str(dur),'-an','-c:v','libx264','-preset','fast','-crf','16','-y',str(r/'media/BSIGN.mp4')],check=True)

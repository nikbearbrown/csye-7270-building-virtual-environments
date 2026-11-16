from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw,ImageFont
r=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-what-is-a-particle-system/redo-2026-10-23');cap=r/'captures';rows=json.loads((cap/'timeline.json').read_text())
im=Image.new('RGB',(1920,1080),'#faf9f5');d=ImageDraw.Draw(im);font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',28);large=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',32)
d.text((96,62),'Scripted actions · Real Godot · Synchronized crops',font=font,fill='#3d3929');d.text((96,145),'Viewport',font=large,fill='#3d3929')
plate=cap/'native-panel-plate.png';im.save(plate)
for row in rows:
 bid=row['beat_id']
 if bid in ['B01','B02','B03','B07','B12','B24']:continue
 filt='[0:v]split=2[v][i];[v]crop=2160:1440:685:425,scale=1188:792,fps=30[vv];[i]crop=585:1125:2940:295,scale=468:900,fps=30[ii];[1:v][vv]overlay=96:200[a];[a][ii]overlay=1356:96,format=yuv420p[out]'
 subprocess.run(['ffmpeg','-v','error','-ss',str(row['start_s']),'-i',str(cap/'native-editor-take-01.mov'),'-loop','1','-i',str(plate),'-filter_complex',filt,'-map','[out]','-t',str(row['duration_s']),'-an','-c:v','libx264','-preset','fast','-crf','16','-y',str(r/'media'/f'{bid}.mp4')],check=True)
 print(bid,'readable synchronized native crops',flush=True)
(cap/'native-panel-edit.json').write_text(json.dumps({'source':'native-editor-take-01.mov','viewport_crop':[685,425,2160,1440],'inspector_crop':[2940,295,585,1125],'method':'Same source frames shown at the same timestamp; original speed. No redrawn editor content.'},indent=2))

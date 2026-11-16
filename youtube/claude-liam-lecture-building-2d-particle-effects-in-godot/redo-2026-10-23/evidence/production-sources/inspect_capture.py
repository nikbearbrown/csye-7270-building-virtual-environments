from pathlib import Path
import sys,json,subprocess
from PIL import Image,ImageDraw,ImageFont
r=Path(sys.argv[1]);out=r/'evidence/capture-inspection';out.mkdir(exist_ok=True,parents=True);rows=json.loads((r/'captures/timeline.json').read_text());font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',20)
tiles=[]
for row in rows:
 for offset in ([float(x) for x in sys.argv[2].split(",")] if len(sys.argv)>2 else [1.5,5.5,9.5]):
  offset=min(offset,row['duration_s']-.5);p=out/f"{row['beat_id']}-{offset:.1f}.jpg"
  subprocess.run(['ffmpeg','-v','error','-ss',str(row['start_s']+offset),'-i',str(r/'captures/native-editor-take-01.mov'),'-frames:v','1','-vf','scale=720:-1','-y',str(p)],check=True)
  im=Image.new('RGB',(730,470),'#faf9f5');im.paste(Image.open(p),(5,35));ImageDraw.Draw(im).text((10,6),f"{row['beat_id']} +{offset:.1f}s",font=font,fill='black');tiles.append(im)
for j in range(0,len(tiles),9):
 page=Image.new('RGB',(2190,1410),'white')
 for k,t in enumerate(tiles[j:j+9]):page.paste(t,((k%3)*730,(k//3)*470))
 page.save(out/f'contact-{j//9+1:02}.jpg')
print(out)

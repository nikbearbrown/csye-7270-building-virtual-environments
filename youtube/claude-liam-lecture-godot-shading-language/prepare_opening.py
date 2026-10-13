#!/usr/bin/env python3
from pathlib import Path
import json,shutil,subprocess,sys,datetime
R=Path(__file__).resolve().parent
s=json.loads((R/'beat_sheet.json').read_text()); b=s['beats'][0]
assert b['beat_id']=='BOPEN' and b.get('audio_file') and b.get('actual_duration_s',0)>0
build=R.parents[2]/'brutalist.art/skills/make/lecture/templates/title-slide-16x9/build.py'
# Keep earlier generated clips recoverable if this opening is rebuilt.
old=list((R/'opening').glob('*.mp4'))
if old:
 archive=R/'_superseded'/('opening-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'));archive.mkdir(parents=True,exist_ok=True)
 for p in old:shutil.move(str(p),archive/p.name)
subprocess.run([sys.executable,str(build),'--out',str(R/'opening'),'--sheet',str(R/'beat_sheet.json'),'--width','3840'],check=True)
clips=list((R/'opening').glob('example-opening-*.mp4'))
assert len(clips)==1,clips
shutil.copy2(clips[0],R/'media/BOPEN.mp4')
print('Prepared BOPEN visual for',b['actual_duration_s'],'seconds; narration muxed by the normal compiler.')

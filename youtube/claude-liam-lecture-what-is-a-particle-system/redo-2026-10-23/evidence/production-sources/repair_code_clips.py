from pathlib import Path
import subprocess,json,shutil,argparse
ap=argparse.ArgumentParser();ap.add_argument('--only');args=ap.parse_args()
r=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-what-is-a-particle-system/redo-2026-10-23');cap=r/'captures';timeline={b['beat_id']:b for b in json.loads((cap/'timeline.json').read_text())};backup=cap/'original-code-clips';backup.mkdir(exist_ok=True)
fixes={'B03':[(0,.3,None),(.3,6.3,(.4,300)),(6.3,None,None)],'B07':[(0,.3,None),(.3,6.3,(7.4,450)),(6.3,None,None)],'B12':[(0,4.3,None),(4.3,8.3,(7.4,450)),(8.3,None,None)],'B24':[(0,.3,None),(.3,5.3,(14.4,200)),(5.3,None,None)]}
for bid,segs in fixes.items():
 if args.only and bid!=args.only:continue
 row=timeline[bid];out=r/'media'/f'{bid}.mp4'
 if not (backup/out.name).exists():shutil.copy2(out,backup/out.name)
 filters=[];labels=[]
 for i,(a,b,source) in enumerate(segs):
  end=row['duration_s'] if b is None else b;length=end-a
  if source:
   start,y=source;inp=0;crop=f'crop=1800:1000:1050:{y},scale=1728:960,pad=1920:1080:96:60:color=0xfaf9f5'
  else:
   start=row['start_s']+a;inp=1;crop='crop=3456:2070:68:68,scale=1624:972,pad=1920:1080:148:54:color=0xfaf9f5'
  filters.append(f'[{inp}:v]trim=start={start}:duration={length},setpts=PTS-STARTPTS,{crop},fps=30,settb=AVTB[v{i}]');labels.append(f'[v{i}]')
 filters.append(''.join(labels)+f'concat=n={len(segs)}:v=1:a=0[v]')
 subprocess.run(['ffmpeg','-v','error','-i',str(cap/'code-inserts-native-v2.mov'),'-i',str(cap/'native-editor-take-01.mov'),'-filter_complex',';'.join(filters),'-map','[v]','-t',str(row['duration_s']),'-an','-c:v','libx264','-preset','fast','-crf','16','-y',str(out)],check=True)
 print(bid,'native close-up repaired',flush=True)
(cap/'code-insert-edit.json').write_text(json.dumps({'source':'code-inserts-native-v2.mov','source_revision':'multiline dictionary formatting only; equations unchanged','edits':fixes,'timing':'Straight cuts, original motion speed; source views are recorded later in the same actual editor.'},indent=2))

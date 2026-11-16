from pathlib import Path
import subprocess,json,shutil,sys
r=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-what-is-a-particle-system/redo-2026-10-23');s=json.loads((r/'beat_sheet.json').read_text());dur={b['beat_id']:b['actual_duration_s'] for b in s['beats']};backup=r/'preserved-candidates'
for b in ['B21','B24']:
 dst=backup/f'before-final-inspection-{b}.mp4'
 if not dst.exists():shutil.copy2(r/'media'/f'{b}.mp4',dst)
v=r/(s['metadata']['slug']+'-slate.mp4');dst=backup/'before-final-inspection-slate.mp4'
if not dst.exists():shutil.copy2(v,dst)
if (r/'evidence/final-qc').exists() and not (r/'evidence/pre-repair-qc').exists():shutil.move(r/'evidence/final-qc',r/'evidence/pre-repair-qc')
fil='[0:v]split[v][i];[v]crop=2160:1440:685:425,scale=1188:792[view];[i]crop=585:1125:2940:295,scale=468:900[inspect];[1:v][view]overlay=96:200:shortest=1[p];[p][inspect]overlay=1356:96:shortest=1,fps=30[out]'
if '--only-b24' not in sys.argv:subprocess.run(['ffmpeg','-v','error','-i',str(r/'captures/builtin-burst-repair-native.mov'),'-loop','1','-i',str(r/'captures/native-panel-plate.png'),'-filter_complex',fil,'-map','[out]','-t',str(dur['B21']),'-an','-c:v','libx264','-preset','fast','-crf','16','-y',str(r/'media/B21.mp4')],check=True)
fil=f'[0:v]trim=duration=5.3,setpts=PTS-STARTPTS,fps=30,settb=AVTB[a];[1:v]trim=start=0.3:duration={dur["B24"]-5.3},setpts=PTS-STARTPTS,fps=30,settb=AVTB[b];[a][b]concat=n=2:v=1:a=0[out]'
subprocess.run(['ffmpeg','-v','error','-i',str(backup/'before-final-inspection-B24.mp4'),'-i',str(r/'media/B23.mp4'),'-filter_complex',fil,'-map','[out]','-t',str(dur['B24']),'-an','-c:v','libx264','-preset','fast','-crf','16','-y',str(r/'media/B24.mp4')],check=True)
for bid,times in [('B21',[1.3,2,3.6,5.4,6,10]),('B24',[2,7,13])]:
 for t in times:subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(r/'media'/f'{bid}.mp4'),'-frames:v','1','-threads','1','-y',str(Path('qc-resume')/f'fixed-{bid}-{t}.jpg')],check=True)
(r/'captures/final-repairs.json').write_text(json.dumps({'B21':'Retaken in real editor with preprocess zero; one-shot, explosiveness and restart actions preserved in builtin-burst-repair-actions.json','B24':'First 5.3 seconds retain native code insert. Remaining 9.68 seconds use original-speed B23 control/result footage starting at .3 seconds. Earlier window capture had gone black. No reconstruction or frozen replacement.'},indent=2))
print('Two affected segments repaired; all other slots preserved')

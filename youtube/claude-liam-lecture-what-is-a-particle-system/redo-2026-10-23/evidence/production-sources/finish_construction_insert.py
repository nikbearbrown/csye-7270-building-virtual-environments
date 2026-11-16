from pathlib import Path
import subprocess,json
r=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-what-is-a-particle-system/redo-2026-10-23')
b=next(b for b in json.loads((r/'beat_sheet.json').read_text())['beats'] if b['beat_id']=='BMAKE');d=b['actual_duration_s'];raw=r/'captures/tool-construction-native.mov'
filters='[0:v]split=3[a][b][c];[a]trim=duration=7,setpts=PTS-STARTPTS,crop=3456:2070:68:68,scale=1624:972,pad=1920:1080:148:54:color=0xfaf9f5,fps=30,settb=AVTB[whole];[b]trim=start=7,setpts=PTS-STARTPTS,crop=2160:1440:685:425,scale=1188:792[view];[c]trim=start=7,setpts=PTS-STARTPTS,crop=585:1125:2940:295,scale=468:900[inspector];[1:v][view]overlay=96:200:shortest=1[panel];[panel][inspector]overlay=1356:96:shortest=1,fps=30,settb=AVTB[detail];[whole][detail]concat=n=2:v=1:a=0[out]'
subprocess.run(['ffmpeg','-v','error','-i',str(raw),'-loop','1','-i',str(r/'captures/native-panel-plate.png'),'-filter_complex',filters,'-map','[out]','-t',str(d),'-an','-c:v','libx264','-preset','fast','-crf','16','-y',str(r/'media/BMAKE.mp4')],check=True)
for t in [2,5,9,13]:subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(r/'media/BMAKE.mp4'),'-frames:v','1','-threads','1','-y',str(Path('qc-resume')/f'BMAKE-{t}.jpg')],check=True)
print('Construction insert slotted',d)

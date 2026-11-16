from pathlib import Path
import subprocess,json
r=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-what-is-a-particle-system/redo-2026-10-23');s=json.loads((r/'beat_sheet.json').read_text());b={x['beat_id']:x for x in s['beats']}
subprocess.run(['ffmpeg','-v','error','-loop','1','-i',str(r/'captures/nature-of-code-source.png'),'-t',str(b['BREF']['actual_duration_s']),'-vf','scale=1728:972,pad=1920:1080:96:54:color=0xfaf9f5,fps=30','-an','-c:v','libx264','-preset','fast','-crf','16','-y',str(r/'media/BREF.mp4')],check=True)
filt='[0:v]split=2[v][i];[v]crop=2160:1440:685:425,scale=1188:792,fps=30[vv];[i]crop=585:1125:2940:295,scale=468:900,fps=30[ii];[1:v][vv]overlay=96:200[a];[a][ii]overlay=1356:96,format=yuv420p[out]'
subprocess.run(['ffmpeg','-v','error','-i',str(r/'captures/one-particle-native.mov'),'-loop','1','-i',str(r/'captures/native-panel-plate.png'),'-filter_complex',filt,'-map','[out]','-t',str(b['BONE']['actual_duration_s']),'-an','-c:v','libx264','-preset','fast','-crf','16','-y',str(r/'media/BONE.mp4')],check=True)
print('supplements slotted')

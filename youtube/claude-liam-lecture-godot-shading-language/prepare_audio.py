#!/usr/bin/env python3
"""After Kokoro: add declared pauses once, then measure every audio file."""
from pathlib import Path
import json,subprocess,hashlib
R=Path(__file__).resolve().parent
sheet=json.loads((R/'beat_sheet.json').read_text())
statepath=R/'mp3/pause-state.json';state=json.loads(statepath.read_text()) if statepath.exists() else {}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for b in sheet['beats']:
 p=R/b['audio_file'];lead=b.get('lead_silence_s',0);tail=b.get('tail_silence_s',0)
 signature={'lead':lead,'tail':tail}
 prior=state.get(b['beat_id'],{})
 if (lead or tail) and (prior.get('sha256')!=digest(p) or prior.get('pauses')!=signature):
  raw=R/'mp3'/f"raw-{b['beat_id']}.mp3"
  raw.write_bytes(p.read_bytes())
  tmp=p.with_suffix('.padded.mp3')
  filt=f'adelay={round(lead*1000)}:all=1,apad=pad_dur={tail}'
  subprocess.run(['ffmpeg','-y','-v','error','-i',str(raw),'-af',filt,'-codec:a','libmp3lame','-q:a','2',str(tmp)],check=True)
  tmp.replace(p)
 state[b['beat_id']]={'sha256':digest(p),'pauses':signature}
 result=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(p)],check=True,text=True,capture_output=True)
 b['actual_duration_s']=float(result.stdout.strip())
(R/'beat_sheet.json').write_text(json.dumps(sheet,indent=2)+'\n')
statepath.write_text(json.dumps(state,indent=2)+'\n')
print('Measured',len(sheet['beats']),'audio files; declared pauses applied.')

#!/usr/bin/env python3
"""After Kokoro: add declared pauses once (BIDEA lead 0.8 s, BVDT lead 0.5 s, BOUT tail 1.0 s: the toolkit generator and compiler do not honour lead_silence_s / tail_silence_s), then measure every audio file and write
the measured durations back to beat_sheet.json. Idempotent (keyed on the file hash). Copied from the sibling film claude-liam-lecture-godot-shading-language/prepare_audio.py.
Run after EVERY (re)generation: python3 prepare_audio.py ; then python3 make_sheet.py (refills the Remotion durations)."""
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

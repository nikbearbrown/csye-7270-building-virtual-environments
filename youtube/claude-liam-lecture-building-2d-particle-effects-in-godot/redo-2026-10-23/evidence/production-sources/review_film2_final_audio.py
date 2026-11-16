from pathlib import Path
import json,subprocess,whisper,torch
r=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-building-2d-particle-effects-in-godot/redo-2026-10-23');out=r/'evidence/final-qc';v=json.loads((out/'validation.json').read_text());torch.set_num_threads(4);m=whisper.load_model(str(Path.home()/'.cache/whisper/small.en.pt'),device='cpu');rows=[]
for row in v['beat_timeline']:
 if row['beat'] not in ['BDEFS','B10','B20','BSIGN','BOUT']:continue
 p=out/(row['beat']+'-final-audio.wav');subprocess.run(['ffmpeg','-v','error','-ss',str(row['start']),'-i',v['video'],'-t',str(row['duration']),'-vn','-ar','16000','-ac','1','-y',str(p)],check=True)
 text=m.transcribe(str(p),fp16=False,language='en',verbose=None)['text'];rows.append(dict(beat=row['beat'],expected=row['narration'],recognized=text));print(row['beat'],text,flush=True)
(out/'flagged-final-audio-review.json').write_text(json.dumps(rows,indent=2))

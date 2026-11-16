from pathlib import Path
import json,subprocess,numpy as np,torch,whisper
W=Path(__file__).resolve().parent;ROOT=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube')
cache=Path.home()/'.cache/whisper/small.en.pt';assert cache.is_file();torch.set_num_threads(4);model=whisper.load_model(str(cache),device='cpu')
for p in sorted(ROOT.glob('*/redo-2026-10-23/evidence/pre-capture-audio/results.json')):
 q=json.loads(p.read_text());R=p.parents[2];s=json.loads((R/'beat_sheet.json').read_text());rows=[]
 selected=set(q['flags'])|{'BIDEA','BHTF','BSIGN','BOUT'}
 for b in s['beats']:
  if b['beat_id'] not in selected:continue
  data=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(R/b['audio_file']),'-f','f32le','-ac','1','-ar','16000','-']),dtype=np.float32)
  # Remove only leading/trailing near silence for independent recognition; delivered track is unchanged.
  active=np.flatnonzero(np.abs(data)>.006)
  if len(active):data=data[max(0,active[0]-1600):min(len(data),active[-1]+1600)]
  v=model.transcribe(data,fp16=False,language='en',verbose=None,condition_on_previous_text=False)
  row=dict(beat=b['beat_id'],expected=b['narration_text'],recognized=v['text']);rows.append(row);print(q['film'],row,flush=True)
 (p.parent/'larger-model-review.json').write_text(json.dumps(dict(film=q['film'],model='cached local Whisper small.en',trim='Analysis only: leading/trailing near-silence trimmed; original tracks unchanged',rows=rows,limits='Automatic cross-check, not human listening'),indent=2))

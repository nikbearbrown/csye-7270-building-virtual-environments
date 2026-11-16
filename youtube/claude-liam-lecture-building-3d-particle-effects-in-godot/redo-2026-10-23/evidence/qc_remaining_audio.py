from pathlib import Path
import json,sys,subprocess,hashlib,datetime,difflib,re
import numpy as np
import whisper,torch
W=Path(__file__).resolve().parent;ROOT=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube')
slugs={3:'claude-liam-lecture-building-3d-particle-effects-in-godot',4:'claude-liam-lecture-a-practical-godot-vfx-library',5:'claude-liam-lecture-adding-particle-effects-to-walker-claude'}
cache=Path.home()/'.cache/whisper';assert (cache/'base.en.pt').is_file(),'No downloads allowed'
torch.set_num_threads(4);model=whisper.load_model(str(cache/'base.en.pt'),device='cpu')
def words(x):return re.findall(r"[a-z0-9']+",x.lower())
for spec in sys.argv[1:]:
 n=int(spec.split(":")[0]);selected=set(spec.split(":")[1].split(",")) if ":" in spec else None
 R=ROOT/slugs[n]/'redo-2026-10-23';s=json.loads((R/'beat_sheet.json').read_text());rows=[]
 out=R/'evidence/pre-capture-audio';out.mkdir(exist_ok=True)
 previous={x['beat']:x for x in json.loads((out/'results.json').read_text())['rows']} if selected else {}
 for b in s['beats']:
  p=R/b['audio_file']
  if selected and b['beat_id'] not in selected:
   row=previous[b['beat_id']];assert row['source_sha256']==hashlib.sha256(p.read_bytes()).hexdigest();rows.append(row);continue
  data=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-f','f32le','-ac','1','-ar','16000','-']),dtype=np.float32).copy()
  v=model.transcribe(data,fp16=False,language='en',verbose=None)
  similarity=difflib.SequenceMatcher(a=words(b['narration_text']),b=words(v['text']),autojunk=False).ratio()
  peak=float(np.max(np.abs(data)));row=dict(beat=b['beat_id'],expected=b['narration_text'],recognized=v['text'],word_similarity=similarity,samples=len(data),peak_dbfs=float(20*np.log10(max(peak,1e-12))),clipped_samples=int(np.sum(np.abs(data)>=1)),source_sha256=hashlib.sha256(p.read_bytes()).hexdigest())
  rows.append(row);print(n,b['beat_id'],round(similarity,3),row['peak_dbfs'],flush=True)
 result=dict(created=datetime.datetime.now(datetime.timezone.utc).isoformat(),film=n,model='cached local Whisper base.en',rows=rows,flags=[x['beat'] for x in rows if x['word_similarity']<.88 or x['clipped_samples']],limits='Source narration analysis only, before native footage and assembly. ASR is not human listening or full-film AV QC.')
 (out/'results.json').write_text(json.dumps(result,indent=2));print('FILM',n,'flags',result['flags'],flush=True)

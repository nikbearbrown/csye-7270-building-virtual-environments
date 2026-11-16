from pathlib import Path
import whisper,torch,json
r=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-building-2d-particle-effects-in-godot/redo-2026-10-23');torch.set_num_threads(4)
p=Path.home()/'.cache/whisper/small.en.pt';assert p.exists();m=whisper.load_model(str(p),device='cpu');rows=[]
s=json.loads((r/'beat_sheet.json').read_text())
for bid in ['BDEFS','B03','B08','B10','B24','B27','B30','BSIGN','BOUT']:
 b=next(b for b in s['beats'] if b['beat_id']==bid);v=m.transcribe(str(r/b['audio_file']),fp16=False,language='en',verbose=None)
 rows.append(dict(beat=bid,expected=b['narration_text'],recognized=v['text']));print(bid,v['text'],flush=True)
(r/'evidence/narration-flag-review.json').write_text(json.dumps(rows,indent=2))

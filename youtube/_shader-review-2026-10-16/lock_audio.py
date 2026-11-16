#!/usr/bin/env python3
"""After TTS, add real silence and synchronize scene clocks; preserve unpadded audio."""
from pathlib import Path
import json,sys,subprocess,hashlib,shutil
reel=Path(sys.argv[1]).resolve();sheetpath=reel/'beat_sheet.json'
sheet=json.loads(sheetpath.read_text());cache=reel/'audio-originals';cache.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def duration(p):return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)],text=True))
for b in sheet['beats']:
 src=reel/b['audio_file'];tag=cache/(b['beat_id']+'.json')
 record=json.loads(tag.read_text()) if tag.exists() else {}
 if record.get('padded_sha256')==sha(src):
  b['actual_duration_s']=duration(src)
 else:
  original=cache/(b['beat_id']+'-'+sha(src)[:12]+src.suffix)
  if not original.exists():shutil.copy2(src,original)
  spoken=duration(original);lead=float(b.get('lead_silence_s',0));tail=float(b.get('tail_silence_s',0));minimum=float(b.get('minimum_duration_s',0))
  if b['beat_id']=='B05' and spoken>16:raise SystemExit('B05 exceeds the 16-second capture; extend its capture before locking this beat.')
  target=max(spoken+lead+tail,minimum)
  if target>spoken or lead:
   out=src.with_name(src.stem+'-padded.wav')
   subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i',str(original),'-af',f'adelay={round(lead*1000)}:all=1,apad','-t',str(target),'-c:a','pcm_s16le',str(out)],check=True)
   b['audio_file']=str(out.relative_to(reel));src=out
  b['actual_duration_s']=duration(src)
  tag.write_text(json.dumps({'original':str(original),'padded_sha256':sha(src),'seconds':b['actual_duration_s']},indent=2)+'\n')
 if 'remotion' in b['shot']:b['shot']['remotion']['props']['durationSeconds']=b['actual_duration_s']
sheetpath.write_text(json.dumps(sheet,indent=2,ensure_ascii=False)+'\n')
print('Measured timeline seconds:',sum(b['actual_duration_s'] for b in sheet['beats']))

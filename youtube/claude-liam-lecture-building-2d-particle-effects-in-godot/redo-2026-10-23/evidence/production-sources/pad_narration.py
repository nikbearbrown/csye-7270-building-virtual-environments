from pathlib import Path
import json,sys,subprocess,shutil
r=Path(sys.argv[1]);p=r/'beat_sheet.json';s=json.loads(p.read_text())
raw=r/'mp3'/'unpadded';raw.mkdir(exist_ok=True)
for b in s['beats']:
 lead=b.get('lead_silence_s',0);tail=b.get('tail_silence_s',0)
 if (lead or tail) and not b.get('padding_applied'):
  audio=r/b['audio_file'];source=raw/audio.name
  shutil.copy2(audio,source)
  filters=[]
  if lead:filters.append(f'adelay={round(lead*1000)}:all=1')
  if tail:filters.append(f'apad=pad_dur={tail}')
  subprocess.run(['ffmpeg','-v','error','-i',str(source),'-af',','.join(filters),'-c:a','libmp3lame','-b:a','128k','-y',str(audio)],check=True)
  b['speech_duration_s']=b['actual_duration_s']
  b['actual_duration_s']=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(audio)]))
  b['padding_applied']=True
 rem=b.get('shot',{}).get('remotion')
 if rem:rem['props']['durationSeconds']=b['actual_duration_s']
p.write_text(json.dumps(s,indent=2))
print('Measured total',sum(b['actual_duration_s'] for b in s['beats']))

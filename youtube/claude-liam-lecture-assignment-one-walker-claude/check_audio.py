"""Independent audio measurements and local ASR; no narration edits."""
from pathlib import Path
import json, subprocess, hashlib, sys
from faster_whisper import WhisperModel
R=Path(__file__).resolve().parent
S=json.loads((R/'beat_sheet.json').read_text())
Q=R/'_qc/audio';Q.mkdir(parents=True,exist_ok=True)
if len(sys.argv)>1 and sys.argv[1]=='revised':
    model=WhisperModel('medium.en',device='cpu',compute_type='int8',local_files_only=True,cpu_threads=4)
    previous=Q/'revised-transcript.json'
    rows=json.loads(previous.read_text()) if previous.exists() else {}
    for bid in (sys.argv[2:] or ['BOPEN','B03']):
        b=next(b for b in S['beats'] if b['beat_id']==bid)
        segs,_=model.transcribe(str(R/b['audio_file']),beam_size=5,language='en',vad_filter=False)
        rows[bid]={'audio_sha256':hashlib.sha256((R/b['audio_file']).read_bytes()).hexdigest(),'segments':[{'start':s.start,'end':s.end,'text':s.text} for s in segs]}
    (Q/'revised-transcript.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(json.dumps(rows,indent=2))
    raise SystemExit(0)
lst=Q/'inputs.txt'
lst.write_text('\n'.join("file '"+str(R/b['audio_file'])+"'" for b in S['beats'])+'\n')
wav=Q/'timeline.wav'
subprocess.run(['ffmpeg','-v','error','-n','-f','concat','-safe','0','-i',str(lst),'-c:a','pcm_s16le',str(wav)],check=True)
log=subprocess.run(['ffmpeg','-hide_banner','-i',str(wav),'-af','loudnorm=print_format=json','-f','null','-'],capture_output=True,text=True,check=True).stderr
(Q/'loudness.txt').write_text(log)
model=WhisperModel('medium.en',device='cpu',compute_type='int8',local_files_only=True,cpu_threads=4)
segments,info=model.transcribe(str(wav),beam_size=5,language='en',vad_filter=False)
rows=[{'start':s.start,'end':s.end,'text':s.text} for s in segments]
(Q/'transcript.json').write_text(json.dumps(rows,indent=2)+'\n')
(Q/'transcript.txt').write_text('\n'.join(f"{s['start']:.2f}–{s['end']:.2f}: {s['text']}" for s in rows)+'\n')
dictionary=R.parents[2]/'brutalist.art/runtime/pronunciation/liam.json'
(Q/'dictionary.json').write_text(json.dumps({'path':str(dictionary),'sha256':hashlib.sha256(dictionary.read_bytes()).hexdigest()},indent=2)+'\n')
print('Audio timeline measured and independently transcribed:',wav)

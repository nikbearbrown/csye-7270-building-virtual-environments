from pathlib import Path
import sys,json,subprocess,math,hashlib,datetime,re
import numpy as np
from PIL import Image,ImageDraw
r=Path(sys.argv[1]).resolve();s=json.loads((r/'beat_sheet.json').read_text());out=r/'evidence/final-qc';out.mkdir(parents=True,exist_ok=True)
p=r/(s['metadata']['slug']+'-slate.mp4')
def run(args):return subprocess.run(args,capture_output=True,text=True,check=True)
probe=json.loads(run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(p)]).stdout)
(out/'ffprobe.json').write_text(json.dumps(probe,indent=2))
v=next(x for x in probe['streams'] if x['codec_type']=='video');a=next(x for x in probe['streams'] if x['codec_type']=='audio')
assert (v['width'],v['height'])==(1920,1080)
run(['ffmpeg','-v','error','-threads','2','-i',str(p),'-f','null','-'])
print('Full decode passed',flush=True)
wav=out/'narration-16k.wav';run(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','16000','-y',str(wav)])
import soundfile as sf
signal,sr=sf.read(wav);peak=float(np.max(np.abs(signal)));rms=float(np.sqrt(np.mean(signal**2)));assert rms>.001
audio=dict(peak=peak,rms=rms,peak_dbfs=float(20*np.log10(max(peak,1e-10))),clipped_samples=int(np.sum(np.abs(signal)>=.9999)),samples=len(signal),sample_rate=sr)
silence=run(['ffmpeg','-hide_banner','-i',str(wav),'-af','silencedetect=noise=-40dB:d=1.8','-f','null','-']).stderr
(out/'silence-detection.txt').write_text(silence)
rows=[];clock=0
for b in s['beats']:
 dur=math.ceil(float(b['actual_duration_s'])*30)/30
 rows.append(dict(beat=b['beat_id'],start=clock,duration=dur,narration=b['narration_text']));clock+=dur
samples=[]
for row in rows:
 for fraction in [.15,.5,.9]:
  t=row['start']+fraction*row['duration'];dest=out/f'{row["beat"]}-{fraction}.jpg'
  run(['ffmpeg','-v','error','-ss',str(t),'-i',str(p),'-frames:v','1','-vf','scale=640:-1','-threads','1','-y',str(dest)])
  samples.append((dest,f'{row["beat"]} · {t:.2f}s'))
for page,offset in enumerate(range(0,len(samples),18),1):
 batch=samples[offset:offset+18];canvas=Image.new('RGB',(1920,390*math.ceil(len(batch)/3)),'#e9e5dc');draw=ImageDraw.Draw(canvas)
 for i,(f,label) in enumerate(batch):
  x=i%3*640;y=i//3*390;canvas.paste(Image.open(f),(x,y+25));draw.text((x+10,y+5),label,fill='black')
 canvas.save(out/f'contact-{page}.jpg')
print('Contact sheets written',flush=True)
import torch,whisper
torch.set_num_threads(4)
modelpath=Path.home()/'.cache/whisper/base.en.pt';assert modelpath.exists(),'Local model missing; no download attempted.'
model=whisper.load_model(str(modelpath),device='cpu');transcript=model.transcribe(str(wav),fp16=False,language='en',verbose=False)
(out/'transcription.json').write_text(json.dumps(transcript,indent=2));(out/'transcription.txt').write_text(transcript['text']+'\n')
import difflib
def words(t):return re.findall(r'[a-z0-9]+',t.lower())
expected=' '.join(x['narration'] for x in rows);comparison=difflib.SequenceMatcher(a=words(expected),b=words(transcript['text']),autojunk=False)
diff=[]
for op,i,j,k,l in comparison.get_opcodes():
 if op!='equal':diff.append(dict(kind=op,expected=' '.join(words(expected)[i:j]),recognized=' '.join(words(transcript['text'])[k:l])))
(out/'transcription-differences.json').write_text(json.dumps(diff,indent=2))
report=dict(video=str(p),duration_s=float(probe['format']['duration']),width=v['width'],height=v['height'],video_codec=v['codec_name'],audio_codec=a['codec_name'],full_decode='passed',audio=audio,asr_word_similarity=comparison.ratio(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),generated=datetime.datetime.now(datetime.timezone.utc).isoformat(),visual_review='Contact sheets awaiting assistant inspection',human_listening='Pending; local speech recognition and level checks do not replace human listening',beat_timeline=rows)
(out/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='beat_timeline'},indent=2),flush=True)

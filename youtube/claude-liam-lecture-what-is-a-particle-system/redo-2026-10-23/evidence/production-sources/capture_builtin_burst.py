from pathlib import Path
import subprocess,time,json,math
w=Path(__file__).resolve().parent/'work-1';r=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-what-is-a-particle-system/redo-2026-10-23')
records=[];base=int(time.time());rid=base
def send(**kw):
 global rid
 rid+=1;req={'id':rid,'node':'Fountain',**kw};(w/'.lecture/request.json').write_text(json.dumps(req));deadline=time.monotonic()+4
 while time.monotonic()<deadline:
  for line in reversed((w/'.lecture/actions.jsonl').read_text().splitlines()[-6:]):
   row=json.loads(line)
   if row['request']['id']==rid:
    if 'error' in row['result']:raise RuntimeError(row)
    records.append({'time':time.monotonic(),'receipt':row});return
  time.sleep(.05)
 raise RuntimeError('No action acknowledgement '+str(req))
(w/'.lecture/request.json').write_text(json.dumps({'id':base,'op':'open','path':'res://builtin_fountain.tscn'}))
log=(w/'.lecture/editor-builtin-burst.log').open('w');editor=subprocess.Popen(['/opt/homebrew/bin/godot','--editor','--path',str(w),'--single-window','--audio-driver','Dummy'],stdout=log,stderr=subprocess.STDOUT);capture=None
try:
 deadline=time.monotonic()+20;window=None
 while time.monotonic()<deadline:
  if editor.poll() is not None:raise RuntimeError('Editor exited '+str(editor.returncode))
  windows=json.loads(subprocess.check_output([str(w.parent/'native_ui'),'windows']));window=next((str(x['kCGWindowNumber']) for x in windows if x['kCGWindowOwnerPID']==editor.pid),None)
  if window and str(base) in (w/'.lecture/actions.jsonl').read_text():break
  time.sleep(.3)
 if not window:raise RuntimeError('No native editor window')
 for prop,v in [('position',{'v2':[0,0]}),('preprocess',0),('amount',80),('one_shot',False),('explosiveness',0)]:send(op='set',property=prop,value=v)
 send(op='zoom')
 beat=next(b for b in json.loads((r/'beat_sheet.json').read_text())['beats'] if b['beat_id']=='B21');duration=beat['actual_duration_s']
 raw=r/'captures/builtin-burst-repair-native.mov';assert not raw.exists();capture=subprocess.Popen(['/usr/sbin/screencapture','-v','-V'+str(math.ceil(duration+1)),'-l'+window,str(raw)],stderr=(r/'captures/builtin-burst-repair.stderr').open('w'))
 t0=time.monotonic();time.sleep(.3);send(op='set',property='one_shot',value=True,label='One Shot: one complete cycle');send(op='set',property='explosiveness',value=1,label='Explosiveness one: simultaneous births')
 for t in [1,5,9]:
  time.sleep(max(0,t-(time.monotonic()-t0)));send(op='call',method='restart',label='Replay full burst; preprocess zero')
 capture.wait(timeout=math.ceil(duration+8));assert capture.returncode==0
 (r/'captures/builtin-burst-repair-actions.json').write_text(json.dumps({'capture_start_monotonic':t0,'actions':records,'reason':'Prior continuous scene preprocess=2 advanced the one-shot beyond visibility. Set zero for complete onset-to-death demonstration.'},indent=2));print(raw,flush=True)
finally:
 if capture is not None and capture.poll() is None:capture.send_signal(2);capture.wait(timeout=10)
 if editor.poll() is None:editor.terminate();editor.wait(timeout=10)
 log.close()

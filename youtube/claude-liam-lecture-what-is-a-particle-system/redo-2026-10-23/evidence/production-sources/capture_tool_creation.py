from pathlib import Path
import subprocess,time,json,math
w=Path(__file__).resolve().parent/'work-1';r=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-what-is-a-particle-system/redo-2026-10-23')
records=[];base=int(time.time());rid=base
def send(**kw):
 global rid
 rid+=1;req={'id':rid,**kw};(w/'.lecture/request.json').write_text(json.dumps(req));deadline=time.monotonic()+4
 while time.monotonic()<deadline:
  for line in reversed((w/'.lecture/actions.jsonl').read_text().splitlines()[-6:]):
   row=json.loads(line)
   if row['request']['id']==rid:
    if 'error' in row['result']:raise RuntimeError(row)
    records.append({'time':time.monotonic(),'receipt':row});return
  time.sleep(.05)
 raise RuntimeError('No action acknowledgement '+str(req))
(w/'.lecture/request.json').write_text(json.dumps({'id':base,'op':'open','path':'res://blank_tool.tscn'}))
log=(w/'.lecture/editor-tool-construction.log').open('w')
editor=subprocess.Popen(['/opt/homebrew/bin/godot','--editor','--path',str(w),'--single-window','--audio-driver','Dummy'],stdout=log,stderr=subprocess.STDOUT)
capture=None
try:
 deadline=time.monotonic()+20;window=None
 while time.monotonic()<deadline:
  if editor.poll() is not None:raise RuntimeError('Editor exited '+str(editor.returncode))
  windows=json.loads(subprocess.check_output([str(w.parent/'native_ui'),'windows']))
  window=next((str(x['kCGWindowNumber']) for x in windows if x['kCGWindowOwnerPID']==editor.pid),None)
  if window and str(base) in (w/'.lecture/actions.jsonl').read_text():break
  time.sleep(.3)
 if not window:raise RuntimeError('No native editor window')
 send(op='select',label='Empty Node2D: no teaching script attached');send(op='zoom')
 beat=next(b for b in json.loads((r/'beat_sheet.json').read_text())['beats'] if b['beat_id']=='BMAKE');duration=beat['actual_duration_s']
 raw=r/'captures/tool-construction-native.mov';assert not raw.exists()
 capture=subprocess.Popen(['/usr/sbin/screencapture','-v','-V'+str(math.ceil(duration+1)),'-l'+window,str(raw)],stderr=(r/'captures/tool-construction.stderr').open('w'))
 t0=time.monotonic();time.sleep(3.5)
 send(op='set',property='script',value={'resource':'res://particle_system.gd'},label='Attach original particle script: controls and live result')
 time.sleep(.3);send(op='call',method='_ready');send(op='zoom')
 time.sleep(max(0,8-(time.monotonic()-t0)));send(op='set',property='wind',value=120,label='New exported Wind control changes the trajectory')
 capture.wait(timeout=math.ceil(duration+8));assert capture.returncode==0
 (r/'captures/tool-construction-actions.json').write_text(json.dumps({'capture_start_monotonic':t0,'actions':records,'source':'blank_tool.tscn plus original particle_system.gd; native EditorPlugin attachment and property edit'},indent=2))
 print(raw,flush=True)
finally:
 if capture is not None and capture.poll() is None:capture.send_signal(2);capture.wait(timeout=10)
 if editor.poll() is None:editor.terminate();editor.wait(timeout=10)
 log.close()

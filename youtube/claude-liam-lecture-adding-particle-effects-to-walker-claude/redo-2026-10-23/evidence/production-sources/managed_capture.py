from pathlib import Path
import subprocess,time,json,sys,shutil

def require_unlocked_session():
 state=subprocess.check_output(['/usr/sbin/ioreg','-n','Root','-d1'],text=True)
 if '"CGSSessionScreenIsLocked"=Yes' in state:
  raise SystemExit('BLOCKED: Mac graphical session is locked. No editor launch or capture attempted; unlock is required.')
require_unlocked_session()
w=Path(sys.argv[1]).resolve();r=Path(sys.argv[2]).resolve();base=w.parent
cap=r/'captures';cap.mkdir(exist_ok=True)
rid=int(time.time()*1000000)
def send(**kw):
 global rid
 rid+=1;req=dict(id=rid,label='Native recording setup',**kw);(w/'.lecture/request.tmp').write_text(json.dumps(req));(w/'.lecture/request.tmp').replace(w/'.lecture/request.json');deadline=time.monotonic()+5
 while time.monotonic()<deadline:
  log=w/'.lecture/actions.jsonl'
  if log.exists():
   for line in reversed(log.read_text().splitlines()[-8:]):
    row=json.loads(line)
    if (row.get('request') or {}).get('id')==rid:
     if 'error' in row['result']:raise RuntimeError(row)
     return
  time.sleep(.1)
 raise RuntimeError('No setup acknowledgement')
(w/'.lecture/request.json').write_text(json.dumps(dict(id=rid,op='open',path='res://arena.tscn')))
log=(cap/'editor-full-take.log').open('w');p=subprocess.Popen(['/opt/homebrew/bin/godot','--editor','--path',str(w),'--audio-driver','Dummy'],stdout=log,stderr=subprocess.STDOUT)
try:
 deadline=time.monotonic()+25;win=None
 while time.monotonic()<deadline:
  if p.poll()!=None:raise RuntimeError('Editor exited')
  wins=json.loads(subprocess.check_output([str(base/'native_ui'),'windows']))
  win=next((str(x['kCGWindowNumber']) for x in wins if x['kCGWindowOwnerPID']==p.pid),None)
  if win and (w/'.lecture/actions.jsonl').exists() and str(rid) in (w/'.lecture/actions.jsonl').read_text():break
  time.sleep(.3)
 if not win:raise RuntimeError('No editor window')
 if 'FrameGuide' in (w/'arena.tscn').read_text():
  send(op='select',node='FrameGuide');time.sleep(.3);send(op='zoom',node='FrameGuide');time.sleep(.5);send(op='select')
 else:
  send(op='view3d',angle=45,orbit=False);time.sleep(.5)
 if (r/'pre_capture_actions.json').exists():
  for req in json.loads((r/'pre_capture_actions.json').read_text()):send(**req)
 (cap/'session.json').write_text(json.dumps(dict(editor_pid=p.pid,window_id=win,project=str(w),method='Godot EditorPlugin + macOS window-only screencapture; native pixels, scripted actions'),indent=2))
 subprocess.run([sys.executable,str(base/'capture_film.py'),str(w),str(r),win],check=True)
 send(op='save')
 if (w/'.lecture/input-log.jsonl').exists():shutil.copy2(w/'.lecture/input-log.jsonl',cap/'runtime-input-actions.jsonl')
 print('Managed take complete',flush=True)
finally:
 if p.poll()==None:p.terminate();p.wait(timeout=15)
 log.close()

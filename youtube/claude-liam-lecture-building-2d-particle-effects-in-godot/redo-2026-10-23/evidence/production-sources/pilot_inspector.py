from pathlib import Path
import subprocess,time,json,shutil
w=Path(__file__).resolve().parent/'work-2';out=w.parent/'film2-pilot-inspector-final';out.mkdir(exist_ok=True)
rid=int(time.time());records=[]
def send(**kw):
 global rid
 rid+=1;req=dict(id=rid,label='Film 2 pilot',**kw);(w/'.lecture/request.json').write_text(json.dumps(req));deadline=time.monotonic()+5
 while time.monotonic()<deadline:
  if (w/'.lecture/actions.jsonl').exists():
   for line in reversed((w/'.lecture/actions.jsonl').read_text().splitlines()[-8:]):
    row=json.loads(line)
    if row['request']['id']==rid:
     if row['result'] is None or 'error' in row['result']:raise RuntimeError(row)
     records.append(row);return
  time.sleep(.1)
 raise RuntimeError('No editor acknowledgement '+str(req))
(w/'.lecture/request.json').write_text(json.dumps(dict(id=rid,op='open',path='res://arena.tscn')))
log=(out/'editor.log').open('w');p=subprocess.Popen(['/opt/homebrew/bin/godot','--editor','--path',str(w),'--audio-driver','Dummy'],stdout=log,stderr=subprocess.STDOUT)
try:
 deadline=time.monotonic()+25;win=None
 while time.monotonic()<deadline:
  if p.poll()!=None:raise RuntimeError('Editor exited')
  wins=json.loads(subprocess.check_output([str(w.parent/'native_ui'),'windows']))
  win=next((str(x['kCGWindowNumber']) for x in wins if x['kCGWindowOwnerPID']==p.pid),None)
  if win and (w/'.lecture/actions.jsonl').exists() and str(rid) in (w/'.lecture/actions.jsonl').read_text():break
  time.sleep(.3)
 if not win:raise RuntimeError('No editor window')
 send(op='select',node='FrameGuide');time.sleep(.3);send(op='zoom',node='FrameGuide');time.sleep(1);send(op='select')
 send(op='add',class_name='GPUParticles2D',name='Burst',properties={'position':{'v2':[0,100]},'amount':48,'lifetime':.8})
 send(op='set',node='Burst',property='process_material',value={'new':'ParticleProcessMaterial'})
 send(op='set',node='Burst',property='texture',value={'resource':'res://assets/soft-dot.tres'})
 send(op='set',node='Burst',resource_property='process_material',property='gravity',value={'v3':[0,-140,0]},filter='gravity');time.sleep(1)
 subprocess.run(['/usr/sbin/screencapture','-x','-o','-l'+win,str(out/'editor.png')],check=True)
 print(out,flush=True)
finally:
 if p.poll()==None:p.terminate();p.wait(timeout=15)
 log.close()

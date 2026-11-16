from pathlib import Path
import subprocess,time,json
w=Path('/Users/bear/Documents/Codex/2026-10-23/task-3/work-1');r=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-what-is-a-particle-system/redo-2026-10-23');p=w/'.lecture/request.json'
def send(i,**kw):p.write_text(json.dumps({'id':i,**kw}))
send(90200,op='open',path='res://lesson.tscn')
log=(w/'.lecture/editor-code-managed.log').open('w')
editor=subprocess.Popen(['/opt/homebrew/bin/godot','--editor','--path',str(w),'--single-window','--audio-driver','Dummy'],stdout=log,stderr=subprocess.STDOUT)
try:
 deadline=time.monotonic()+15;window=None
 while time.monotonic()<deadline:
  if editor.poll() is not None:raise RuntimeError('Editor terminated before capture: '+str(editor.returncode))
  windows=json.loads(subprocess.check_output([str(w.parent/'native_ui'),'windows']))
  window=next((str(x['kCGWindowNumber']) for x in windows if x['kCGWindowOwnerPID']==editor.pid),None)
  if window and (w/'.lecture/actions.jsonl').exists() and '90200' in (w/'.lecture/actions.jsonl').read_text():break
  time.sleep(.3)
 if not window:raise RuntimeError('No editor window')
 send(90201,op='script',path='res://particle_system.gd',line=30,label='Actual script: particle records');time.sleep(.7)
 out=r/'captures/code-inserts-native-v2.mov'
 err=(r/'captures/code-inserts-v2.stderr').open('w')
 f=subprocess.Popen(['/usr/sbin/screencapture','-v','-V22','-l'+window,str(out)],stderr=err)
 t=time.monotonic()
 for delay,i,line in [(7,90202,49),(14,90203,8)]:
  time.sleep(max(0,delay-(time.monotonic()-t)))
  if editor.poll() is not None:raise RuntimeError('Editor terminated during capture: '+str(editor.returncode))
  send(i,op='script',path='res://particle_system.gd',line=line,label='Actual script: readable source')
 f.wait(timeout=25)
 print('code insert capture',f.returncode,out,flush=True)
finally:
 if editor.poll() is None:editor.terminate();editor.wait(timeout=10)
 log.close()

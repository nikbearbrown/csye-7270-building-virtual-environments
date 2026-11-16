from pathlib import Path
import subprocess,time,json,math
w=Path('/Users/bear/Documents/Codex/2026-10-23/task-3/work-1');r=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-what-is-a-particle-system/redo-2026-10-23');p=w/'.lecture/request.json';records=[]
def send(i,**kw):
 req={'id':i,**kw};p.write_text(json.dumps(req));time.sleep(.3);records.append({'sent_monotonic':time.monotonic(),'request':req})
send(90300,op='open',path='res://lesson.tscn')
log=(w/'.lecture/editor-single-particle.log').open('w')
editor=subprocess.Popen(['/opt/homebrew/bin/godot','--editor','--path',str(w),'--single-window','--audio-driver','Dummy'],stdout=log,stderr=subprocess.STDOUT)
try:
 deadline=time.monotonic()+15;window=None
 while time.monotonic()<deadline:
  if editor.poll() is not None:raise RuntimeError('Editor terminated: '+str(editor.returncode))
  windows=json.loads(subprocess.check_output([str(w.parent/'native_ui'),'windows']))
  window=next((str(x['kCGWindowNumber']) for x in windows if x['kCGWindowOwnerPID']==editor.pid),None)
  if window and '90300' in (w/'.lecture/actions.jsonl').read_text():break
  time.sleep(.3)
 for i,(prop,v) in enumerate([('heading','One Moving Element'),('birth_rate',0),('lifetime',2.5),('spread',15),('radius',14),('vectors',True),('fade',False),('shrink',False),('burst_size',1)],90301):send(i,op='set',property=prop,value=v)
 send(90320,op='call',method='reset');send(90321,op='zoom')
 b=next(b for b in json.loads((r/'beat_sheet.json').read_text())['beats'] if b['beat_id']=='BONE');duration=b['actual_duration_s']
 out=r/'captures/one-particle-native.mov';err=(r/'captures/one-particle.stderr').open('w')
 f=subprocess.Popen(['/usr/sbin/screencapture','-v','-V'+str(math.ceil(duration+1)),'-l'+window,str(out)],stderr=err)
 t=time.monotonic();time.sleep(.3);send(90330,op='call',method='burst',label='One birth: position, velocity, acceleration')
 time.sleep(max(0,5-(time.monotonic()-t)));send(90331,op='call',method='burst',label='Second single-particle trial')
 f.wait(timeout=math.ceil(duration+8));print('single particle capture',f.returncode,out)
 (r/'captures/one-particle-actions.json').write_text(json.dumps({'capture_start_monotonic':t,'actions':records},indent=2))
finally:
 if editor.poll() is None:editor.terminate();editor.wait(timeout=10)
 log.close()

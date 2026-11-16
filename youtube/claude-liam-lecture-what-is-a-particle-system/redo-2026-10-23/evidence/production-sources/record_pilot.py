import json,time,subprocess
from pathlib import Path
p=Path('/Users/bear/Documents/Codex/2026-10-23/task-3/pilot/editor-request.json')
def request(i,prop,v):
 p.write_text(json.dumps({'id':i,'op':'set','node':'Fountain','property':prop,'value':v}))
request(7,'amount',40);time.sleep(.4);request(8,'lifetime',2);time.sleep(2)
out=Path('/Users/bear/Documents/Codex/2026-10-23/task-3/pilot-reel/native-pilot.mov')
f=subprocess.Popen(['/usr/sbin/screencapture','-v','-V21','-l4533',str(out)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
t0=time.monotonic()
for delay,i,prop,v in [(7,9,'amount',160),(13,10,'lifetime',1)]:
 time.sleep(max(0,delay-(time.monotonic()-t0)))
 request(i,prop,v)
o,e=f.communicate(timeout=30)
print('return',f.returncode,'stdout',o.decode(),'stderr',e.decode(),'size',out.stat().st_size if out.exists() else None)

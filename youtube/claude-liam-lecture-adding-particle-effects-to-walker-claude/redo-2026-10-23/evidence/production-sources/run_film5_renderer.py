from pathlib import Path
import subprocess,json,statistics,datetime,hashlib,platform
W=Path(__file__).resolve().parent;w=W/'work-5';out=W/'film5-renderer';out.mkdir(exist_ok=True)
state=subprocess.check_output(['/usr/sbin/ioreg','-n','Root','-d1'],text=True)
if '"CGSSessionScreenIsLocked"=Yes' in state:raise SystemExit('Blocked: Mac locked. No renderer pricing or capture attempted.')
rows=[]
for fresh in range(3):
 cmd=['/opt/homebrew/bin/godot','--path',str(w),'--fixed-fps','60','--script','res://tests/price-render.gd','--audio-driver','Dummy']
 r=subprocess.run(cmd,capture_output=True,text=True,timeout=240);text=r.stdout+r.stderr;(out/f'render-fresh-{fresh}.log').write_text(text)
 if r.returncode or 'SCRIPT ERROR' in text:raise RuntimeError(text)
 for line in text.splitlines():
  if line.startswith('RENDER,'):rows.append(dict(json.loads(line[7:]),fresh_process=fresh,command=cmd))
 print('Renderer process',fresh,'complete',flush=True)
assert len(rows)==36
summary=[]
for mode in ['off','burst-loop-upper-bound','ambient','both']:
 sample=[r for r in rows if r['mode']==mode];gpu=[r['render_gpu_ms'] for r in sample if r['gpu_timer_available']]
 summary.append(dict(mode=mode,render_cpu_ms=statistics.median(r['render_cpu_ms'] for r in sample),render_gpu_ms=statistics.median(gpu) if gpu else None,draw_calls=statistics.median(r['draw_calls'] for r in sample)))
result=dict(created=datetime.datetime.now(datetime.timezone.utc).isoformat(),rows=rows,summary=summary,instrument='RenderingServer viewport CPU/GPU timers + frame setup; 60 warm-up / 300 timed / 3 repeats / 3 fresh processes.',renderer_context=rows[0]['adapter']+' · '+rows[0]['renderer']+' · '+rows[0]['window_pixels'],effect_sha256={n:hashlib.sha256((w/'effects'/n).read_bytes()).hexdigest() for n in ['burst.tscn','ambient.tscn']},machine=platform.platform())
(out/'results.json').write_text(json.dumps(result,indent=2));(w/'evidence/render-results.json').write_text(json.dumps(result,indent=2));print(json.dumps(summary),flush=True)

from pathlib import Path
import subprocess,json,platform,statistics,datetime
W=Path(__file__).resolve().parent;w=W/'work-5';out=W/'film5-selected-checks';out.mkdir(exist_ok=True)
for name,script in [('build-tuning','build_tuning.gd'),('bake-editor-lab','bake_editor_lab.gd'),('selected-regression-real-time','tests/test-game.gd'),('selected-effects-real-time','tests/test-effects.gd')]:
 cmd=['/opt/homebrew/bin/godot','--headless','--path',str(w),'--max-fps','60','--script','res://'+script];r=subprocess.run(cmd,capture_output=True,text=True,timeout=55);text=r.stdout+r.stderr;(out/(name+'.log')).write_text(text);print(name,r.returncode,text[-250:],flush=True)
 if r.returncode or 'SCRIPT ERROR' in text:raise RuntimeError(name)
rows=[]
for fresh in range(3):
 cmd=['/opt/homebrew/bin/godot','--headless','--path',str(w),'--fixed-fps','60','--script','res://tests/price-cpu.gd'];r=subprocess.run(cmd,capture_output=True,text=True,timeout=60);text=r.stdout+r.stderr;(out/f'cpu-fresh-{fresh}.log').write_text(text);assert r.returncode==0 and 'ERROR' not in text,text
 for line in text.splitlines():
  if line.startswith('PRICE,'):rows.append(dict(json.loads(line[6:]),fresh_process=fresh,command=cmd))
 print('CPU process',fresh,'done',flush=True)
assert len(rows)==36
import hashlib
source_hashes={n:hashlib.sha256((w/'effects'/n).read_bytes()).hexdigest() for n in ['burst.tscn','ambient.tscn']}
summary=[]
for mode in ['empty','burst-loop-upper-bound','ambient','both']:
 values=[r['mean_ms'] for r in rows if r['mode']==mode];summary.append(dict(mode=mode,median_ms=statistics.median(values),min_ms=min(values),max_ms=max(values),samples=len(values)))
(out/'cpu-results.json').write_text(json.dumps(dict(created=datetime.datetime.now(datetime.timezone.utc).isoformat(),machine=platform.platform(),effect_sha256=source_hashes,engine=subprocess.check_output(['/opt/homebrew/bin/godot','--version'],text=True).strip(),rows=rows,summary=summary,limits='Headless CPU wall instrument; no GPU rendering or interactive frame-time claim. Provisional tuned appearance awaits native visual comparison. Same fixed 60 Hz simulation, 60 warm-up and 300 timed frames; 3 repetitions in each of 3 fresh processes.'),indent=2))
print(json.dumps(summary),flush=True)

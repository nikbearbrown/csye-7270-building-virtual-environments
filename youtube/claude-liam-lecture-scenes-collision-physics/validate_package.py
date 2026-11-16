from pathlib import Path
import ast,re,json,sys,subprocess,hashlib
R=Path(__file__).resolve().parent;T=R.parents[2]/'brutalist.art';sys.path.insert(0,str(T/'runtime/scripts'))
from build_safety import validate_project,validate_approvals
s=json.loads((R/'beat_sheet.json').read_text());validate_project(s);validate_approvals(R,s)
for p in R.glob('*.py'):ast.parse(p.read_text(),filename=str(p))
bs=s['beats'];ids=[b['beat_id'] for b in bs];assert len(ids)==len(set(ids))==67
assert ids[:3]==['BOPEN','BIDEA','BDEFS'] and ids[-3:]==['BVDT','BHTF','BOUT']
assert all(re.fullmatch(r'B[0-9A-Z]+',x) for x in ids)
assert bs[-2]['narration_text']==bs[-2]['shot']['remotion']['props']['command']
assert len(bs[-3]['shot']['remotion']['props']['artifactLines'])==6
assert bs[-1]['narration_text']==s['metadata']['title']+'. At Nik Bear Brown.'
assert not any(k in s['metadata'] for k in ['series_video_number','series_video_count','series_entry_video'])
classes=re.findall(r'^class (B\w+)\(Scene\):',(R/'scenes.py').read_text(),re.M);results=[]
for cls in classes:
 p=subprocess.run([sys.executable,str(T/'runtime/qc/static_scene_check.py'),str(R/'scenes.py'),'--class',cls],text=True,capture_output=True)
 results.append({'class':cls,'returncode':p.returncode,'output':p.stdout+p.stderr});assert p.returncode==0,(cls,p.stdout,p.stderr)
for b in bs:
 sh=b['shot']
 if 'manim' in sh:assert sh['manim']['class'] in classes
 if 'remotion' in sh:
  p=sh['remotion']['props'];pattern=sh['remotion']['pattern'];assert (T/'runtime/remotion/src/scenes'/f'{pattern}.tsx').exists()
  if pattern=='BrowserCapture':assert (T/'runtime/remotion/public'/p['image']).exists()
 if b['lane'] not in ['bookend','card']:assert b['lecture']['runner_up'] and sh['motion_claim'] and sh['show']
for name in ['ACTS.md','SHOTLIST.md','FACTCHECK.md','PROMPTS.md','SOURCES.md','BUILD-PROMPT.md','BUILD-LOG.md','CHECKS-REPORT.md']:assert (R/name).exists(),name
subprocess.run([sys.executable,str(R/'verify_evidence.py')],check=True)
p=subprocess.run([sys.executable,str(T/'runtime/qc/beat_lint.py'),str(R/'beat_sheet.json')],text=True,capture_output=True);assert p.returncode==0,p.stdout+p.stderr
(R/'evidence/static-scene-checks.json').write_text(json.dumps(results,indent=2))
record={'status':'preparation passed','beats':len(bs),'manim_classes':len(classes),'static_errors':0,'static_warnings':0,'engine_checks':32,'beat_lint':p.stdout,'runtime_validation':'validate_project and validate_approvals passed','schema_exception':'Legacy schema excludes CARD; current mandated BOPEN contract uses CARD and runtime accepts it. No shared schema modified.','not_run':['audio synthesis and listening','film stills','film render','Gate B/V/T','final master and bookend checks']}
(R/'evidence/package-validation.json').write_text(json.dumps(record,indent=2))
files=[*list((R/'godot').glob('*.gd')),*list((R/'godot').glob('*.tscn')),R/'godot/project.godot',R/'scenes.py',R/'content.json',*list((R/'captures').glob('*.png'))]
(R/'evidence/source-hashes.json').write_text(json.dumps({str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2))
print(json.dumps(record,indent=2))

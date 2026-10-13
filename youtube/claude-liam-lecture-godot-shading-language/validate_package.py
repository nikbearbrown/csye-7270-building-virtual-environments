#!/usr/bin/env python3
from pathlib import Path
import ast,sys,re,json,subprocess,collections
R=Path(__file__).resolve().parent
T=R.parents[2]/'brutalist.art'
sys.path.insert(0,str(T/'runtime/scripts'))
from build_safety import validate_project,validate_approvals
s=json.loads((R/'beat_sheet.json').read_text());validate_project(s);validate_approvals(R,s)
for p in R.glob('*.py'):ast.parse(p.read_text(),filename=str(p))
bs=s['beats']; ids=[b['beat_id'] for b in bs]
assert ids[:3]==['BOPEN','BIDEA','BDEFS'] and ids[-3:]==['BVDT','BHTF','BOUT']
assert len(ids)==len(set(ids))==58
assert all(re.fullmatch(r'B[0-9A-Z]+',x) for x in ids)
assert bs[-2]['narration_text']==bs[-2]['shot']['remotion']['props']['command']
assert len(bs[-3]['shot']['remotion']['props']['artifactLines'])==6
assert not any(k in s['metadata'] for k in ['series_video_number','series_video_count','series_entry_video'])
source=(R/'scenes.py').read_text();classes=re.findall(r'^class (B\w+)\(Scene\):',source,re.M)
results=[]
for cls in classes:
 run=subprocess.run([sys.executable,str(T/'runtime/qc/static_scene_check.py'),str(R/'scenes.py'),'--class',cls],text=True,capture_output=True)
 results.append({'class':cls,'returncode':run.returncode,'output':run.stdout+run.stderr})
 assert run.returncode==0,(cls,run.stdout,run.stderr)
for b in bs:
 sh=b['shot']
 if 'manim' in sh:assert sh['manim']['class'] in classes
 if 'remotion' in sh:
  p=sh['remotion']['props'];pattern=sh['remotion']['pattern']
  assert (T/'runtime/remotion/src/scenes'/f'{pattern}.tsx').exists(),pattern
  if pattern=='BrowserCapture':assert (T/'runtime/remotion/public'/p['image']).exists()
 if b['lane'] not in ['bookend','card']:
  assert b.get('lecture',{}).get('runner_up') and sh.get('show') and sh.get('motion_claim')
subprocess.run([sys.executable,str(R/'verify_evidence.py')],check=True)
lint=subprocess.run([sys.executable,str(T/'runtime/qc/beat_lint.py'),str(R/'beat_sheet.json')],text=True,capture_output=True)
assert lint.returncode==0,lint.stdout
(R/'evidence/static-scene-checks.json').write_text(json.dumps(results,indent=2)+'\n')
result={'status':'preparation checks passed','beats':len(bs),'manim_classes':len(classes),'static_errors':0,'static_warnings':0,'runtime_contract':'validate_project and validate_approvals passed; no human approval record required or fabricated','beat_lint':lint.stdout,'legacy_json_schema_note':'The legacy schema excludes CARD. The explicitly mandated lecture BOPEN template uses CARD per its current integration contract; runtime validation accepts it. The legacy schema was not edited.','not_run':['TTS','film still render','pixel-layout gate','full film render','typography gate','audio listening','final-master verification']}
(R/'evidence/package-validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

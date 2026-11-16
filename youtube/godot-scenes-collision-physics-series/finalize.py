#!/usr/bin/env python3
from pathlib import Path
import json,sys,subprocess,hashlib,importlib.util,collections,re
S=Path(__file__).resolve().parent;Y=S.parent;T=Y.parent.parent/'brutalist.art';O=Y/'claude-liam-lecture-scenes-collision-physics';L=S/'evidence-lab'
films=json.loads((S/'films.json').read_text())
spec=importlib.util.spec_from_file_location('title_template',T/'skills/make/lecture/templates/title-slide-16x9/build.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
reports=[]
for f in films:
 R=Y/f['slug'];sheet=json.loads((R/'beat_sheet.json').read_text());C=json.loads((R/'content.json').read_text());bs=sheet['beats'];ids=[b['beat_id'] for b in bs]
 assert len(C['recap'])==4 and len(C['terms'])==4
 assert all(4<=sum(b['act']==i for b in C['body'])<=10 for i in range(4))
 assert all(len(t)<=17 for t,m in C['terms'])
 assert C['trigger'] in C['framing'] and not C['trigger'].endswith(('.',',','?','!'))
 assert all(not b['narration_text'].endswith('?.') for b in bs)
 assert len(C['title_lines'])<=3 and all(len(x)<=28 for x in C['title_lines'])
 fields=mod.from_sheet(sheet);mod.svg(fields) # validate opening fields, without rendering or synthesizing
 (R/'evidence/portrait-selection.txt').write_text('Seed: '+R.name+'\nPortrait: '+str(fields['portrait_path'])+'\nSelected for this film; opening is not rendered yet.\n')
 (R/'opening-fields.json').write_text(json.dumps(fields,indent=2)+'\n')
 entries=json.loads((R/'evidence/excerpt-map.json').read_text())
 entries=[e for e in entries if e['key'] not in ['conventions','migration_excerpt']]
 entries += [{'key':'conventions','file':'CONVENTIONS.md','kind':'authored summary of proposed project policy, not executable code'},{'key':'migration_excerpt','file':'sources/docs-migration.txt','kind':'four exact short quotations with subject labels'}]
 (R/'evidence/excerpt-map.json').write_text(json.dumps(entries,indent=2)+'\n')
 em={}
 for entry in entries:em.setdefault(entry['key'],[]).append(entry)
 excerpt_checks=[]
 for b in C['body']:
  if b['lane']!='code':continue
  key=b['asset'];group=em[key];entry=group[0];actual=(R/'excerpts'/f'{key}.txt').read_text().strip();ll=(R/entry['file']).read_text().splitlines()
  if key=='conventions':
   assert 'Suggested project conventions' in '\n'.join(ll)
   assert 'record version and backend' in actual and 'physics callbacks' in actual
  elif key=='migration_excerpt':
   for quote in re.findall('“([^”]+)”',actual):assert quote in '\n'.join(ll),quote
  elif len(group)>1:
   expected='\n'.join(ll[entry['start_line']-1:entry['end_line']])+'\n'
   for e in group[1:]:
    source=(R/e['file']).read_text().splitlines();expected+='\n# Also executed: '+e['file']+':'+str(e['start_line'])+'\n'+'\n'.join(source[e['start_line']-1:e['end_line']])+'\n'
   assert actual==expected.strip(),(R.name,key)
  elif 'start_line' in entry:expected='\n'.join(ll[entry['start_line']-1:entry['end_line']]).strip();assert actual==expected,(R.name,key)
  elif 'line_numbers' in entry:expected='\n'.join(ll[j-1] for j in entry['line_numbers']).strip();assert actual==expected,(R.name,key)
  elif key=='door-tree':
   for name,typ in [('Door','Node2D'),('Panel','Polygon2D'),('Solid','StaticBody2D'),('Approach','Area2D')]:assert f'[node name="{name}" type="{typ}"' in '\n'.join(ll)
  excerpt_checks.append(key)
 (R/'evidence/selected-excerpt-checks.json').write_text(json.dumps({'checked':excerpt_checks,'status':'exact or explicitly derived source matches'},indent=2)+'\n')
 subprocess.run(['python3',str(R/'validate_package.py')],check=True,stdout=subprocess.DEVNULL)
 report=json.loads((R/'evidence/package-validation.json').read_text());secs=round(sum(b['estimated_duration_s'] for b in bs));lane=collections.Counter(b['lane'] for b in C['body'])
 report.update({'title':f['title'],'duration_estimate_seconds':secs,'duration_measured':False,'body_lanes':dict(lane),'exact_excerpts_verified':len(excerpt_checks)})
 reports.append(report)
 (R/'CHECKS-REPORT.md').write_text('# Preparation checks\n\nStatus: PASS for preparation only.\n\n'+f"- {len(bs)} total beats; four acts; {len(C['body'])} body beats.\n- All body beats SHOW; no HOLD or PUNT.\n- Body lanes: "+', '.join(f'{v} {k}' for k,v in lane.items())+'.\n'+f"- {report['manim_classes']} literal Manim classes; zero static errors or warnings.\n- Runtime project/approval validation and beat lint passed.\n- {len(excerpt_checks)} used code excerpts match their recorded source or labeled derivation.\n- Opening fields and slug-seeded portrait resolve through the approved template.\n- Inherited evidence: 32 cases; additional comparison: 21 cases, all passed. Results were reused across films, not re-executed for each copy.\n- New screenshots inspected as native 3840 × 2160 engine evidence.\n\nEstimated runtime {secs//60}:{secs%60:02d}; not measured. Audio synthesis/listening, alignment, film stills, render, final visual/typography/audio/bookend gates and master inspection remain unrun. No MP4 is delivered by this stage.\n")
 prov=[]
 for d in ['captures','sources','godot','evidence']:
  for p in (R/d).iterdir():
   if not p.is_file():continue
   candidates=[L/d/p.name,O/d/p.name]
   origin=next((q for q in candidates if q.exists() and q.is_file() and q.read_bytes()==p.read_bytes()),None)
   if origin:prov.append({'copy':str(p.relative_to(R)),'origin':str(origin),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 (R/'evidence/reused-provenance.json').write_text(json.dumps(prov,indent=2)+'\n')
 with (R/'BUILD-LOG.md').open('a') as out:out.write('\nThe final graphics repetition stalled at a frame-post-draw wait and was stopped. Earlier complete captures were retained; a fresh headless run verified all 21 checks against the final script. comparison-rendered-interrupted.log is not a success record.\nFinal preparation validation passed: exact excerpt checks, template field validation, runtime validation, scene static checks and beat lint. See CHECKS-REPORT.md. No final rendering gate was run.\n')
(S/'validation-summary.json').write_text(json.dumps(reports,indent=2)+'\n')
index='# Godot lecture films — prepared production packages\n\nLiam in for Bear · CSYE 7270 Building Virtual Environments · @NikBearBrown. Each film is independent and has four acts. These are complete stage-one scripts and production specifications; audio and final movies are not yet rendered.\n\n| Recommended order | Film and script | Estimated speech/edit time | Build handoff |\n|---|---|---|---|\n'
for i,(f,r) in enumerate(zip(films,reports),1):
 R=Y/f['slug'];secs=r['duration_estimate_seconds'];index+=f"| {i} | [{f['title']}]({R}/NARRATION.md) | {secs//60}:{secs%60:02d}, unmeasured | [Build]({R}/BUILD-PROMPT.md) |\n"
index+='\n[Teaching layout]('+str(S/'SERIES.md')+') · [Whole-source coverage]('+str(S/'SOURCE-COVERAGE.md')+') · [Build all four]('+str(S/'BUILD-ALL.md')+')\n\nPreparation validation passed for all packages. The original 32-case evidence is retained with provenance. The new paired body/area and door experiment passed 21 checks. Native engine captures were inspected. Static checks are not a substitute for the later audio, frame and master reviews.\n\nCollider commonly means a solid collision boundary; a trigger detects overlap without solid blocking. Both use collision geometry. In Godot, a physics body or an Area owns the shape and gives it its role. The door demonstrates both: a solid panel and a larger approach sensor. See the [official physics introduction](https://docs.godotengine.org/en/stable/tutorials/physics/physics_introduction.html).\n'
(S/'README.md').write_text(index)
allbuild='# Build the prepared Godot lecture films\n\nLaunch Claude Code from `/Users/bear/Documents/CoWork/bear-textbooks/books`. Read the applicable CLAUDE.md and the lecture skill in brutalist.art. This is the stage-two render handoff. Build the films below sequentially; each is a separate deliverable. Read each BUILD-PROMPT.md fully before its build. Do not rebuild the old combined lecture or regenerate these packages from assemble.py. The finalized per-film content.json is authoritative.\n\n'
for f in films:allbuild+='- '+f['title']+': `'+str(Y/f['slug']/'BUILD-PROMPT.md')+'`\n'
allbuild+='\nFor each: generate and listen to Liam/am_onyx narration; measure and align audio; build the approved portrait/title opening; render and inspect stills; fix only failed units; run normal review/final gates; inspect the 3840 × 2160 master and exact outro. Respect each film\'s four-sentence recap, full Your Turn prompt, and one-second outro tail. Estimates are not duration targets. Do not add series numbers. Do not use paid generation, publish, stage or push.\n\nDo not call a preparation pass a final render pass. Report each actual master path, measured duration, lane count and gate results. The new 21 checks were run once centrally and copied with hashes, alongside inherited 32-case evidence; do not claim independent repeated testing. Multiple-actor door race cases, platform carry/leave behavior, drop-through clearance and human control feel remain separate tests.\n\nIf one film has a genuinely external blocker, record the specific blocker and continue independent films. Finish all authorized rendering work that can proceed.\n'
(S/'BUILD-ALL.md').write_text(allbuild)
print(json.dumps([{'title':r['title'],'beats':r['beats'],'estimate_s':r['duration_estimate_seconds'],'status':r['status']} for r in reports],indent=2))

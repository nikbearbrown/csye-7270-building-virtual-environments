from pathlib import Path
import re,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
paste=ROOT/'canvas/assignment-sources/final-project-pasted.txt'
s=paste.read_text();old=(ROOT/'pantry/backups/assignments-before-canvas-sync-2026-10-14/10-final-project.md').read_text()
s=re.sub(r'^(?:bash|text)\n(?=```)', '',s,flags=re.M)
s='# Assignment 10 - Final Project: From Brief to Export\n\n'+s
s=s.replace('CSYE 7270 · Fall 2026 · 250 points','CSYE 7270 · Fall 2026 · **250 points**',1)
anchors=[('This is the final project,','## Executive summary\n\n'),('Start this project early.','## Your task\n\n'),('Bring your Assignment 9 technique from its scenario scenes','### Integrate your Assignment 9 technique\n\n'),('- GDD. Update','### Take the cycle to export\n\n'),('Replace the contents of CHANGE-BRIEF.md','## 1. Predict\n\n'),('Split the work into separate agent runs','## 2. Build It\n\n'),('What agents got wrong in Modules 14 and 15','### What the recorded runs got wrong\n\n'),('Record actual results in TEST-REPORT.md','## 3. Use It\n\n'),('Use the course-provided [Brutalist]','### The two defense films\n\n'),('- The game source and used assets','## 4. Ship It\n\n'),('Clone tag a10 into an empty folder','## 5. Verify\n\n'),('In FRICTIONAL.md, record','### Frictional — honest log — 25 points\n\n'),('- 10 points: Required, accessible game source','### GitHub version posting matching Canvas — 25 points\n\n'),('Assigned after the instructor and TAs','### Relative Quartile — 50 points\n\n'),('Use SOURCES.md to credit every starter','## Academic integrity\n\n')]
for needle,heading in anchors:
 assert needle in s,needle;s=s.replace(needle,heading+needle,1)
prep='''
| Preparation target | Work toward the final |
|---|---|
| Assignment 4 GDD — October 19 | Read the final brief; name the core loop, scope, export target and largest uncertainty. |
| Assignment 5 shaders — October 29 | Keep the shaders/materials and their evidence; identify renderer-dependent features. |
| Assignment 6 particles — November 3 | Preserve visual and cost checks; write save rules and attempt an early export. |
| Assignment 7 animation — November 15 | Keep a small playable loop with documented transitions and earlier layers working. |
| Assignment 8 pitch — November 22 | Save the “exists today” and “will exist” lists that the final must reconcile. |
| Assignment 9 teaching technique — December 12 | Preserve the technique, tests and teach/ projects; plan its integration and the audit gap. |
| Assignment 10 final — December 20 | Complete integration, persistence, menu, clean-clone/export evidence, pitch ledger and both films. |
'''
s=s.replace('Then work to these targets:\n','Then work to these targets:\n'+prep+'\n',1)
options=re.search(r'(\| Option \(Module 14\).*?)(?=\n\nA behavior-tree addon)',old,re.S).group(1)
# Retain only option minima consistent with the new final; do not impose a second new technique.
s=s.replace('A behaviour-tree addon',options+'\n\nA behaviour-tree addon',1)
checks='''
| Check | Evidence to collect |
|---|---|
| Clean clone of a10 | Import log, git status, generated-file inventory, engine/renderer/OS, short main-scene run and every documented test result. |
| Assignment 9 technique in the finished game | The technique's checks, scenario-to-game integration evidence, the new audit of a missed case, and your own play against it. |
| Assignment 9 teach/ projects | The documented starter and solution checks with the correct GODOT_PROJECT, preserving the tested revision. |
| Persistence | Round trip, missing/corrupt/newer-version/unwritable cases, real save folder unchanged by tests, and a human restart check. |
| Menu | Start or pause menu operated by keyboard, with initial focus; screen-reader testing only if actually attempted. |
| Semester layers | Generated art/sound, Blender assets, GDD/interaction, shaders/materials, particles, animation and game AI working together, or a documented removal/replacement. |
| Pitch ledger | Each Assignment 8 “will exist” item marked delivered, changed or dropped, with evidence or reason. |
| Export state | Committed preset, target/renderer, inspected pack contents, export attempt, exact blockers or played exported build, and checksum if built. |
| Human playtest and revision | A real full play session and at least one observation-driven inspect-and-revise cycle; honest remaining limits. |
'''
s=s.replace('Record actual results in TEST-REPORT.md, with revision, engine version, renderer, operating system and date:\n','Record actual results in TEST-REPORT.md, with revision, engine version, renderer, operating system and date:\n'+checks+'\n',1)
# Scale the established 60-point implementation weights by 2.5. New prose and cases govern.
# Replace older optional-new-technique and Assignment-9-audio assumptions with the final's requirements.
impl='''
| Criterion | Points |
|---|---:|
| Assignment 9 technique integrated into real play, justified if changed, behind the specified observable-state test contract; an audit of a case the tests miss and human play against it. | 32.5 |
| Persistence and reproduction: save rules written first and enforced, version/corruption handling, isolated save tests, and a clean a10 clone passing every documented game and teach/ check. | 25 |
| Export: committed preset, target/renderer decision, inspected pack contents and an attempted release export; source-ready/export-ready claims match actual evidence. | 15 |
| Finished game: the semester's layers working together, a keyboard-usable front door, a reconciled pitch ledger, clear run instructions, names, licenses and professional presentation. | 30 |
| Verification: actual full playtesting, an observation-driven revision, appropriate checks and honest limitations. | 12.5 |
| Both required Brutalist films: real-play coverage and GDD defense, pitch/save/export evidence, all five capacities with concrete tagged moments, readable/audible films showing the submitted game revision. | 35 |
| **Subtotal** | **150** |
'''
rubric='''## Rubric — 250 points

| Component | Points |
|---|---:|
| Implementation and explanation | 150 |
| Frictional — honest log | 25 |
| GitHub version posting matching Canvas | 25 |
| Relative Quartile | 50 |
| **Total** | **250** |

### Implementation and explanation — 150 points

'''+impl+'\n'
s=s.replace('Award partial credit for demonstrated work within each criterion.',rubric+'Award partial credit for demonstrated work within each criterion.',1)
# Link supplied references without changing the task's substance.
s=s.replace('See the Fall 2026 assignment schedule','See the [Fall 2026 assignment schedule](fall-2026-assignment-schedule.md)',1)
s=s.replace('See the release and preparation plan.','See the [release and preparation plan](fall-2026-assignment-schedule.md#release-and-preparation-plan).',1)
links={'the Module 15 lesson':'the [Module 15 lesson](../modules/15-final-projects-brief-to-export/lesson.md)','the Module 14 lesson':'the [Module 14 lesson](../modules/14-game-ai-and-systems/lesson.md)','its labs page':'its [labs page](../modules/14-game-ai-and-systems/labs.md)','examples/15-final-projects-brief-to-export':'[examples/15-final-projects-brief-to-export](../examples/15-final-projects-brief-to-export/)','examples/14-game-ai-and-systems':'[examples/14-game-ai-and-systems](../examples/14-game-ai-and-systems/)'}
for a,b in links.items():s=s.replace(a,b,1)
(ROOT/'assignments/10-final-project.md').write_text(s)
shutil_copy=paste.read_bytes();(ROOT/'canvas/assignment-sources/final-project-pasted.txt').write_bytes(shutil_copy)
p=ROOT/'assignments/canvas-authority.json';d=json.loads(p.read_text());r=d['assignments'][-1];r['pasted_source']='canvas/assignment-sources/final-project-pasted.txt';r['pasted_sha256']=hashlib.sha256(shutil_copy).hexdigest();r['imported_markdown_sha256']=hashlib.sha256(s.encode()).hexdigest();r['restored_tables']={'authorized_by':'Bear, 2026-10-14: adapt to match the final assignments','preparation':'aligned with exported A4–A10 deadlines and pasted final requirements','options':'retained prior Module 14 technique minima, used only if the A9 technique changes','use_it':'adapted to game-AI integration, teach/ preservation, pitch ledger and final export state','implementation':'prior 60-point criterion weights scaled by 2.5 to 150; descriptions conform to the pasted final'};p.write_text(json.dumps(d,indent=2)+'\n')
print('Final restored from the pasted text; compatible tables adapted to its requirements and 250-point total.')

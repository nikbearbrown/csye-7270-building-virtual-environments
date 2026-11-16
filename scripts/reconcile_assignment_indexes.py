from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'assignments/canvas-authority.json').read_text());rows=data['assignments']
films={1:'godot-walkthrough',2:'godot-gamedev',3:'godot-gamedev',4:'No film specified',5:'godot-gamedev',6:'godot-gamedev',7:'godot-walkthrough',8:'Brutalist pitch film',9:'godot-walkthrough (Explain → Show → Try)',10:'godot-walkthrough + godot-gdd'}
# Titles/metadata are Canvas's; the new final's title comes from the instructor's replacement.
rows[3]['modules']=[5]
rows[-1].setdefault('canvas_title',rows[-1]['title']);rows[-1]['title']='Assignment 10 - Final Project: From Brief to Export'
(ROOT/'assignments/canvas-authority.json').write_text(json.dumps(data,indent=2)+'\n')
def table():
 out='| # | Assignment | Points | Due (America/New_York) | Modules | Required film |\n|---|---|---:|---|---|---|\n'
 for r in rows:
  date=r['due_at_local'][:10];out+=f"| {r['number']} | [{r['title']}](../{r['source']}) | {r['points']:g} | {date}, 11:59 pm | {', '.join(map(str,r['modules']))} | {films[r['number']]} |\n"
 return out
text='# Assignments — CSYE 7270, Fall 2026\n\nThe repository now follows the Fall 2026 Canvas export supplied on October 14, 2026. Canvas is authoritative for Assignments 1–9, their titles, point values, deadlines and submission settings. The instructor’s pasted replacement is authoritative for Assignment 10; the export confirms its 250-point value and December 20 deadline.\n\nAssignment 4 is the five-point GDD. It is part of this ten-assignment sequence, not an additional milestone. Assignment 8 is a 50-point pitch. The seven 100-point assignments, GDD, pitch and 250-point final total **1,005 points**. Individual briefs govern their grading; the GDD does not inherit a 100-point rubric.\n\n'+table()+'\n## One project and its evidence\n\nFrom Assignment 2 onward, use the chosen `walker-` project and the revisions/tagging required by each brief. The final integrates the semester’s work, Assignment 9’s technique, persistence, a menu, pitch reconciliation and clean-clone/export evidence. Read the exact assignment before treating a lesson exercise as a graded requirement.\n\nRead the [AI policy](../prerequisites/ai-policy.md) and [film requirements](../prerequisites/brutalist-godot-explainers.md). The 10% daily late penalty remains. Canvas’s deadline field is authoritative.\n\n## Sources and generated copies\n\n[canvas-authority.json](canvas-authority.json) records the exported settings and source paths. Public assignment HTML/XML snapshots are in [canvas/assignment-sources](../canvas/assignment-sources/). Superseded local drafts are retained in the dated pantry backup; they are historical and are not generated as active assignments.\n\nRun `python3 scripts/build_course.py` to regenerate local HTML fragments and the importable course package. The builder uses the assignment metadata for actual points, due dates and submission types. Its default generated publication state remains unpublished. No live Canvas records are changed by building.\n'
(ROOT/'assignments/README.md').write_text(text.replace('(../assignments/','('))
schedule='# Fall 2026 assignment schedule\n\nSynchronized from the Fall 2026 Canvas export on October 14, 2026. All deadlines below are confirmed export values at 11:59:59 pm America/New_York; Canvas is the official source. The final’s new description is supplied separately by the instructor.\n\n'+table().replace('(../assignments/','(')+'\nThere is no additional unnumbered GDD assignment: the October 19, five-point GDD is Assignment 4. The earlier locally proposed October 25, November 13, November 23, December 3 and December 13 deadlines have been superseded. The pitch deadline is November 22 and the game-AI teaching assignment is December 12.\n\n## Release and preparation plan\n\nStart the final early and preserve preparation work in the existing project log. These are preparation targets, not additional graded submissions. Read the final brief alongside the October 19 GDD; identify the intended experience, scope, export target and risks. Use shader, particle and animation work to build the integrated game. Assignment 8 states the pitch promise; Assignment 9 supplies the game-AI technique and teaching projects; the final tests those against the complete game and reconciles each promised item as delivered, changed or dropped.\n\nThe exact requirements and the Canvas deadline for each assignment govern. The final’s 250 points replace the former local 100-point draft and the export’s older portfolio description.\n'
(ROOT/'assignments/fall-2026-assignment-schedule.md').write_text(schedule)
# Update all current course links, while leaving historical evidence and student work alone.
rename={'04-specify-and-build-a-3d-interaction.md':'04-create-a-game-design-document.md','05-shader-and-material.md':'05-shaders-materials-and-godot-shading-language.md','06-audit-a-shader-change.md':'06-creating-particle-effects.md','07-particle-effects.md':'07-doing-animation.md','08-animation-and-state.md':'08-final-project-pitch-film.md','09-audio-and-a-performance-budget.md':'09-teach-one-game-ai-technique.md'}
for folder in ['modules','prerequisites','chapters','canvas']:
 for p in (ROOT/folder).rglob('*.md'):
  if 'assignment-sources' in p.parts:continue
  old=p.read_text();new=old
  for a,b in rename.items():new=new.replace(a,b)
  if old!=new:p.write_text(new)
# Replace stale module-index assignment column with the current mapping.
p=ROOT/'modules/README.md';s=p.read_text();lines=[]
for line in s.splitlines():
 if re.match(r'\| \d+ \|',line):
  cells=line.split('|');num=int(cells[1].strip());matches=[r for r in rows if num in r['modules']]
  cells[-2]=' '+('; '.join(f"[A{r['number']}](../{r['source']})" for r in matches) or '—')+' ';line='|'.join(cells)
 lines.append(line)
p.write_text('\n'.join(lines)+'\n')
p=ROOT/'modules/00-start-here/course-map.md';s=p.read_text();start=s.index('Module order is the teaching sequence');end=s.index('## One game',start) if '## One game' in s[start:] else s.index('After Assignment 1',start)
new='Module order describes the learning sequence. The assignment sequence and its confirmed Canvas deadlines are below. The GDD is Assignment 4, the pitch is Assignment 8, and the final is 250 points.\n\n'+table()+'\nThe seven 100-point assignments follow their stated 60/10/10/20 rubrics. Assignment 8 uses 30/5/5/10; the final uses 150/25/25/50. Assignment 4 follows its five-point GDD requirements. Read [the assessment policy](../../prerequisites/assessment-policy.md) and each brief. Late work loses 10% per day.\n\n'
s=s[:start]+new+s[end:];s=s.replace(' 100 points.',' Points are stated in each assignment.');p.write_text(s)
p=ROOT/'prerequisites/assessment-policy.md';s=p.read_text();a=s.index('The ten numbered');b=s.index('| Component |',a);s=s[:a]+'''The active assignments match the Fall 2026 Canvas export supplied October 14, 2026 and the instructor’s pasted final project. There are seven 100-point assignments, Assignment 4 (GDD) at 5 points, Assignment 8 (pitch) at 50 points, and Assignment 10 (final) at 250 points: 1,005 points in total. The GDD is numbered Assignment 4, not a separate extra milestone. See the [confirmed schedule](../assignments/fall-2026-assignment-schedule.md).

The 100-point assignments use 60 / 10 / 10 / 20. The pitch uses 30 / 5 / 5 / 10. The final uses 150 / 25 / 25 / 50. Each allocation includes Relative Quartile in its stated total; the five-point GDD follows its own Canvas requirements. The table below is the regular 100-point example. Individual assignment rubrics are authoritative.

'''+s[b:];s=s.replace('Every numbered assignment draft includes an explainer video','The assignments that specify a film require it').replace('Every numbered assignment draft','Each assignment that requires it');p.write_text(s)
print('Updated assignment index, confirmed schedule, course map, module index and assessment policy.')

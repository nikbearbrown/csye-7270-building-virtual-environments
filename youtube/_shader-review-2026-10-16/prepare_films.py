#!/usr/bin/env python3
"""Prepare the authored, source-backed lecture packages. Does not generate audio or a film."""
from pathlib import Path
import json, shutil, hashlib, re
HERE=Path(__file__).resolve().parent
BOOK=HERE.parent.parent
TOOLKIT=BOOK.parent/'brutalist.art'
DATA=json.loads((HERE/'film-content.json').read_text())
SHADERS=sorted((HERE/'project-snapshot/shaders').glob('*.gdshader'))
GREETINGS=['Hola','Olá','Bonjour','Ciao','Hallo','Hej','Hei','Ahoj','Shalom','Salaam','Jambo','Namaste','Halo','Aloha','Merhaba','Selam']

def base(bid,act,narration):
 return {'beat_id':bid,'act':act,'lane':'bookend','proof_gate':'SHOW','narration_text':narration,'estimated_duration_s':round(len(narration.split())/2.4,2),'voice':'am_onyx','engine':'kokoro'}
def rem(bid,act,narration,pattern,props,events):
 b=base(bid,act,narration);b['shot']={'type':'REMOTION','source':'own','visual_intent':events[-1]['event'],'show':events,'motion_claim':events[-1]['event'],'remotion':{'pattern':pattern,'props':props}};return b

def build(d,reel):
 shader=SHADERS[d['id']];slug=reel.name;title=d['title'];asset='shader-lesson-captures/'+shader.stem
 lines=shader.read_text().splitlines();code=[(i+1,l) for i,l in enumerate(lines) if l.strip() and not l.lstrip().startswith('//')]
 B=[]
 b=base('BOPEN','Opening',f"Godot Shader Techniques. {title}. {d['objective']}")
 b['proof_gate']='CARD';b['shot']={'type':'GRAPHIC','source':'own','template':'lecture-title-slide-16x9','narration_contract':'playlist-title-summary-v1','motion':'hold','visual_intent':'Professor Bear portrait, title, narrator credit and learning payoff','show':[{'at':0,'event':'Complete portrait and title card visible immediately'}]};B.append(b)
 b=rem('BIDEA','Opening',f"{GREETINGS[d['id']]}. This is Liam, in for Bear. The key correction is that {d['right']}. We will trace the code, inspect its output, and test where the model stops working.",'BrutalistHesitantWriter',{'text':f"For this shader,\n{d['wrong']}.",'triggerWords':d['wrong'],'replacementWords':d['right'],'fontSize':64,'charMs':22,'seed':slug,'banner':''},[{'at':0,'event':'Type the initial misconception'},{'at':0.55,'event':'Correct the misconception to the actual shader behavior'}]);b['lead_silence_s']=0.8;b['qc']={'sparse_by_design':True,'sparse_reason':'The correction is the opening visual mechanism.'};B.append(b)
 narration='Three terms. '+' '.join(k+': '+v+'.' for k,v in d['terms'].items())
 B.append(rem('BDEFS','Opening',narration,'ClaudeDefinitions',{'title':'Terms In This Lecture','terms':[{'term':k,'meaning':v} for k,v in d['terms'].items()]},[{'at':i/3,'event':'Reveal '+k} for i,k in enumerate(d['terms'])]))
 source_rows=[]
 for j,(heading,keyword,narration) in enumerate(d['beats']):
  found=next((n for n,(ln,line) in enumerate(code) if keyword in line),None)
  if found is None: raise ValueError((shader.name,keyword))
  start=max(0,found-1);end=min(len(code),found+2)
  excerpt='\n'.join(line.split('//')[0].rstrip() for _,line in code[start:end]);target=found-start+1
  layout='video' if j==4 else ('side' if j in (1,3,6) else 'code')
  props={'title':('Trace The Model' if j==0 else 'Test The Model' if j==4 else heading),'videoAspect':(16/9 if j==4 else 1280/620),'layout':layout,'code':excerpt,'codeFile':shader.name+' (excerpt)','cues':[{'at':0,'lines':[]},{'at':0.18,'lines':[target]}], 'caption':'Godot · recorded evidence', 'videoLabel':'Controlled Godot demo' if j==4 else 'Godot output', 'video':asset+('.mp4' if j==4 else '.jpg')}
  if j==4:props['code']='';props['codeFile']='';props['cues']=[]
  events=[{'at':0,'event':('Act: Trace The Model. ' if j==0 else 'Act: Test The Model. ' if j==4 else '')+heading},{'at':0.18,'event':'Play the controlled parameter demonstration' if j==4 else 'Highlight the exact source expression: '+keyword}]
  b=rem(f'B{j+1:02d}','Trace The Model' if j<4 else 'Test The Model',narration,'ShaderLab',props,events);b['lane']='remotion';b['evidence']={'shader':str(shader),'sha256':hashlib.sha256(shader.read_bytes()).hexdigest(),'line':code[found][0],'numeric_review':str(HERE/'REVIEW.md')}
  if j==4:b['minimum_duration_s']=16.0;b['capture_duration_s']=16.0
  B.append(b);source_rows.append((b['beat_id'],heading,keyword,code[found][0],layout))
 recap='Let’s recap with Claude. '+' '.join(d['recap'])+' Liam, in for Bear.'
 b=rem('BVDT','Closing',recap,'ClaudeVerdictArtifact',{'artifactTitle':title,'artifactHeading':'What We Established','artifactLines':d['recap'],'lectureLayout':True},[{'at':0,'event':'Recap the source-backed mechanism'},{'at':0.5,'event':'Show remaining recap conclusions'}]);b['lead_silence_s']=0.5;B.append(b)
 prompt=d['exercise']+' Check two things: '+ ' '.join(d['checks'])
 B.append(rem('BHTF','Closing',prompt,'ClaudeComposerAsk',{'greeting':'Your turn.','largeText':True,'topic':'GODOT · YOUR TURN','segment':'Predict Then Test','command':prompt,'runningText':'Try this in Godot','output':d['checks'],'folderLabel':'@NikBearBrown'},[{'at':0,'event':'The complete exercise prompt types'},{'at':0.8,'event':'Reveal the two checks'}]))
 b=rem('BOUT','Closing',title+'. At Nik Bear Brown.','ClaudeTitleOutro',{'title':title,'slug':slug,'lectureLayout':True},[{'at':0,'event':'Exact title, @NikBearBrown and seeded mascot'}]);b['kind']='outro_voice';b['tail_silence_s']=1.0;B.append(b)
 sheet={'metadata':{'slug':slug,'title':title,'playlist':'Godot Shader Techniques','series_title':'Godot Shader Techniques','lecture_opening_description':d['objective'],'skill':'lecture','style_preset':'lecture','channel':'claude-liam','persona':'Liam (in for Bear)','voice_kokoro':'am_onyx','voice':'am_onyx','engine':'kokoro','palette':'claude','register':'Teardown','clock':'narration','fps':24,'aspect_ratio':'16:9','width':3840,'height':2160,'source_doc':str(shader),'caption_policy':'none','tags':['Godot','shaders','game development'],'status':'authored; audio and film rendering pending'},'beats':B}
 old=reel/'beat_sheet.json'
 if old.exists():
  previous={b['beat_id']:b for b in json.loads(old.read_text())['beats']}
  for b in B:
   p=previous.get(b['beat_id'],{})
   if p.get('narration_text')==b['narration_text']:
    for k in ['audio_file','actual_duration_s']:
     if k in p:b[k]=p[k]
 old.write_text(json.dumps(sheet,indent=2,ensure_ascii=False)+'\n')
 (reel/'NARRATION.md').write_text('# '+title+'\n\n'+'\n\n'.join('## '+b['beat_id']+'\n\n'+b['narration_text'] for b in B)+'\n')
 (reel/'ACTS.md').write_text('# '+title+'\n\nLearning objective: '+d['objective']+'\n\nOpening: portrait/title, corrected misconception, three prerequisites.\n\nAct — Trace The Model: B01–B04 introduce the inputs, coordinate/data contract and central calculation.\n\nAct — Test The Model: B05–B08 demonstrate a controlled change, examine the implementation and state its limitation.\n\nClosing: four-point recap, predictive exercise with two checks, Liam sign-off and exact-title outro.\n\nCast: the same sphere, torus, camera and generated textures throughout.\n\nCoverage: all executable source stages are assigned to the two acts. Existing lighting terms are summarized as prerequisites where they are not the target mechanism. LEFT OUT: copied-source historical comments, host metadata, unused terms, and unrelated engine features. No claim is made that this is a physically complete material.\n')
 (reel/'SHOTLIST.md').write_text('# Shot decisions\n\nLibrary queried: `art scenes "Godot shader code demo"`; ShaderLab, ClaudeDefinitions, ClaudeVerdictArtifact, BrutalistHesitantWriter and ClaudeTitleOutro confirmed renderable.\n\n| Beat | About | Selected | Alternative | Why |\n|---|---|---|---|---|\n'+'\n'.join(f'| {bid} | {h} | ShaderLab / {layout} | Manim conceptual diagram | '+('Actual controlled Godot output establishes the behavior.' if layout=='video' else 'The exact executed source is the artifact under discussion; line emphasis follows the spoken expression.')+' |' for bid,h,k,ln,layout in source_rows)+'\n\nSource examples are recorded evidence, not a fabricated editor session. Code-only beats progressively highlight exact expressions; side-by-side beats keep the output visible. Act names are attached to the first picture of each act. No speculative icons or generated footage.\n')
 (reel/'FACTCHECK.md').write_text('# Fact check\n\nSource hashes, fresh windowed tests and limitations: '+str(HERE/'REVIEW.md')+'\n\n| Beat | Claim | Verdict | Source | Fix |\n|---|---|---|---|---|\n'+'\n'.join(f'| {bid} | {h}; `{k}` | Source checked; numeric tests pass for supplied rig | `{shader}:{ln}` | Caveats stated in narration |' for bid,h,k,ln,layout in source_rows)+'\n\nPrimary API reference: https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html (checked 2026-10-16). All sample calculations follow the displayed code; measured screen values are deliberately omitted to avoid confusing renderer-specific transfer with model weights. The original Cg host behavior is not claimed as independently verified.\n')
 (reel/'SOURCES.md').write_text('# Sources\n\nReviewed shader: '+str(shader)+'\n\nOriginal project: '+str(BOOK/'shader_lessons_godot')+'\n\nProvenance: '+str(BOOK/'shader_lessons_godot/SOURCES.md')+'\n\nSnapshot, tests, capture program and logs: '+str(HERE)+'\n\nThe code is a conversion of third-party Eat 3D teaching material (credit Luiz); distribution terms remain unconfirmed. Local production only; no Git push, staging or publication is authorized. Generated test textures are code-authored by the existing project.\n')
 (reel/'PROMPTS.md').write_text('# Generation prompts\n\nNo paid or generative-media calls. Free local Kokoro narration and existing Remotion components. The Your Turn text is a proposed learner exercise, not a claim that a model executed it.\n')
 (reel/'CHECKS-REPORT.md').write_text('# Authoring checks\n\n8 body SHOW beats; 0 body HOLD; 0 unresolved body placeholders.\n\nFramework: B01–B04. Worked source/example: B03–B05. Falsifiability/limitation: B07–B08. Scaffolded task: BHTF, two explicit checks. Opening and closing bookends authored. Claims trace to source and the reproduced rig. Lane histogram: 8 ShaderLab body beats, 6 bookends.\n\nStatus: source and captures reviewed; final scene typography, cue alignment, audio, opening portrait layout, bookend timing and master QC remain build-stage checks. This is not a rendered-film PASS.\n')
 (reel/'BUILD-LOG.md').write_text('# Build log\n\n2026-10-16: authored from inspected shader source and 268 fresh passing numerical checks. Native Higgsfield was not used: the existing lecture format and actual Godot evidence are the working assumption pending any user correction. Separate film per shader; base and Lambert have different objectives despite identical code.\n\nCompact standalone treatment; estimated runtime is a planning aid, not a measured result. Audio-first production and final visual review remain pending. No audio or master generated in this preparation stage.\n')
 (reel/'make_sheet.py').write_text('''#!/usr/bin/env python3
import importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('shader_preparation',Path(%r)/'prepare_films.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
module.build(json.loads((HERE/'film-content.json').read_text()),HERE)
'''%str(HERE))
 (reel/'BUILD-PROMPT.md').write_text(f'''# Build {title}

Read the lecture skill at `{TOOLKIT}/skills/make/lecture/SKILL.md`, this film's ACTS, SHOTLIST, FACTCHECK, SOURCES, CHECKS-REPORT and the shared REVIEW. This is a local film build, never a publication. Do not change the narration or source shader to make a gate pass.

Prepared: complete 14-beat sheet, narration, registered ShaderLab and bookend scenes, actual Godot capture, source excerpts and hash-linked evidence. No new scene registration is needed. The source snapshot is preserved. No audio or master has been built.

Run from books/ in this order:

```bash
python3 '{HERE}/install_assets.py'
python3 '{TOOLKIT}/runtime/scripts/generate_audio_kokoro.py' '{reel}'
python3 '{HERE}/lock_audio.py' '{reel}'
python3 '{TOOLKIT}/skills/make/lecture/templates/title-slide-16x9/build.py' --out '{reel}/opening' --sheet '{reel}/beat_sheet.json' --width 3840
```

Copy the generated video-only opening MP4 into `{reel}/media/BOPEN.mp4` (the title builder emits its measured-duration filename). Before any long render, render low-resolution component stills at 15/50/85 percent, inspect every frame, and log layout findings. The body uses the registered ShaderLab component. All excerpts are actual source. B05's 16-second capture MUST play completely; its audio is padded to at least 16 seconds by lock_audio.py. If narration exceeds the capture, use a freshly captured longer version with the same controls, not a freeze or a loop of an irreversible parameter change. Reposition B05's visual transition relative to the voice only through a documented capture timing change; do not imply that unsynchronized audio has been checked.

Align code highlight cues with actual spoken references after generating word timestamps. Preserve source code and the authored explanation. The original Godot caption remains inside the capture; confirm it clears type limits at final size. Use larger source crops or the full-width layout if needed, without hiding evidence. Ordinary code strings are code, not improperly typeset equations.

```bash
./brutalist.art/art run '{reel}' --height 2160
./brutalist.art/art final '{reel}' --height 2160 --out '{reel}/exports/landscape'
python3 '{TOOLKIT}/runtime/scripts/bookend_check.py' '{reel}'
```

Run every normal gate including factual, static, layout, visual, type and sharpness checks. Inspect the master, not just its file probe. Hear/transcribe the opening, scientific terms and ending; verify the explicit silence, no truncation, and exact title/handle. Required values: 3840×2160, measured audio clock, no unresolved placeholders, one-second silent outro tail. No paid services and no gate bypasses.

Only 25 GiB was free during preparation: check free space before each film and build serially. Do not delete other files or interfere with the Wikipedia build. Do not stage, push or publish. Report the exact final path and measured runtime only after the master and all applicable gates pass; otherwise report the precise incomplete gate.
''')
 return sheet

def main():
 manifest=[]
 for d in DATA:
  reel=BOOK/'youtube'/('claude-liam-lecture-shader-'+d['slug']);reel.mkdir(exist_ok=True)
  (reel/'film-content.json').write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
  sheet=build(d,reel)
  manifest.append({'shader':SHADERS[d['id']].name,'title':d['title'],'reel':str(reel),'words':sum(len(b['narration_text'].split()) for b in sheet['beats']),'status':'authored; render pending'})
 (HERE/'film-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(json.dumps(manifest,indent=2))
if __name__=='__main__':main()

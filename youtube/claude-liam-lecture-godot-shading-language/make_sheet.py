#!/usr/bin/env python3
"""Assemble the lecture; preserve measured audio when narration is unchanged."""
from pathlib import Path
import json, shutil
from PIL import Image
R=Path(__file__).resolve().parent
C=json.loads((R/'content.json').read_text())
TITLE=C['title']; SLUG=R.name; COURSE='CSYE 7270 Building Virtual Environments'
PUBLIC=R.parents[2]/'brutalist.art/runtime/remotion/public'/SLUG
PUBLIC.mkdir(parents=True,exist_ok=True)
for p in (R/'captures').glob('*.png'): shutil.copy2(p,PUBLIC/p.name)
old={b['beat_id']:b for b in json.loads((R/'beat_sheet.json').read_text())['beats']} if (R/'beat_sheet.json').exists() else {}
def base(bid,act,text,lane='bookend',gate='SHOW'):
 b={'beat_id':bid,'act':act,'lane':lane,'proof_gate':gate,'narration_text':text,'estimated_duration_s':round(max(3,len(text.split())/2.6),2),'voice':'am_onyx','engine':'kokoro','persona':'liam'}
 if old.get(bid,{}).get('narration_text')==text:
  for k in ['audio_file','actual_duration_s']:
   if k in old[bid]: b[k]=old[bid][k]
 return b
def rem(b,pattern,props,motion):
 duration=b.get('actual_duration_s',b['estimated_duration_s'])
 props={**props,'durationSeconds':duration}
 b['shot']={'type':'REMOTION','source':'own','visual_intent':motion,'motion_claim':motion,'show':[{'at':0,'event':'Establish the artifact'},{'at':0.22,'event':motion}], 'remotion':{'pattern':pattern,'props':props}}
 return b
B=[]
b=base('BOPEN','Opening','CSYE seventy-two seventy, Building Virtual Environments. Godot Shading Language. Learn to turn coordinates and material inputs into effects you can predict and test.',gate='CARD')
b['shot']={'type':'CARD','source':'own','template':'lecture-title-slide-16x9','narration_contract':'playlist-title-summary-v1','motion':'hold','visual_intent':'Professor Bear portrait, course and exact title visible immediately','show':[{'at':0,'event':'Complete portrait/title card holds for measured narration'}]}
B.append(b)
b=base('BIDEA','Opening','Hallo. This is Liam, in for Bear, for CSYE seventy-two seventy, Building Virtual Environments. Shaders compute from their inputs. Once you can predict those inputs, the language starts to make sense.')
b['lead_silence_s']=0.8
b['qc']={'sparse_by_design':True,'sparse_reason':'Mandated hesitant writer bookend; the phrase correction carries the idea.'}
B.append(rem(b,'BrutalistHesitantWriter',{'text':'Shaders remember the last pixel','triggerWords':'remember the last pixel','replacementWords':'compute from their inputs','fontSize':68,'charMs':25,'hesitateBetween':6,'hesitateWithin':1,'mistakeRate':4,'jitter':20,'seed':SLUG,'banner':''},'Type the misconception, then replace the whole phrase'))
terms=[('GPU','Processor for parallel graphics work.'),('Vertex','A geometry point with attributes.'),('Fragment','A candidate contribution to a pixel.'),('Material','Surface settings, including a shader.'),('UV','Coordinates used to address a texture.')]
b=base('BDEFS','Opening','Five terms. G P U: the processor doing parallel graphics work. A vertex is a geometry point. A fragment is a candidate contribution to a pixel. A material describes a surface. U V coordinates address a texture.',gate='CARD')
B.append(rem(b,'ClaudeDefinitions',{'title':'Terms In This Lecture','terms':[{'term':t,'meaning':v} for t,v in terms],'folderLabel':'@NikBearBrown'},'Definitions arrive in spoken order'))
urls={x['name']:x['requested_url'] for x in json.loads((R/'evidence/web-captures.json').read_text())}
previous_act=-1
for row in C['body']:
 act=C['acts'][row['act']]
 if row['act']!=previous_act:
  div=base(f"BACT{row['act']+1}",act,act+'.',lane='card',gate='CARD')
  B.append(rem(div,'FormACard',{'lines':[act],'dark':False},'Act title arrives and holds'))
  previous_act=row['act']
 b=base(row['id'],act,row['narration'],row['lane'])
 b['lecture']={'about':row['topic'],'runner_up':row['runner_up'],'why':row['why']}
 asset=row['asset'];lane=row['lane']
 if lane=='manim':
  b['shot']={'type':'GRAPHIC','source':'own','visual_intent':row['topic'],'motion_claim':row['motion'],'show':[{'at':0,'event':'Establish the persistent objects'},{'at':0.25,'event':row['motion']},{'at':0.75,'event':'Hold the resulting relationship'}],'manim':{'class':row['id']+'_'+asset}}
 elif lane=='capture':
  p=R/'captures'/f'{asset}.png';w,h=Image.open(p).size
  isdoc=asset.startswith('docs-')
  # Explicit per-artifact focal points, not a generic arbitrary pan.
  if asset=='godot-editor': moves=[{'at':0,'x':0.2,'y':0.16,'scale':1},{'at':0.22,'x':0.94,'y':0.75,'scale':2.6,'ring':[0.84,0.7,0.14,0.085]}]
  elif asset=='uv': moves=[{'at':0,'x':0.5,'y':0.5,'scale':1},{'at':0.2,'x':0.3,'y':0.27,'scale':1.7},{'at':0.68,'x':0.6,'y':0.73,'scale':1.7}]
  elif asset in ['unique','shared']: moves=[{'at':0,'x':0.5,'y':0.5,'scale':1},{'at':0.22,'x':0.27,'y':0.5,'scale':1.15},{'at':0.68,'x':0.73,'y':0.5,'scale':1.15}]
  elif asset=='flash': moves=[{'at':0,'x':0.5,'y':0.5,'scale':1},{'at':0.22,'x':0.5,'y':0.55,'scale':1.12,'ring':[0.35,0.24,0.28,0.53]}]
  elif isdoc:
   focus={'book':(0.38,0.73),'community':(0.53,0.64),'visual':(0.51,0.76),'compute':(0.5,0.5),'first2d':(0.52,0.3)}.get(asset[5:],(.5,.4))
   moves=[{'at':0,'x':0.5,'y':0.5,'scale':1},{'at':0.22,'x':focus[0],'y':focus[1],'scale':1.7}]
  else: moves=[{'at':0,'x':0.5,'y':0.5,'scale':1},{'at':0.22,'x':0.45,'y':0.48,'scale':1.4}]
  props={'image':f'{SLUG}/{asset}.png','imageAspect':w/h,'frame':'browser' if isdoc else 'app','url':urls.get(asset[5:],'') if isdoc else '', 'caption':('Public page' if isdoc else 'Real Godot capture')+' · 13 Oct 2026','moves':moves,'moveSeconds':0.8}
  rem(b,'BrowserCapture',props,row['motion'])
 elif lane=='code':
  if asset=='hints':
   code='uniform int mode : hint_enum("Off", "Tint", "Mask") = 0;\n\n// GDScript, from the executed lab:\nshared.set_shader_parameter("amount", 7.0)\n// Recorded: CHECK hint_range stores 7.0'
   title='uniform.gdshader + lab.gd (excerpts)'; language='Shader / GDScript'
  elif asset=='switch_excerpt':
   code='switch (mode) {\n    case 1: value = 0.25; break;\n    case 2: value = 0.75; break;\n    default: value = 0.1; break;\n}'
   title='switch.gdshader (fragment excerpt)';language='Godot Shader'
  else:
   code=(R/'godot/shaders'/f'{asset}.gdshader').read_text().strip()
   title=f'{asset}.gdshader';language='Godot Shader'
   if asset=='uniform':code='\n'.join(code.splitlines()[:4]);title+=' (declarations)'
   if asset=='instance':
    code+='\n// GDScript, on the drawable node:\nleft.set_instance_shader_parameter("tint", Color(0.85,0.25,0.12,1))'
    title='instance.gdshader + lab.gd (excerpts)';language='Shader / GDScript'
  cues=[0]*len(code.splitlines())
  d=b.get('actual_duration_s',b['estimated_duration_s'])
  for i in range(1,len(cues)): cues[i]=int((0.06+0.30*i/max(1,len(cues)-1))*d*24)
  rem(b,'ClaudeCodeBeat',{'title':title,'code':code,'sparkLine':row['topic'],'language':language,'largeText':True,'brandLabel':'@NikBearBrown','lineCues':cues},row['motion'])
  b['code_evidence']='godot/shaders/'+asset+'.gdshader' if (R/'godot/shaders'/f'{asset}.gdshader').exists() else 'godot/lab.gd'
 elif lane=='shell':
  if asset=='negative':
   log=(R/'evidence/negative-type.log').read_text()
   diagnostic=next(x for x in log.splitlines() if x.startswith('SHADER ERROR:'))
   lines=['# Recorded Godot diagnostic · negative.gd','float gain = 5;',diagnostic,'# Fix in scalars.gdshader: float(count)']
  else: lines=(R/'evidence/verification.txt').read_text().splitlines()
  rem(b,'CCPlainShell',{'title':'Recorded local evidence · Godot shader lab','lines':lines[:12],'fontSize':32,'lineGap':30,'durationSeconds':b.get('actual_duration_s',b['estimated_duration_s'])},row['motion'])
 B.append(b)
recap=['Choose the shader type and the output for its stage.','Compute from coordinates and inputs, not the previous pixel.','Match scalar types, vector sizes, and matrix columns.','Know whether a value belongs to a material or an instance.','Pass varyings deliberately and keep control flow bounded.','Predict, render, compare, then judge the effect in context.']
b=base('BVDT','Closing',"Let's recap with Claude. For CSYE seventy-two seventy, Building Virtual Environments. "+' '.join(recap));b['lead_silence_s']=0.5
B.append(rem(b,'ClaudeVerdictArtifact',{'artifactTitle':'Recap','artifactHeading':'A Shader You Can Explain','artifactLines':recap,'lectureLayout':True,'brandLabel':'@NikBearBrown'},'Recap pages arrive two statements at a time'))
prompt='Help me build a Godot canvas item tint shader. Preserve incoming alpha and expose a color plus an amount from zero to one. Predict the output at zero, one half, and one. Explain how two objects can have independent amounts. Give me the shader, a minimal test scene, and checks that distinguish parsing from rendered appearance.'
b=base('BHTF','Closing',prompt)
B.append(rem(b,'ClaudeComposerAsk',{'greeting':'Your turn.','topic':'CLAUDE · YOUR TURN','segment':'Build and Test a Tint','command':prompt,'runningText':'paste this into Claude…','output':['Check: 0 preserves the base; 1 reaches the tint; alpha is unchanged.','Check: change one object; the other keeps its own amount.'],'folderLabel':'@NikBearBrown'},'Prompt types in full; two learner checks appear'))
b=base('BOUT','Closing',TITLE+'. At Nik Bear Brown.');b['kind']='outro_voice';b['tail_silence_s']=1.0
B.append(rem(b,'ClaudeTitleOutro',{'title':TITLE,'slug':SLUG,'lectureLayout':True},'Exact title, channel handle and seeded crisp mascot'))
meta={'slug':SLUG,'title':TITLE,'skill':'lecture','style_preset':'lecture','channel':'claude-liam','channel_title':'@NikBearBrown','persona':'Liam (in for Bear)','voice':'am_onyx','voice_kokoro':'am_onyx','engine':'kokoro','register':'Teardown','clock':'narration','palette':'claude','fps':24,'width':3840,'height':2160,'aspect_ratio':'16:9','caption_policy':'sidecar','course':COURSE,'playlist':COURSE,'series_title':COURSE,'lecture_opening_description':'Predict, build, and test a visible effect','lecture_opening_title_lines':['Godot Shading','Language'],'lecture_opening_template':'lecture-title-slide-16x9','source_doc':str(R/'sources/user-transcript.txt'),'audience':'Beginning shader programmers in CSYE 7270 and independent Godot learners','tags':['Godot','shaders','CSYE 7270','Building Virtual Environments','GLSL','uniforms'],'bookend_exempt':['cold-open'],'bookend_exempt_reason':'Lecture opens with a narrated portrait/title, writer, and terms; recap is present.'}
(R/'beat_sheet.json').write_text(json.dumps({'metadata':meta,'beats':B},indent=2)+'\n')
(R/'NARRATION.md').write_text('# '+TITLE+'\n\n'+ '\n\n'.join('## '+b['beat_id']+' · '+b['act']+'\n\n'+b['narration_text'] for b in B)+'\n')
print(len(B),'beats;',sum(len(b['narration_text'].split()) for b in B),'words; estimated',round(sum(b['estimated_duration_s'] for b in B)),'seconds (unmeasured)')

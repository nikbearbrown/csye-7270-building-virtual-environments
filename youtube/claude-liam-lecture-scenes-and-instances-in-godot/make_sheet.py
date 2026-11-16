#!/usr/bin/env python3
from pathlib import Path
import json,shutil
from PIL import Image
R=Path(__file__).resolve().parent;C=json.loads((R/'content.json').read_text())
TITLE=C['title'];SLUG=R.name;COURSE='CSYE 7270 Building Virtual Environments'
PUBLIC=R.parents[2]/'brutalist.art/runtime/remotion/public'/SLUG;PUBLIC.mkdir(parents=True,exist_ok=True)
for p in (R/'captures').glob('*.png'):shutil.copy2(p,PUBLIC/p.name)
old={b['beat_id']:b for b in json.loads((R/'beat_sheet.json').read_text())['beats']} if (R/'beat_sheet.json').exists() else {}
def base(bid,act,s,lane='bookend',gate='SHOW'):
 b={'beat_id':bid,'act':act,'lane':lane,'proof_gate':gate,'narration_text':s,'estimated_duration_s':round(max(3,len(s.split())/2.6),2),'voice':'am_onyx','engine':'kokoro','persona':'liam'}
 if old.get(bid,{}).get('narration_text')==s:
  for k in ['audio_file','actual_duration_s']:
   if k in old[bid]:b[k]=old[bid][k]
 return b
def rem(b,pattern,props,motion):
 b['shot']={'type':'REMOTION','source':'own','visual_intent':motion,'motion_claim':motion,'show':[{'at':0,'event':'Establish artifact'},{'at':.22,'event':motion}],'remotion':{'pattern':pattern,'props':{**props,'durationSeconds':b.get('actual_duration_s',b['estimated_duration_s'])}}};return b
B=[]
b=base('BOPEN','Opening','CSYE seventy-two seventy, Building Virtual Environments. '+TITLE+'. '+C['summary'],gate='CARD');b['shot']={'type':'CARD','source':'own','template':'lecture-title-slide-16x9','narration_contract':'playlist-title-summary-v1','motion':'hold','visual_intent':'Complete course, exact title, Professor Bear portrait and Liam credit visible immediately','show':[{'at':0,'event':'Hold complete portrait/title for measured speech'}]};B.append(b)
b=base('BIDEA','Opening',C['intro']);b['lead_silence_s']=.8;b['qc']={'sparse_by_design':True,'sparse_reason':'Mandated writer bookend: the phrase correction carries the distinction.'}
B.append(rem(b,'BrutalistHesitantWriter',{'text':C['framing'],'triggerWords':C['trigger'],'replacementWords':C['replacement'],'fontSize':65,'charMs':25,'hesitateBetween':6,'hesitateWithin':1,'mistakeRate':4,'jitter':20,'seed':SLUG,'banner':''},'Type the mistaken framing and replace its final phrase'))
terms=C['terms']
b=base('BDEFS','Opening',' '.join(t+'. '+m for t,m in terms),gate='CARD');B.append(rem(b,'ClaudeDefinitions',{'title':'Terms In This Lecture','terms':[{'term':t,'meaning':m} for t,m in terms],'folderLabel':'@NikBearBrown'},'Terms arrive in spoken order'))

web={x['name']:x for x in json.loads((R/'evidence/web-captures.json').read_text())}
logs=(R/'evidence/rendered-lab.log').read_text().splitlines();extra=(R/'evidence/supplemental.log').read_text().splitlines()
shells={
'version':[next(x for x in logs if x.startswith('ENGINE '))]+[x for x in (R/'godot/project.godot').read_text().splitlines() if x.startswith('config/features')],
'masks':[x for x in logs if any(t in x for t in ['area detects','zero mask'])],
'latch':[x for x in logs if any(t in x for t in ['area detects','coin latch'])],
'results':(R/'evidence/verification.txt').read_text().splitlines(),
'audit':(R/'evidence/audit.txt').read_text().splitlines()}
for p in (R/'evidence').glob('*.txt'):
 shells.setdefault(p.stem,p.read_text().splitlines())
previous=-1
for row in C['body']:
 act=C['acts'][row['act']]
 if row['act']!=previous:
  b=base(f"BACT{row['act']+1}",act,act if act.endswith(('?','!','.')) else act+'.','card','CARD');B.append(rem(b,'FormACard',{'lines':[act],'dark':False},'Act title arrives and holds'));previous=row['act']
 b=base(row['id'],act,row['narration'],row['lane']);b['lecture']={'about':row['topic'],'runner_up':row['runner_up'],'why':row['why']};asset=row['asset']
 if row['lane']=='manim':
  b['shot']={'type':'GRAPHIC','source':'own','visual_intent':row['topic'],'motion_claim':row['motion'],'show':[{'at':0,'event':'Establish persistent geometry'},{'at':.25,'event':row['motion']},{'at':.75,'event':'Hold result'}],'manim':{'class':row['id']+'_'+asset}}
 elif row['lane']=='capture':
  p=R/'captures'/f'{asset}.png';w,h=Image.open(p).size;isdoc=asset.startswith('docs-')
  if isdoc:
   focus={'character':(.51,.43),'rigid':(.5,.43),'oneway':(.51,.43),'migration':(.5,.5),'jolt':(.48,.43),'physics':(.5,.6)}.get(asset[5:],(.5,.4));moves=[{'at':0,'x':.5,'y':.5,'scale':1},{'at':.22,'x':focus[0],'y':focus[1],'scale':1.8}]
  else:
   focus={'coin':(.38,.49),'crate':(.45,.68),'tiles':(.39,.48),'sweep':(.44,.57)}.get(asset,(.5,.5));moves=[{'at':0,'x':.5,'y':.5,'scale':1},{'at':.22,'x':focus[0],'y':focus[1],'scale':1.45},{'at':.70,'x':.43,'y':.24,'scale':1.3}]
  if asset.startswith('comparison-'):moves=[{'at':0,'x':.5,'y':.5,'scale':1},{'at':.22,'x':.47,'y':.36,'scale':1.25},{'at':.70,'x':.52,'y':.70,'scale':1.25}]
  if asset.startswith('door-'):moves=[{'at':0,'x':.5,'y':.5,'scale':1},{'at':.22,'x':.6,'y':.52,'scale':1.35},{'at':.70,'x':.45,'y':.78,'scale':1.18}]
  props={'image':f'{SLUG}/{asset}.png','imageAspect':w/h,'frame':'browser' if isdoc else 'app','url':web[asset[5:]]['resolved_url'] if isdoc else '', 'caption':('Official documentation' if isdoc else 'Real engine capture · scripted experiment')+' · 14 Oct 2026','moves':moves,'moveSeconds':.8}
  rem(b,'BrowserCapture',props,row['motion'])
 elif row['lane']=='code':
  code=(R/'excerpts'/f'{asset}.txt').read_text().strip();d=b.get('actual_duration_s',b['estimated_duration_s']);n=len(code.splitlines());cues=[0 if i==0 else round((.08+.28*i/max(1,n-1))*d*24) for i in range(n)]
  rem(b,'ClaudeCodeBeat',{'title':('Official 4.7 migration guide · quoted excerpts' if asset=='migration_excerpt' else 'Door hierarchy · derived from saved scene' if asset=='door-tree' else asset+' · source excerpt'),'code':code,'sparkLine':row['topic'],'language':('Official documentation' if asset=='migration_excerpt' else 'Project conventions' if asset=='conventions' else 'Derived scene hierarchy' if asset=='door-tree' else 'Selected source lines' if asset=='contact-monitor' else 'Godot / GDScript'),'largeText':True,'brandLabel':'@NikBearBrown','lineCues':cues},row['motion']);b['code_evidence']='excerpts/'+asset+'.txt'
 elif row['lane']=='shell':rem(b,'CCPlainShell',{'title':'Recorded local evidence · Godot lab','lines':shells[asset],'fontSize':32,'lineGap':34},row['motion'])
 B.append(b)
recap=C['recap']
b=base('BVDT','Closing',"Let's recap with Claude. For CSYE seventy-two seventy, Building Virtual Environments. "+' '.join(recap));b['lead_silence_s']=.5;B.append(rem(b,'ClaudeVerdictArtifact',{'artifactTitle':'Recap','artifactHeading':'What You Can Now Explain','artifactLines':recap,'lectureLayout':True,'brandLabel':'@NikBearBrown'},'Recap arrives two statements at a time'))
prompt=C['prompt']
b=base('BHTF','Closing',prompt);B.append(rem(b,'ClaudeComposerAsk',{'greeting':'Your turn.','topic':'CLAUDE · YOUR TURN','segment':'Build a Testable Room','command':prompt,'runningText':'paste this into Claude…','output':C['checks'],'folderLabel':'@NikBearBrown'},'Full prompt types; two learner checks arrive'))
b=base('BOUT','Closing',TITLE+'. At Nik Bear Brown.');b['kind']='outro_voice';b['tail_silence_s']=1.0;B.append(rem(b,'ClaudeTitleOutro',{'title':TITLE,'slug':SLUG,'lectureLayout':True},'Exact title, handle and seeded mascot'))
meta={'slug':SLUG,'title':TITLE,'skill':'lecture','style_preset':'lecture','channel':'claude-liam','channel_title':'@NikBearBrown','persona':'Liam (in for Bear)','voice':'am_onyx','voice_kokoro':'am_onyx','engine':'kokoro','register':'Teardown','clock':'narration','palette':'claude','fps':24,'width':3840,'height':2160,'aspect_ratio':'16:9','caption_policy':'sidecar','course':COURSE,'playlist':COURSE,'series_title':COURSE,'lecture_opening_description':C['description'],'lecture_opening_title_lines':C['title_lines'],'lecture_opening_template':'lecture-title-slide-16x9','source_doc':str(R/'sources/research-notes.txt'),'audience':'CSYE 7270 students and independent Godot beginners','tags':['Godot','scenes','collision','physics','CSYE 7270','Building Virtual Environments'],'bookend_exempt':['cold-open'],'bookend_exempt_reason':'Lecture portrait/title opening replaces composer cold open.'}
(R/'beat_sheet.json').write_text(json.dumps({'metadata':meta,'beats':B},indent=2)+'\n')
(R/'NARRATION.md').write_text('# '+TITLE+'\n\n'+ '\n\n'.join('## '+b['beat_id']+' · '+b['act']+'\n\n'+b['narration_text'] for b in B)+'\n')
print(len(B),'beats;',sum(len(b['narration_text'].split()) for b in B),'words; estimated',round(sum(b['estimated_duration_s'] for b in B)),'seconds (unmeasured)')

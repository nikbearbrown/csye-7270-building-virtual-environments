from pathlib import Path
import json,sys,shutil
ROOT=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube')
WORK=Path(__file__).resolve().parent
PLAYLIST='Particle Systems and VFX in Godot'
def act(label, text, actions, focus='viewport'):
 return dict(act=label,narration=text,actions=actions,focus=focus)
def setp(prop,v,node='.',**kw):return dict(op='set',property=prop,value=v,node=node,**kw)
def call(method,**kw):return dict(op='call',method=method,**kw)
def at(t,**kw):return dict(at=t,**kw)
def script(line):return dict(op='script',path='res://particle_system.gd',line=line)
def author(d):
 r=ROOT/d['slug']/'redo-2026-10-23';r.mkdir(parents=True,exist_ok=True)
 metadata=dict(slug=d['slug']+'-redo',title=d['title'],channel='claude-liam',channel_title='@NikBearBrown',engine='kokoro',voice='am_onyx',voice_kokoro='am_onyx',register='Teardown',skill='lecture',style_preset='lecture',aspect_ratio='16:9',fps=30,series_title=PLAYLIST,lecture_opening_description=d['payoff'])
 def rem(bid,nar,pattern,props,**kw):return dict(beat_id=bid,narration_text=nar,lane='bookend',proof_gate='CARD',shot=dict(type='REMOTION',source='own',motion='component animation',remotion=dict(pattern=pattern,props=props)),**kw)
 beats=[dict(beat_id='BOPEN',act='Opening',lane='bookend',proof_gate='CARD',narration_text=PLAYLIST+'. '+d['title']+'. '+d['summary'],shot=dict(type='CARD',source='own',template='lecture-title-slide-16x9',narration_contract='playlist-title-summary-v1',motion='hold')),
 rem('BIDEA','Hallo. This is Liam, in for Bear. '+d['framing'],'BrutalistHesitantWriter',dict(text=d['question'],triggerWords=d['trigger'],replacementWords=d['replacement'],fontSize=72,charMs=26,hesitateBetween=7,hesitateWithin=1,mistakeRate=5,jitter=20,seed=d['slug']),lead_silence_s=.8,qc=dict(sparse_by_design=True,sparse_reason='The required hesitant writer corrects one misconception; deliberate sparse bookend.')),
 rem('BDEFS',' '.join(t['term']+'. '+t['meaning']+'.' for t in d['terms']),'ClaudeDefinitions',dict(title='Terms In This Lecture',terms=d['terms'],durationSeconds=18))]
 for i,b in enumerate(d['body'],1):
  beats.append(dict(beat_id=f'B{i:02}',act=b['act'],lane='capture',proof_gate='SHOW',lead_silence_s=1.2,narration_text=b['narration'],shot=dict(type='CAPTURE',source='capture',motion='Genuine native editor actions and particles at original speed',visual_intent=b['act']),capture_actions=b['actions'],capture_focus=b.get('focus','viewport')))
 recap=d['recap']
 beats += [rem('BVDT',"Let's recap with Claude. "+' '.join(recap),'ClaudeVerdictArtifact',dict(artifactTitle='What The Editor Demonstrated',artifactHeading='The Useful Part',artifactLines=recap,lectureLayout=True,brandLabel='@NikBearBrown'),lead_silence_s=.5),
 rem('BHTF',d['prompt'],'ClaudeComposerAsk',dict(greeting='Your turn.',topic='YOUR TURN · PARTICLE LAB',segment='Build, Change, Check',command=d['prompt'],output=d['checks'],runningText='Your next experiment',largeText=True,animateTyping=False,modelLabel='Your local project',effortLabel='One change')),
 rem('BSIGN',"This is Liam, in for Bear. Keep the version that survives the test.",'ClaudeTitleOutro',dict(title=d['title'],slug=d['slug'],lectureLayout=True)),
 rem('BOUT',d['title'].rstrip('.?')+('?' if d['title'].endswith('?') else '.')+' At Nik Bear Brown.','ClaudeTitleOutro',dict(title=d['title'],slug=d['slug'],lectureLayout=True),kind='outro_voice',tail_silence_s=1.0)]
 sheet={'metadata':metadata,'beats':beats};(r/'beat_sheet.json').write_text(json.dumps(sheet,indent=2))
 (r/'lesson-plan.json').write_text(json.dumps(d,indent=2))
 (r/'ACTS.md').write_text('# Source coverage and acts\n\n'+d['coverage']+'\n\n'+'\n'.join(f"- B{i:02} · {b['act']} · {b['narration']}" for i,b in enumerate(d['body'],1))+'\n\nLEFT OUT: Source publication histories, paid tools and external submissions. No topic is replaced with footage from a different project.\n')
 (r/'SCRIPT.md').write_text('\n\n'.join('## '+b['beat_id']+'\n\n'+b['narration_text'] for b in beats)+'\n')
 (r/'SHOTLIST.md').write_text('# Beat-level visual work order\n\nNative Godot is the body lane. A reconstruction was auditioned and rejected because it cannot prove an actual edit. A diagram was considered for motion and lifetime; the original runnable visualization supplies actual state and visible consequences. Bookends use the registered lecture components.\n\n'+'\n'.join(f"- {b['beat_id']} · {b['proof_gate']} · {b.get('act','Lecture bookend')} · {b['shot']['motion']} · {b['shot'].get('remotion',{}).get('pattern',b['shot']['type'])}" for b in beats)+'\n')
 (r/'FACTCHECK.md').write_text('# Claim ledger\n\n'+d['facts']+'\n\nEnvironment: Godot 4.7.2 stable on Apple M4 Pro, Compatibility renderer unless specifically recorded otherwise. Scripted native EditorPlugin actions, not human mouse input. No real-time performance claim follows from screen or movie capture.\n\nEach action receipt records observed property values. Visual inspection remains required: a state assertion does not establish that particles can be seen.\n')
 (r/'SOURCES.md').write_text('# Sources\n\n'+d.get('sources','Original teaching source authored for this redo. Course chapter: /Users/bear/Downloads/seis-course-publish/chapters/09-particle-effects.md. Official Godot class documentation for GPUParticles2D, GPUParticles3D, ParticleProcessMaterial and EditorInterface.')+'\n\nPlans read: SERIES-PLAN.md, SOURCE-NOTES.md, PRODUCTION-HANDOFF.md and OVERNIGHT-BUILD.md under /Users/bear/Downloads/seis-course-publish/youtube/particle-effects-series-plan/.\n')
 (r/'RECORDING-PLAN.md').write_text('# Genuine editor recording\n\nWindow-only macOS screencapture records the actual Godot editor. A project-local EditorPlugin selects real nodes/resources, applies undoable properties and opens the actual GDScript editor. Every scripted operation is labeled in the native toolbar and logged. Native media is retained without retiming; editorial crops only remove window shadow or focus genuine pixels. No reconstructed editor is used.\n\nCapture actions and offsets are in beat_sheet.json. Body narration begins after a measured 1.2 second lead so the visible operation leads the explanation. The source clips are cut at original speed to the measured narration clock.\n')
 (r/'PROMPTS.md').write_text('# Production prompts\n\nNo paid generation. No generated editor imagery. All body slots require native Godot footage of the actual source. BOPEN uses the approved seeded portrait template. BIDEA/BDEFS/BVDT/BHTF/BOUT use registered components with film-specific props.\n')
 (r/'BUILD-LOG.md').write_text('# Redo build log\n\n2026-10-23. Old root films preserved. The 18.5-second native editor pilot passed Gate V after safe framing; Amount 40→160 and Lifetime 2→1 demonstrated in real Godot. Original full-window source and failed first gate retained. No human viewing/listening approval is claimed.\n')
 (r/'QC.md').write_text('# Pending validation\n\nNot ready for review until the complete narrated MP4 and act samples are checked.\n')
 shutil.copy2(__file__,r/'make_sheet.py')
 print(r)
 return r
if __name__=='__main__':author(json.loads(Path(sys.argv[1]).read_text()))

from pathlib import Path
import shutil,json,argparse
from make_film3 import b,view,proc,draw,setp,at
W=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--suffix',default='');args=ap.parse_args()
tag=('-'+args.suffix) if args.suffix else ''
assert all(c.isalnum() or c in '-_' for c in tag)
r=W/('film3-pilot'+tag);w=W/('work-3-pilot'+tag)
if r.exists() or w.exists():raise SystemExit('Pilot exists; inspect instead of overwriting')
shutil.copytree(W/'work-3',w,ignore=shutil.ignore_patterns('.godot','request.json','actions.jsonl'))
r.mkdir()
(w/'.godot/editor').mkdir(parents=True,exist_ok=True)
(w/'.godot/editor/project_metadata.cfg').write_text('[game_view]\nembed_on_play=true\nmake_floating_on_play=false\nembed_size_mode=1\n')
pre=[]
for row in b[:5]:
 for action in row['actions']:pre.append({k:v for k,v in action.items() if k!='at'})
pre.append(view())
(r/'pre_capture_actions.json').write_text(json.dumps(pre,indent=2))
beats=[]
def add(name,actions,d=12):beats.append(dict(beat_id=name,act=name,actual_duration_s=d,capture_actions=actions))
add('mesh_orbit',[view(45,True)])
add('vertex_alpha',[view(),proc('color_ramp',{'resource':'res://assets/hot-fade.tres'}),at(3,**draw('vertex_color_use_as_albedo',True)),at(6,**draw('transparency',1))])
# Build smoke with the same native actions planned for the complete film.
a=[];offset=0
for row in b[16:22]:
 for action in row['actions']:
  if action['op']=='view3d':continue
  a.append({**action,'at':offset});offset+=.35
add('smoke_setup',a,max(15,offset+4))
add('soft_orbit',[view(45,True)],12)
a=[view(),setp('visible',False,'Smoke')]+b[28]['actions']
add('collision_setup',[{**x,'at':i*.4} for i,x in enumerate(a)],12)
add('collision_compare',b[29]['actions'],16)
add('collision_orbit',[view(45,True)],12)
(r/'beat_sheet.json').write_text(json.dumps(dict(beats=beats),indent=2))
print(r,w)

from pathlib import Path
import shutil,json,subprocess,hashlib
W=Path(__file__).resolve().parent;src=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/walker-claude');w=W/'work-5'
if w.exists():raise SystemExit('Existing work-5 must be inspected; refusing to overwrite')
w.mkdir();shutil.copytree(src/'godot/signal-garden',w/'signal-garden',ignore=shutil.ignore_patterns('*.uid','*.import','.DS_Store'))
for n in ['effects','baseline-effects','historical-tuned','tests','.lecture','addons/lecture_capture']:(w/n).mkdir(parents=True,exist_ok=True)
for name in ['burst.tscn','ambient.tscn']:
 shutil.copy2(src/'godot/signal-garden/effects'/name,w/'baseline-effects'/name)
 shutil.copy2(src/'godot/course-series/effects'/name,w/'historical-tuned'/name)
 shutil.copy2(src/'godot/signal-garden/effects'/name,w/'effects'/name)
for name in ['plugin.cfg','plugin.gd','actions.gd']:shutil.copy2(W/'work-3/addons/lecture_capture'/name,w/'addons/lecture_capture'/name)
(w/'project.godot').write_text('''config_version=5
[application]
config/name="Signal Garden — Isolated Particle Lecture"
run/main_scene="res://main.tscn"
config/use_custom_user_dir=true
config/custom_user_dir_name="particle-redo-signal-garden"
[display]
window/size/viewport_width=1280
window/size/viewport_height=720
window/stretch/mode="canvas_items"
[rendering]
renderer/rendering_method="gl_compatibility"
[editor_plugins]
enabled=PackedStringArray("res://addons/lecture_capture/plugin.cfg")
''')
(w/'main.tscn').write_text('''[gd_scene load_steps=2 format=3]
[ext_resource type="Script" path="res://lecture_game.gd" id="1"]
[node name="SignalGarden" type="Node3D"]
script=ExtResource("1")
''')
(w/'lecture_game.gd').write_text('''extends "res://signal-garden/garden.gd"
# Isolated instructional derivative. Existing game authority stays in garden.gd.
var input_request := ""
var effect_events: Array[Dictionary] = []
func _ready():
 super._ready()
 var ambient_position=ambient.position
 remove_child(burst);burst.queue_free();remove_child(ambient);ambient.queue_free()
 burst=load("res://effects/burst.tscn").instantiate();ambient=load("res://effects/ambient.tscn").instantiate()
 add_child(burst);add_child(ambient);ambient.position=ambient_position
 audio_enabled=false;sound.enabled=false;sound.stop_all()
 hud.text="SIGNAL GARDEN · Isolated teaching copy"
func fire_burst(at:Vector3):
 super.fire_burst(at)
 effect_events.append({"position":str(at),"ticks_msec":Time.get_ticks_msec(),"event":effect_events.size()+1})
func _process(_delta):
 var p="res://.lecture/input.json"
 if not FileAccess.file_exists(p):return
 var text=FileAccess.get_file_as_string(p)
 if text==input_request:return
 input_request=text
 var req=JSON.parse_string(text)
 if not req is Dictionary:return
 if req.has("key"):
  var event=InputEventKey.new();event.keycode=OS.find_keycode_from_string(req.key);event.physical_keycode=event.keycode;event.pressed=req.get("pressed",true);Input.parse_input_event(event)
 if req.has("property"):set(req.property,req.value)
 var f=FileAccess.open("res://.lecture/input-log.jsonl",FileAccess.READ_WRITE)
 if f==null:f=FileAccess.open("res://.lecture/input-log.jsonl",FileAccess.WRITE)
 f.seek_end();f.store_line(JSON.stringify({"request":req,"gate_open":gate_open,"won":won,"paused":get_tree().paused,"burst_emitting":burst.emitting,"ambient_emitting":ambient.emitting,"player":str(player.position),"events":effect_events}));f.close()
''')
(w/'README.md').write_text('''# Signal Garden particle lecture copy

This is an isolated instructional derivative of the existing Walker Claude Signal Garden, not a newly discovered pre-particle revision. `signal-garden/` preserves copied source; `baseline-effects/` preserves its original 32-particle burst and 48-particle motes. `historical-tuned/` preserves later course-series resources for comparison, not as a claimed new tuning session. `effects/` is the film's independently editable version. The source repository and its default game remain untouched.

Run `godot --path .`. WASD/arrows move; E starts the committed charge while on the pad; R resets; P pauses. The lecture bridge emits ordinary InputEventKey events and logs them. It is labeled scripted input, not human playtesting. Original gameplay decisions remain in signal-garden/garden.gd. No publication or submission is performed.
''')
rows=[]
for p in sorted((src/'godot/signal-garden').rglob('*')):
 if p.is_file() and p.suffix not in ['.uid','.import']:rows.append(dict(source=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size))
provenance=dict(source_repository=str(src),head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=src,text=True).strip(),status=subprocess.check_output(['git','status','--short'],cwd=src,text=True),scope='Copied current Signal Garden source. Existing local changes preserved. No pre-particle history is claimed.',files=rows)
(w/'SOURCE-PROVENANCE.json').write_text(json.dumps(provenance,indent=2))
# Regression suite runs the isolated selected version, retaining all earlier game checks.
s=(w/'signal-garden/tests/test-garden.gd').read_text().replace('preload("res://signal-garden/garden.gd")','preload("res://lecture_game.gd")')
(w/'tests/test-game.gd').write_text(s)
print(w)

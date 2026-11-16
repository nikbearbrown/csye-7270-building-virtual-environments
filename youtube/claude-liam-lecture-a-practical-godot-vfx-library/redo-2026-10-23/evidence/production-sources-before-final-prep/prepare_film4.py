from pathlib import Path
import shutil
W=Path(__file__).resolve().parent;w=W/'work-4'
if w.exists():raise SystemExit('Existing work-4; refusing overwrite')
shutil.copytree(W/'work-3',w,ignore=shutil.ignore_patterns('.godot','request.json','actions.jsonl','check_scene.gd','check_constants.gd'))
(w/'project.godot').write_text((w/'project.godot').read_text().replace('3D Particle Effects — Original Teaching Stage','Practical VFX Library — Original Teaching Stage').replace('particle-redo-3d','particle-redo-library'))
(w/'stage.gd').write_text('''@tool
extends Node3D
@export var heading := "Build An Explosion"
@export var selected_effect := "Explosion"
var spawned := 0
var cleaned := 0
var input_request := ""
func _ready():
 var camera=get_node_or_null("Camera")
 if camera:camera.position=Vector3(7,5,8);camera.look_at(Vector3(0,1,0))
func _process(_delta):
 var title=get_node_or_null("Title")
 if title:title.text=heading
 if Engine.is_editor_hint():return
 var p="res://.lecture/input.json"
 if FileAccess.file_exists(p):
  var text=FileAccess.get_file_as_string(p)
  if text!=input_request:
   input_request=text;var req=JSON.parse_string(text)
   if req is Dictionary and req.has("key"):
    var event=InputEventKey.new();event.keycode=OS.find_keycode_from_string(req.key);event.physical_keycode=event.keycode;event.pressed=req.get("pressed",true);Input.parse_input_event(event)
func _unhandled_input(event):
 if event is InputEventKey and event.pressed and not event.echo and event.keycode==KEY_SPACE:spawn_effect()
func spawn_effect():
 var file="res://effects/"+selected_effect.to_snake_case()+".tscn"
 if not ResourceLoader.exists(file):return
 var effect=load(file).instantiate();effect.name="Instance"+str(spawned);effect.preview_loop=false;effect.auto_free=true;add_child(effect);effect.position=Vector3(0,.15,0)
 effect.tree_exited.connect(func():cleaned+=1;update_status());effect.play();spawned+=1;update_status()
func update_status():
 var label=get_node_or_null("Status")
 if label:label.text="SPACE · play saved scene | spawned %d · cleaned %d · active %d"%[spawned,cleaned,spawned-cleaned]
''')
(w/'arena.tscn').write_text((w/'arena.tscn').read_text()+'''\n[node name="Status" type="Label3D" parent="."]
position=Vector3(0,-0.1,3.0)
text="SPACE · play saved scene"
font_size=36
pixel_size=0.006
billboard=1
''')
(w/'effect.gd').write_text('''@tool
extends Node3D
## Preview looping is explicitly labeled. Runtime spawns use play() and bounded disposal.
@export var preview_loop := true
@export var preview_interval := 3.5
@export var solo_layer := ""
@export var smoke_enabled := true
@export var auto_free := false
var phase := 999.0
var active := false
var triggered: Array[String] = []
func play():
 phase=0.0;active=true;triggered.clear()
func stop():
 active=false;preview_loop=false
 for child in get_children():
  if child is GPUParticles3D:child.emitting=false
func _process(delta):
 if not is_visible_in_tree():return
 if preview_loop and phase>=preview_interval:play()
 if not active:return
 phase+=delta
 var finish_time:=0.0
 for child in get_children():
  if child is GPUParticles3D:
   child.visible=(solo_layer=="" or solo_layer==child.name) and (smoke_enabled or child.name!="Smoke")
   var delay=float(child.get_meta("delay",0.0));var stop_at=float(child.get_meta("emit_until",4.0))
   finish_time=maxf(finish_time,delay+child.lifetime if child.one_shot else stop_at+child.lifetime)
   if phase>=delay and not str(child.name) in triggered:
    if child.emitting:child.restart()
    else:child.emitting=true
    triggered.append(str(child.name))
   if not child.one_shot and phase>=stop_at:child.emitting=false
  elif child is OmniLight3D:child.light_energy=maxf(0.0,1.0-absf(phase-1.5)*4.0)*2.5
 if auto_free and phase>finish_time+.15:queue_free()
''')
(w/'build_library_assets.gd').write_text('''extends SceneTree
func _initialize():
 var image=Image.create(256,64,false,Image.FORMAT_RGBA8)
 for frame in range(4):
  for y in range(64):
   for x in range(64):
    var p=(Vector2(x,y)-Vector2(31.5,31.5))/31.5
    var radius=.35+frame*.18
    var alpha=clampf(1.0-p.length()/radius,0,1)*(1.0-frame*.17)
    image.set_pixel(frame*64+x,y,Color(1,1,1,alpha))
 image.save_png("res://assets/smoke-flipbook.png")
 var ring=GradientTexture2D.new();ring.width=128;ring.height=128;ring.fill=GradientTexture2D.FILL_RADIAL;ring.fill_from=Vector2(.5,.5);ring.fill_to=Vector2(1,.5)
 var gradient=Gradient.new();gradient.set_color(0,Color(1,1,1,0));gradient.set_color(1,Color(1,1,1,0));gradient.add_point(.65,Color(1,1,1,0));gradient.add_point(.8,Color.WHITE);gradient.add_point(.9,Color(1,1,1,0));ring.gradient=gradient;ResourceSaver.save(ring,"res://assets/ring.tres")
 var fade=GradientTexture1D.new();fade.gradient=Gradient.new();fade.gradient.set_color(0,Color(1,.9,.5,1));fade.gradient.set_color(1,Color(.6,.15,.02,0));ResourceSaver.save(fade,"res://assets/flash-fade.tres")
 var blue=GradientTexture1D.new();blue.gradient=Gradient.new();blue.gradient.set_color(0,Color(.2,.6,1,1));blue.gradient.set_color(1,Color(.7,.2,1,0));ResourceSaver.save(blue,"res://assets/magic-fade.tres")
 print("Original flipbook, ring and ramps saved");quit()
''')
(w/'arena2d.gd').write_text('''@tool
extends Node2D
@export var heading := "Dust And Trails"
@export var moving := false
@export var stream_enabled := true
@export var repeat_preview := true
var clock:=0.0
var last_burst:=0.0
func _process(delta):
 clock+=delta
 var trail=get_node_or_null("Trail")
 if trail:trail.position=Vector2(sin(clock)*260 if moving else 0,100);trail.emitting=stream_enabled
 var dust=get_node_or_null("Dust")
 if dust and repeat_preview and clock-last_burst>2.8:dust.restart();last_burst=clock
 queue_redraw()
func _draw():
 draw_rect(Rect2(-620,-340,1240,680),Color("10151d"))
 draw_line(Vector2(-560,110),Vector2(560,110),Color("a7b3b9"),2)
 draw_string(ThemeDB.fallback_font,Vector2(-560,-280),heading,HORIZONTAL_ALIGNMENT_LEFT,-1,36,Color.WHITE)
 draw_string(ThemeDB.fallback_font,Vector2(-560,280),"Scripted preview · world-space motion · same ground line",HORIZONTAL_ALIGNMENT_LEFT,-1,22,Color("a7b3b9"))
''')
(w/'arena2d.tscn').write_text('''[gd_scene load_steps=2 format=3]
[ext_resource type="Script" path="res://arena2d.gd" id="1"]
[node name="DustStage" type="Node2D"]
script=ExtResource("1")
[node name="FrameGuide" type="Control" parent="."]
offset_left=-640.0
offset_top=-360.0
offset_right=640.0
offset_bottom=360.0
mouse_filter=2
''')
(w/'README.md').write_text('''# Practical VFX library teaching stage

Original procedural textures and scenes, created for this corrective lecture. The editor plugin labels scripted actions and logs property changes. Native recording is a required final gate. Preview loops are explicit teaching controls. Runtime Space spawns a saved scene with bounded disposal; the real game state owns any gameplay event. No motion capture here is a performance benchmark.

The flipbook is an original four-cell radial sequence generated by Godot, not a downloaded asset. Resource ownership separates behavior/material edits while retaining intentional texture sharing. Rain collision/sub-emission remains provisional until tested on the actual renderer; a decorative emitter must never be described as a collision result.
''')
print(w)

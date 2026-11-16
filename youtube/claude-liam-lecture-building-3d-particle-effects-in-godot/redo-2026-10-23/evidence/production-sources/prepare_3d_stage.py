from pathlib import Path
import shutil
w=Path(__file__).resolve().parent/'work-3'
w.mkdir(exist_ok=True)
for n in ['assets','effects','.lecture','addons/lecture_capture']:(w/n).mkdir(parents=True,exist_ok=True)
for n in ['plugin.cfg','plugin.gd','actions.gd']:
 src=w.parent/('work-2/addons/lecture_capture' if n=='plugin.cfg' else 'shared-plugin')/n
 shutil.copy2(src,w/'addons/lecture_capture'/n)
(w/'project.godot').write_text('''config_version=5
[application]
config/name="3D Particle Effects — Original Teaching Stage"
run/main_scene="res://arena.tscn"
config/use_custom_user_dir=true
config/custom_user_dir_name="particle-redo-3d"
[display]
window/size/viewport_width=1280
window/size/viewport_height=720
window/stretch/mode="canvas_items"
[rendering]
renderer/rendering_method="gl_compatibility"
environment/defaults/default_clear_color=Color(0.04,0.05,0.07,1)
[editor_plugins]
enabled=PackedStringArray("res://addons/lecture_capture/plugin.cfg")
''')
(w/'stage.gd').write_text('''@tool
extends Node3D
@export var heading := "Add Depth And A Draw Pass"
@export var move_source := false
@export var orbit_camera := false
var clock := 0.0
func _ready():
 var camera=get_node_or_null("Camera")
 if camera:camera.position=Vector3(7,5,8);camera.look_at(Vector3(0,1,0))
func _process(delta):
 clock+=delta
 var title=get_node_or_null("Title")
 if title:title.text=heading
 var source=get_node_or_null("Particles")
 if source and move_source:source.position.x=sin(clock)*2
 var camera=get_node_or_null("Camera")
 if camera and orbit_camera:
  camera.position=Vector3(cos(clock*.4)*9,5,sin(clock*.4)*9);camera.look_at(Vector3(0,1,0))
''')
(w/'arena.tscn').write_text('''[gd_scene load_steps=7 format=3]
[ext_resource type="Script" path="res://stage.gd" id="1"]
[sub_resource type="StandardMaterial3D" id="FloorMat"]
albedo_color=Color(0.15,0.19,0.23,1)
[sub_resource type="PlaneMesh" id="Floor"]
material=SubResource("FloorMat")
size=Vector2(12,12)
[sub_resource type="StandardMaterial3D" id="ScaleMat"]
albedo_color=Color(0.85,0.37,0.25,1)
[sub_resource type="BoxMesh" id="ScaleMesh"]
material=SubResource("ScaleMat")
size=Vector3(0.15,1,0.15)
[sub_resource type="Environment" id="World"]
background_mode=1
background_color=Color(0.035,0.045,0.065,1)
ambient_light_source=3
ambient_light_color=Color(0.7,0.8,1,1)
ambient_light_energy=0.6
[node name="ParticleStage" type="Node3D"]
script=ExtResource("1")
[node name="Floor" type="MeshInstance3D" parent="."]
mesh=SubResource("Floor")
[node name="ScaleReference" type="MeshInstance3D" parent="."]
position=Vector3(-2,0.5,0)
mesh=SubResource("ScaleMesh")
[node name="ScaleLabel" type="Label3D" parent="."]
position=Vector3(-2,1.4,0)
text="1 m"
font_size=48
pixel_size=0.005
billboard=1
[node name="Title" type="Label3D" parent="."]
position=Vector3(0,4.5,0)
text="Add Depth And A Draw Pass"
font_size=48
pixel_size=0.006
billboard=1
[node name="Light" type="DirectionalLight3D" parent="."]
rotation_degrees=Vector3(-55,-25,0)
light_energy=1.1
shadow_enabled=true
[node name="WorldEnvironment" type="WorldEnvironment" parent="."]
environment=SubResource("World")
[node name="Camera" type="Camera3D" parent="."]
current=true
fov=55.0
''')
(w/'build_assets.gd').write_text('''extends SceneTree
func _initialize():
 var dot=GradientTexture2D.new();dot.width=96;dot.height=96;dot.fill=GradientTexture2D.FILL_RADIAL;dot.fill_from=Vector2(.5,.5);dot.fill_to=Vector2(1,.5)
 var gradient=Gradient.new();gradient.set_color(0,Color.WHITE);gradient.set_color(1,Color(1,1,1,0));gradient.add_point(.4,Color(1,1,1,.6));dot.gradient=gradient
 ResourceSaver.save(dot,"res://assets/soft-dot.tres")
 var ramp=GradientTexture1D.new();ramp.gradient=Gradient.new();ramp.gradient.set_color(0,Color(1,.9,.5,1));ramp.gradient.set_color(1,Color(.9,.22,.04,0));ramp.gradient.add_point(.3,Color(1,.45,.07,1));ResourceSaver.save(ramp,"res://assets/hot-fade.tres")
 var smoke=GradientTexture1D.new();smoke.gradient=Gradient.new();smoke.gradient.set_color(0,Color(.6,.67,.75,.1));smoke.gradient.set_color(1,Color(.35,.4,.48,0));smoke.gradient.add_point(.2,Color(.7,.74,.8,.55));ResourceSaver.save(smoke,"res://assets/smoke-fade.tres")
 var curve=CurveTexture.new();curve.curve=Curve.new();curve.curve.add_point(Vector2(0,.2));curve.curve.add_point(Vector2(.3,.6));curve.curve.add_point(Vector2(1,1));ResourceSaver.save(curve,"res://assets/grow.tres")
 print("Original procedural particle resources saved");quit()
''')
print(w)

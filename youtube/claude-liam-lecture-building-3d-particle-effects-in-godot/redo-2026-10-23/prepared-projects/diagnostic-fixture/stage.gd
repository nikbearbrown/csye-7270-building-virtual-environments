@tool
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

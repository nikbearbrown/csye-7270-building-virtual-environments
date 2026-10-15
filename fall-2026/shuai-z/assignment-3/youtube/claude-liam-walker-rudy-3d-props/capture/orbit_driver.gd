extends Node
## Film-only autoload, added to an isolated copy of godot/ (never to the
## project itself). The real main scene, res://scenes/props_room.tscn, boots
## as F5 runs it; this node only moves its Camera around the props and quits.
## It changes no prop, light, floor or material.
##
## Take: HOLD frames on the scene's own camera, then one 360-degree orbit about
## the props' middle at the camera's own radius and height, then HOLD frames.

const HOLD := 45            ## frames (1.5 s at 30 fps)
const ORBIT := 600          ## frames (20 s)
const CENTRE := Vector3(-0.3, 0.25, 0.0)  ## the point the scene's camera looks at

var _cam: Camera3D
var _home: Transform3D
var _radius := 0.0
var _height := 0.0
var _frame := -1


func _ready() -> void:
	await get_tree().process_frame
	_cam = get_tree().current_scene.get_node("Camera") as Camera3D
	_home = _cam.global_transform
	var off := _home.origin - CENTRE
	_radius = Vector2(off.x, off.z).length()
	_height = _home.origin.y
	print("orbit: home %s radius %.3f height %.3f" % [_home.origin, _radius, _height])


func _process(_delta: float) -> void:
	if _cam == null:
		return
	_frame += 1
	var f := _frame - HOLD
	if f <= 0:
		_cam.global_transform = _home
	elif f <= ORBIT:
		var u := float(f) / ORBIT
		var a := TAU * (u - sin(TAU * u) / TAU)  # eases in and out, one full turn
		var pos := CENTRE + Vector3(sin(a) * _radius, _height - CENTRE.y, cos(a) * _radius)
		_cam.look_at_from_position(pos, CENTRE, Vector3.UP)
	else:
		_cam.global_transform = _home
	if _frame >= HOLD * 2 + ORBIT:
		get_tree().quit()

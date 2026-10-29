extends Node
## Film-only autoload, added to an isolated copy of godot/ (never to the
## project itself). The real main scene, res://scenes/props_room.tscn, boots
## as F5 runs it; this node only moves its Camera and quits. It changes no prop,
## light, floor or material, so the waystone's and the circle's surfaces are
## drawn by weathered_stone.gdshader through their two materials, as saved.
##
## Take, in frames at 30 fps, with a cut between parts:
##   A  HOLD on the scene's own camera, one orbit about the props' middle at the
##      camera's own radius and height, HOLD at home;
##   B  an arc in front of the waystone, close up;
##   C  an arc over the teleport circle, close up.

const HOLD := 45
const ORBIT := 600
const ARC := 300
const CENTRE := Vector3(-0.3, 0.25, 0.0)    ## the point the scene's camera looks at
const WAYSTONE := Vector3(-0.8, 0.42, 0.0)  ## the waystone's middle (origin -0.8, 0, 0; 0.84 m tall)
const CIRCLE := Vector3(1.2, 0.05, 0.0)     ## the circle's top (origin 1.2, 0, 0)

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
	var f := _frame
	if f < HOLD:
		_cam.global_transform = _home
		return
	f -= HOLD
	if f < ORBIT:
		var u := float(f) / ORBIT
		var a := TAU * (u - sin(TAU * u) / TAU)  # eases in and out, one full turn
		_cam.look_at_from_position(CENTRE + Vector3(sin(a) * _radius, _height - CENTRE.y, cos(a) * _radius), CENTRE, Vector3.UP)
		return
	f -= ORBIT
	if f < HOLD:
		_cam.global_transform = _home
		return
	f -= HOLD
	if f < ARC:
		_arc(f, WAYSTONE, 1.7, 0.95, deg_to_rad(-55.0), deg_to_rad(55.0))
		return
	f -= ARC
	if f < ARC:
		_arc(f, CIRCLE, 2.0, 1.5, deg_to_rad(-40.0), deg_to_rad(40.0))
		return
	get_tree().quit()


## One eased sweep from angle a0 to a1 (0 = in front, +Z) about target, at a
## horizontal radius and a height above the floor.
func _arc(f: int, target: Vector3, radius: float, height: float, a0: float, a1: float) -> void:
	var u := float(f) / (ARC - 1)
	var a := lerpf(a0, a1, 0.5 - 0.5 * cos(PI * u))
	_cam.look_at_from_position(Vector3(target.x + sin(a) * radius, height, target.z + cos(a) * radius), target, Vector3.UP)

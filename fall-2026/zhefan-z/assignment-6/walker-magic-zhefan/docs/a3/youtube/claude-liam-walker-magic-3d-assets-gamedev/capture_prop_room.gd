extends Node3D
## Capture harness for the Assignment 3 prop room film. Lives only in the throwaway capture copy,
## at res://capture/. Instantiates the REAL res://showcase3d/prop_room.tscn unchanged and moves
## ONLY its Camera: a hold on the saved camera, then a slow orbit around the saved look point.
## Nothing else in the scene is written. Every frame's camera pose is logged.
##
## Environment:
##   WALKER_CAPTURE_MODE=probe|run-01   probe: 1 s hold + 2 s orbit through 60 deg; run-01: the take
##   WALKER_CAPTURE_LOG=<path>          JSONL camera log (one row per frame)
##
## Checks before the first frame, exit 1 on failure: exactly one Light3D; Rock, Crystal and Chest
## with their lowest vertex at y = 0 (+-0.02 m); the Mage set to Y-billboard. Exit 0 when the
## camera path completes. The prop room has no sound; Movie Maker records silence.

const TARGET := Vector3(-0.65, 0.45, 0.0)   # the saved camera's look point (see prop_room.tscn)
const TOL := 0.02
const MODES := {
	"probe": {"hold": 60, "orbit": 120, "sweep_deg": 60.0, "tail": 30},
	"run-01": {"hold": 120, "orbit": 540, "sweep_deg": 180.0, "tail": 60},
}

var scene: Node3D
var cam: Camera3D
var mode := "probe"
var plan: Dictionary
var log_file: FileAccess
var frame := 0
var radius := 0.0
var height := 0.0
var start_angle := 0.0


func _ready() -> void:
	var m := OS.get_environment("WALKER_CAPTURE_MODE")
	if m != "":
		mode = m
	if not MODES.has(mode):
		_fail("unknown WALKER_CAPTURE_MODE " + mode)
		return
	plan = MODES[mode]
	var log_path := OS.get_environment("WALKER_CAPTURE_LOG")
	if log_path != "":
		log_file = FileAccess.open(log_path, FileAccess.WRITE)
	scene = (load("res://showcase3d/prop_room.tscn") as PackedScene).instantiate()
	add_child(scene)
	cam = scene.get_node("Camera")
	var offset := cam.position - TARGET
	radius = Vector2(offset.x, offset.z).length()
	height = cam.position.y
	start_angle = atan2(offset.x, offset.z)

	var problems: Array[String] = []
	var lights := _count_lights(scene)
	if lights != 1:
		problems.append("lights = %d" % lights)
	var lowest := {}
	for n in ["Rock", "Crystal", "Chest"]:
		var y := _lowest_y(scene.get_node(n))
		lowest[n] = snappedf(y, 0.0001)
		if absf(y) > TOL:
			problems.append("%s lowest y = %.4f" % [n, y])
	var mage: Sprite3D = scene.get_node("Mage")
	if mage.billboard != BaseMaterial3D.BILLBOARD_FIXED_Y:
		problems.append("Mage billboard = %d" % mage.billboard)
	_log({"event": "start", "mode": mode, "plan": plan, "lights": lights, "lowest_y": lowest,
		"mage_billboard": mage.billboard, "radius": snappedf(radius, 0.0001), "height": height,
		"viewport": [get_viewport().size.x, get_viewport().size.y]})
	if not problems.is_empty():
		_fail("checks failed: " + ", ".join(problems))


func _process(_delta: float) -> void:
	if plan.is_empty():
		return
	frame += 1
	var phase := "hold"
	var angle := start_angle
	if frame > plan.hold:
		var t := clampf(float(frame - plan.hold) / float(plan.orbit), 0.0, 1.0)
		angle = start_angle + deg_to_rad(plan.sweep_deg) * smoothstep(0.0, 1.0, t)
		phase = "orbit" if frame <= plan.hold + plan.orbit else "tail"
		cam.position = Vector3(TARGET.x + sin(angle) * radius, height, TARGET.z + cos(angle) * radius)
		cam.look_at(TARGET, Vector3.UP)
	_log({"frame": frame, "phase": phase, "angle_deg": snappedf(rad_to_deg(angle), 0.001),
		"cam": [snappedf(cam.position.x, 0.0001), snappedf(cam.position.y, 0.0001), snappedf(cam.position.z, 0.0001)]})
	if frame >= plan.hold + plan.orbit + plan.tail:
		_log({"event": "end", "frames": frame, "exit": 0})
		print("CAPTURE END mode=%s frames=%d exit=0" % [mode, frame])
		get_tree().quit(0)


func _count_lights(node: Node) -> int:
	var n := 1 if node is Light3D else 0
	for c in node.get_children():
		n += _count_lights(c)
	return n


func _lowest_y(node: Node) -> float:
	var lowest := INF
	for c in node.find_children("*", "MeshInstance3D", true, false):
		var mi := c as MeshInstance3D
		for s in mi.mesh.get_surface_count():
			for v in mi.mesh.surface_get_arrays(s)[Mesh.ARRAY_VERTEX]:
				var p: Vector3 = mi.global_transform * v
				lowest = minf(lowest, p.y)
	return lowest


func _log(row: Dictionary) -> void:
	if log_file:
		log_file.store_line(JSON.stringify(row))
		log_file.flush()


func _fail(reason: String) -> void:
	_log({"event": "fail", "reason": reason, "exit": 1})
	print("CAPTURE FAIL mode=%s: %s" % [mode, reason])
	plan = {}
	get_tree().quit(1)

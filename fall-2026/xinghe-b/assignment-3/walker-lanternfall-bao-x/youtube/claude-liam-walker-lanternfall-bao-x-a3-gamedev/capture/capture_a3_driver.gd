extends Node
## Film capture driver for the Assignment 3 room — used only in an isolated copy of godot/ at the film's
## source revision. It plays the room through its real input actions (Input.action_press), so the room reads
## the same actions a player's keys produce. Scripted input, labelled on screen.
##
##   godot --always-on-top --path . res://capture_a3_main.tscn --write-movie out.avi --fixed-fps 30 -- <take>
##   takes: orbit (front → behind → below → front → zoom) · block (collision shapes on; stand-in into the gate)

const ROOM := "res://a3/lantern_gate_room.tscn"

# [first process frame, last frame (exclusive), action, on-screen label]; 30 frames per second.
const TIMELINES := {
	"orbit": [
		[45, 104, "a3_orbit_right", "E held · orbit"],
		[164, 186, "a3_tilt_down", "F held · tilt down, below the floor"],
		[261, 282, "a3_tilt_up", "R held · tilt up"],
		[282, 341, "a3_orbit_right", "E held · orbit back to the front"],
		[371, 389, "a3_zoom_in", "Z held · zoom in"],
	],
	"block": [
		[0, 18, "a3_zoom_in", "Z held · zoom in"],
		[30, 53, "move_right", "D held · stand-in moves in front of the gate"],
		[60, 150, "move_up", "W held · stand-in drives into the gate base"],
	],
}
const LENGTH := {"orbit": 450, "block": 210}

var take := "orbit"
var room: Node3D
var f := 0                 # timeline frame: advances only on frames the window could draw
var movie_frame := 0       # every process frame Movie Maker writes
var stale: Array = []      # movie frames written while the window could not draw (the tree was paused)
var label: Label
var log_lines: Array = []

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS   # keeps running while the room is paused on a stale frame
	var args := OS.get_cmdline_user_args()
	if args.size() > 0:
		take = args[0]
	if take == "block":
		get_tree().debug_collisions_hint = true   # must be set before the bodies enter the tree
	room = load(ROOM).instantiate()
	room.process_mode = Node.PROCESS_MODE_PAUSABLE
	add_child(room)
	var layer := CanvasLayer.new()
	layer.layer = 50
	add_child(layer)
	label = Label.new()
	label.position = Vector2(8, 330)
	label.add_theme_font_size_override("font_size", 10)
	label.add_theme_color_override("font_outline_color", Color.BLACK)
	label.add_theme_constant_override("outline_size", 3)
	layer.add_child(label)
	_log("start", {"take": take, "camera": str(room.camera.position)})

func _process(_delta: float) -> void:
	movie_frame += 1
	# macOS stops drawing an occluded window and Movie Maker repeats the last picture: pause the room on
	# those frames and list them, so tools/clean_take.py can drop exactly those frames.
	if not DisplayServer.window_can_draw():
		stale.append(movie_frame - 1)
		get_tree().paused = true
		return
	get_tree().paused = false
	var active := "no input"
	for step in TIMELINES[take]:
		var held: bool = f >= step[0] and f < step[1]
		if held and not Input.is_action_pressed(step[2]):
			Input.action_press(step[2])
			_log("press", {"action": step[2]})
		elif not held and f == step[1]:
			Input.action_release(step[2])
			_log("release", {"action": step[2], "camera": str(room.camera.position),
				"floor_mesh_visible": room.floor_mesh.visible, "stand_in": str(room.stand_in.position)})
		if held:
			active = step[3]
	label.text = "Real engine capture · scripted input · %s" % active
	f += 1
	if f >= LENGTH[take]:
		_log("end", {"frames": f, "movie_frames": movie_frame, "stale": stale, "camera": str(room.camera.position),
			"stand_in": str(room.stand_in.position)})
		var out := FileAccess.open("user://capture-%s.jsonl" % take, FileAccess.WRITE)
		for line in log_lines:
			out.store_line(line)
		out.close()
		print("A3_CAPTURE_LOG ", ProjectSettings.globalize_path("user://capture-%s.jsonl" % take))
		get_tree().quit(0)

func _log(event: String, data: Dictionary) -> void:
	data["event"] = event
	data["frame"] = f
	log_lines.append(JSON.stringify(data))
	print("A3_CAPTURE ", JSON.stringify(data))

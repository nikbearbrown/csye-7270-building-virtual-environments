extends Node
## GENERIC CAPTURE DRIVER (scratch copies only; never part of a source project).
## Autoload. Reads a JSON plan (user arg --plan=/abs/plan.json) and, frame by frame
## (Movie Maker fixed 30 fps), injects REAL input through Input.parse_input_event:
##   {"f":N, "action":"move_left", "down":true, "strength":1.0}  -> InputEventAction
##   {"f":N, "key":"Enter", "down":true}                           -> InputEventKey
##   {"f":N, "motion":[dx,dy]}                                     -> InputEventMouseMotion (relative)
##   {"f":N, "click":[x,y], "button":1, "down":true}               -> InputEventMouseButton
##   "seed": N (optional) seeds the global RNG once at startup (repeatable random spawns)
##   {"f":N, "call":"method_name", "node":"/root/Path"}            -> calls a method on a node (logged)
##   "track": [{"node":"/root/Pong/Left","target":"/root/Pong/Ball","up":"a_up","down":"a_down",
##              "from":F0,"to":F1,"axis":"y","deadzone":4}]  -> each frame between F0 and F1, PRESSES/RELEASES the
##              up/down actions (InputEventAction) so `node` follows `target` on that axis: a scripted
##              "player" that reads the screen state and pushes buttons; it never moves anything itself.
## and saves rendered viewport frames: {"f":N, "name":"01-x"} in "shots".
## Every injected event is printed as "INPUT f=<frame> ...". Quits at plan.quit.

var plan: Dictionary = {}
var out := ""
var frame := 0

func _ready() -> void:
	process_priority = -100
	process_mode = Node.PROCESS_MODE_ALWAYS
	var plan_path := ""
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--plan="): plan_path = a.substr(7)
		if a.begins_with("--out="): out = a.substr(6)
	plan = JSON.parse_string(FileAccess.get_file_as_string(plan_path))
	DirAccess.make_dir_recursive_absolute(out)
	if plan.has("seed"):
		seed(int(plan.seed)) # global RNG seed only, so a random demo is repeatable
		print("SEED %d" % int(plan.seed))
	print("CAPTURE DRIVER plan=%s out=%s" % [plan_path, out])

func _process(_delta: float) -> void:
	frame += 1
	for e in plan.get("events", []):
		if int(e.f) == frame: _inject(e)
	for s in plan.get("shots", []):
		if int(s.f) == frame: _shot(s.name)
	for t in plan.get("track", []):
		_track(t)
	if frame == int(plan.get("quit", 300)): get_tree().quit()

var _track_state := {}
func _track(t: Dictionary) -> void:
	var key: String = t.node + t.up
	var want := 0
	if frame >= int(t.get("from", 0)) and frame < int(t.get("to", 1000000)):
		var n := get_node_or_null(t.node)
		var g := get_node_or_null(t.target)
		if n and g:
			var ax: String = t.get("axis", "y")
			var d: float = (g.global_position[ax] - n.global_position[ax]) + float(t.get("offset", 0))
			var dz := float(t.get("deadzone", 4))
			if d > dz: want = 1
			elif d < -dz: want = -1
	var have: int = _track_state.get(key, 0)
	if want == have: return
	if have == 1: _inject({"action": t.down, "down": false})
	if have == -1: _inject({"action": t.up, "down": false})
	if want == 1: _inject({"action": t.down, "down": true})
	if want == -1: _inject({"action": t.up, "down": true})
	_track_state[key] = want

func _inject(e: Dictionary) -> void:
	var down: bool = e.get("down", true)
	if e.has("action"):
		var ev := InputEventAction.new()
		ev.action = e.action
		ev.pressed = down
		ev.strength = float(e.get("strength", 1.0)) if down else 0.0
		Input.parse_input_event(ev)
		print("INPUT f=%d t=%.2fs action %s %s" % [frame, frame / 30.0, e.action, "DOWN" if down else "UP"])
	elif e.has("key"):
		var k := InputEventKey.new()
		var code := OS.find_keycode_from_string(e.key)
		k.keycode = code
		k.physical_keycode = code
		k.pressed = down
		Input.parse_input_event(k)
		print("INPUT f=%d t=%.2fs key %s %s" % [frame, frame / 30.0, e.key, "DOWN" if down else "UP"])
	elif e.has("motion"):
		var m := InputEventMouseMotion.new()
		m.relative = Vector2(e.motion[0], e.motion[1])
		m.screen_relative = m.relative
		m.position = get_viewport().get_visible_rect().size / 2
		Input.parse_input_event(m)
		print("INPUT f=%d t=%.2fs mouse motion %s" % [frame, frame / 30.0, str(m.relative)])
	elif e.has("click"):
		var b := InputEventMouseButton.new()
		b.button_index = int(e.get("button", 1))
		b.position = Vector2(e.click[0], e.click[1])
		b.global_position = b.position
		b.pressed = down
		Input.parse_input_event(b)
		print("INPUT f=%d t=%.2fs mouse button %d at %s %s" % [frame, frame / 30.0, b.button_index, str(b.position), "DOWN" if down else "UP"])
	elif e.has("call"):
		var n := get_node_or_null(e.get("node", "/root"))
		if n and n.has_method(e.call):
			n.call(e.call)
			print("CALL f=%d t=%.2fs %s.%s()" % [frame, frame / 30.0, e.get("node"), e.call])
		else:
			print("CALL FAILED f=%d %s.%s()" % [frame, e.get("node"), e.call])

func _shot(label: String) -> void:
	await RenderingServer.frame_post_draw
	var img := get_viewport().get_texture().get_image()
	var path := out + "/" + label + ".png"
	img.save_png(path)
	print("SHOT f=%d t=%.2fs %s %dx%d" % [frame, frame / 30.0, path, img.get_width(), img.get_height()])

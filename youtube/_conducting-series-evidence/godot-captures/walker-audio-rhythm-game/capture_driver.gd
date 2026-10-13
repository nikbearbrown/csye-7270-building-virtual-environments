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
##   "seek": {"player":path,"camera":path,"targets":path,"from":F0,"to":F1,"jump_every":90,"jump_hold":60,"shoot_every":30}
##       3D state-observing route (same idea as walker-3d-platformer tests/feature_route.gd): steers toward the
##       nearest untaken child of `targets` by PRESSING move_* actions (analog strength), jumping and shooting.
##   "rhythm": {"node":"/root/Main/Notes","action":"main_key","lead":0.06,"from":F0,"to":F1,"skip_every":0}
##       reads the NoteManager's own next-note delta and PRESSES the action when the note is `lead` seconds
##       away (one 30 fps frame of input latency); never assigns scores. skip_every=N lets every Nth note pass.
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
	if plan.has("seek"): _seek(plan.seek)
	if plan.has("rhythm"): _rhythm(plan.rhythm)
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


var _seek_jump_age := 100
var _held := {}
func _set_action(action: String, strength: float) -> void:
	var was: float = _held.get(action, 0.0)
	if strength <= 0.01:
		if was > 0.0:
			_inject({"action": action, "down": false})
			_held[action] = 0.0
		return
	if was <= 0.0:
		_inject({"action": action, "down": true, "strength": strength})
	elif absf(was - strength) > 0.02:
		var ev := InputEventAction.new() # strength update while held (not logged per frame)
		ev.action = action
		ev.pressed = true
		ev.strength = strength
		Input.parse_input_event(ev)
	_held[action] = strength

func _seek(cfg: Dictionary) -> void:
	var actions := ["move_forward", "move_back", "move_left", "move_right", "jump", "shoot"]
	var desired := {}
	if frame >= int(cfg.get("from", 0)) and frame < int(cfg.get("to", 1000000)):
		var player: Node3D = get_node_or_null(cfg.player)
		var camera: Node3D = get_node_or_null(cfg.camera)
		var targets := get_node_or_null(cfg.targets)
		if player and camera and targets:
			var nearest: Node3D = null
			var distance := INF
			for c in targets.get_children():
				if ("taken" in c and c.taken): continue
				if cfg.has("max_y") and c.global_position.y > float(cfg.max_y): continue
				var d: float = player.global_position.distance_to(c.global_position)
				if d < distance:
					distance = d
					nearest = c
			_seek_jump_age += 1
			if nearest:
				var delta: Vector3 = nearest.global_position - player.global_position
				delta.y = 0
				var right: Vector3 = camera.global_basis.x
				var back: Vector3 = camera.global_basis.z
				right.y = 0
				back.y = 0
				var mv := Vector2(delta.normalized().dot(right.normalized()), delta.normalized().dot(back.normalized()))
				desired["move_right" if mv.x > 0 else "move_left"] = absf(mv.x)
				desired["move_back" if mv.y > 0 else "move_forward"] = absf(mv.y)
				if player.is_on_floor() and _seek_jump_age > int(cfg.get("jump_every", 90)) and distance > 1:
					_seek_jump_age = 0
				if _seek_jump_age < int(cfg.get("jump_hold", 60)) / 2:
					desired["jump"] = 1.0
				if int(cfg.get("shoot_every", 0)) > 0 and frame % int(cfg.shoot_every) == 0:
					desired["shoot"] = 1.0
	for a in actions:
		_set_action(a, float(desired.get(a, 0.0)))
	if frame % 30 == 0 and get_node_or_null(cfg.player) and "coins" in get_node(cfg.player):
		print("STATE f=%d coins=%d pos=%s" % [frame, get_node(cfg.player).coins, str(get_node(cfg.player).global_position)])


var _rhythm_release := -1
var _rhythm_last_note: Object = null
var _rhythm_count := 0
func _rhythm(cfg: Dictionary) -> void:
	if frame == _rhythm_release:
		_inject({"action": cfg.action, "down": false})
	if frame < int(cfg.get("from", 0)) or frame >= int(cfg.get("to", 1000000)): return
	var nm := get_node_or_null(cfg.node)
	if nm == null or nm._notes.is_empty(): return
	var note: Object = nm._notes[0]
	if note == _rhythm_last_note: return
	var delta: float = nm._get_note_delta(note)
	if delta >= -float(cfg.get("lead", 0.06)) and delta < 0.1:
		_rhythm_last_note = note
		_rhythm_count += 1
		var skip := int(cfg.get("skip_every", 0))
		if skip > 0 and _rhythm_count % skip == 0:
			print("RHYTHM f=%d note beat=%.2f delta=%.3f LET PASS (deliberate miss)" % [frame, note.beat, delta])
			return
		print("RHYTHM f=%d note beat=%.2f observed delta=%.3f -> press" % [frame, note.beat, delta])
		_inject({"action": cfg.action, "down": true})
		_rhythm_release = frame + 2

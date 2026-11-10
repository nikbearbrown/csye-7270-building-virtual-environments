extends SceneTree
## Scripted-input capture driver for the Assignment 6 film (Brutalist godot-waikthrough capture contract, used by
## godot-gamedev). Runs the real game scene, res://game/main.tscn, on an isolated copy of the project at the film's
## revision, and plays it only through the normal input path: Input.parse_input_event with key events (A/D walk,
## Space jump, Esc pause) and mouse events (motion to the aim point, then a left click to cast). It observes positions
## to choose its inputs; it never moves the player, calls cast() or explode(), or sets any game or effect value.
## `test_mode` is set on Main only so that a failure would not reload the scene under this script (main.gd:79, 95).
## Harness, not game: the game runs inside its own 640x360 SubViewport, shown 1:1 by a TextureRect that fills the
## window. In a real window, every viewport whose section root is the window (the root, or a SubViewport inside a
## SubViewportContainer) reads the aim from the OS cursor (Viewport.get_mouse_position asks the display server), so
## injected mouse motion would not move it, and warping the cursor would take over the user's real mouse. A standalone
## SubViewport uses the last mouse event pushed into it instead. Keys go through Input.parse_input_event (the actions
## the player reads) and are also pushed into the game's viewport (SessionInput's Esc). The SubViewport is pausable,
## so the game pauses exactly as in a normal run.
## Record with Movie Maker, windowed (the frames are the real rendered 640x360 viewport):
##   godot --path <capture copy> --script <this file> --write-movie <abs>/frame.png --fixed-fps 30 --resolution 1280x720
## Writes one JSON line per input and per observed event to the path in the first user argument (-- <log.jsonl>), and
## quits 1 if an expected impact, trail or pause did not happen, so an exhausted run is never taken as success.

const MAIN := "res://game/main.tscn"
const IMPACT := "res://effects/fireball_impact.tscn"
const TRAIL := "res://effects/fireball_trail.tscn"
const GROUND_Y := 345.0     # an aim point below the ground top (327)
const STAFF_Y := 267.0      # the staff crystal's height when standing (feet 327, STAFF_TIP.y -60)

var main: Node
var vp: SubViewport
var player: Node2D
var frame := 0
var log_file: FileAccess
var counts := {}
var failures: Array[String] = []
var segment := ""


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	log_file = FileAccess.open(args[0] if args.size() > 0 else "user://capture_inputs.jsonl", FileAccess.WRITE)
	process_frame.connect(func() -> void: frame += 1)
	vp = SubViewport.new()
	vp.size = Vector2i(640, 360)
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	vp.process_mode = Node.PROCESS_MODE_PAUSABLE
	root.add_child(vp)
	var view := TextureRect.new()
	view.texture = vp.get_texture()
	view.size = Vector2(640, 360)
	view.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	view.process_mode = Node.PROCESS_MODE_ALWAYS
	root.add_child(view)
	call_deferred("run")


func note(kind: String, data := {}) -> void:
	var row := {"frame": frame, "segment": segment, "kind": kind}
	row.merge(data)
	log_file.store_line(JSON.stringify(row))
	log_file.flush()


func frames(n: int) -> void:
	for i in n:
		await process_frame


func seconds(s: float) -> void:
	await frames(int(round(s * 30.0)))


func expect(id: String, ok: bool, data := {}) -> void:
	note("expect", {"id": id, "ok": ok}.merged(data))
	if not ok:
		failures.append(id)


func fresh(name: String) -> void:
	if is_instance_valid(main):
		main.queue_free()
		await frames(2)
	segment = name
	counts = {"casts": 0, "impacts": 0, "trails_detached": 0, "pauses": 0}
	main = load(MAIN).instantiate()
	main.test_mode = true
	main.child_entered_tree.connect(_on_child)
	vp.add_child(main)
	player = main.player
	player.cast_fired.connect(func(o: Vector2, d: Vector2) -> void:
		counts.casts += 1
		note("cast_fired", {"origin": [snappedf(o.x, 0.1), snappedf(o.y, 0.1)], "dir": [snappedf(d.x, 0.001), snappedf(d.y, 0.001)]}))
	note("segment_start", {"player": [player.global_position.x, player.global_position.y]})
	await frames(15)


func _on_child(node: Node) -> void:
	if node.scene_file_path == IMPACT:
		counts.impacts += 1
		note("impact", {"pos": [snappedf((node as Node2D).global_position.x, 0.1), snappedf((node as Node2D).global_position.y, 0.1)]})
	elif node.scene_file_path == TRAIL:
		counts.trails_detached += 1
		note("trail_detached")


## Real mouse input, in window coordinates: world -> game viewport (canvas transform) -> window (the container sits at
## the root's origin at 1:1, then the window's stretch transform).
func to_window(world: Vector2) -> Vector2:
	var in_vp: Vector2 = vp.get_canvas_transform() * world
	return root.get_final_transform() * in_vp


## Mouse motion goes straight into the game's viewport, in its own coordinates (SubViewport.push_input).
func mouse_move(world: Vector2) -> Vector2:
	var p := to_window(world)
	var ev := InputEventMouseMotion.new()
	var local: Vector2 = vp.get_canvas_transform() * world
	ev.position = local
	ev.global_position = local
	vp.push_input(ev)
	return p


func click(world: Vector2) -> void:
	var p := mouse_move(world)
	await frames(1)
	var seen: Vector2 = main.get_global_mouse_position()
	for pressed: bool in [true, false]:
		var ev := InputEventMouseButton.new()
		ev.button_index = MOUSE_BUTTON_LEFT
		ev.pressed = pressed
		ev.position = p
		ev.global_position = p
		Input.parse_input_event(ev)
		await frames(2)
	note("click", {"aim": [world.x, world.y], "mouse_world_seen": [snappedf(seen.x, 0.1), snappedf(seen.y, 0.1)]})


func key(code: Key, pressed: bool) -> void:
	var ev := InputEventKey.new()
	ev.keycode = code
	ev.physical_keycode = code
	ev.pressed = pressed
	Input.parse_input_event(ev)
	vp.push_input(ev.duplicate())
	note("key", {"key": OS.get_keycode_string(code), "pressed": pressed})


## Hold D until the player reaches x (observed, not set), optionally pressing Space at jump_at.
func walk_right_to(x: float, jump_at := INF) -> void:
	key(KEY_D, true)
	var jumped := false
	var guard := 0
	while player.global_position.x < x and guard < 600:
		if not jumped and player.global_position.x >= jump_at:
			key(KEY_SPACE, true)
			await frames(12)
			key(KEY_SPACE, false)
			jumped = true
		await frames(1)
		guard += 1
	key(KEY_D, false)
	await frames(10)
	note("walked", {"player": [snappedf(player.global_position.x, 0.1), snappedf(player.global_position.y, 0.1)]})


func esc() -> void:
	key(KEY_ESCAPE, true)
	await frames(1)
	key(KEY_ESCAPE, false)
	await frames(2)
	note("paused_state", {"paused": paused})


func run() -> void:
	note("start", {"engine": Engine.get_version_info().string, "window": [root.size.x, root.size.y],
		"final_transform_scale": root.get_final_transform().get_scale().x})

	# 1. One cast into the ground: the trail flies, the impact bursts, the trail fades where it stopped.
	await fresh("first-impact")
	await click(Vector2(200, GROUND_Y))
	await seconds(1.6)
	expect("first-impact", counts.casts == 1 and counts.impacts == 1 and counts.trails_detached == 1, counts.duplicate())

	# 2. Effect A in play: the left wall at the screen edge, the wolf across the pit, then rapid casts into the ground.
	await fresh("effect-a-play")
	await click(Vector2(0, STAFF_Y))
	await seconds(1.0)
	await walk_right_to(605.0, 492.0)
	var wolf: Node2D = main.get_node("Level/Wolf")
	var defeated := {"at": -1}
	wolf.defeated.connect(func() -> void:
		defeated.at = frame
		note("wolf_defeated"))
	var tries := 0
	# The wolf is freed 0.6 s after it is defeated (wolf.gd DOWN_TIME), so check the instance before reading it.
	while is_instance_valid(wolf) and not wolf.dead and tries < 6:
		var centre := wolf.global_position + Vector2(8, -14)
		var flight: float = centre.distance_to(player.global_position + Vector2(11, -60)) / 260.0
		await click(centre + wolf.velocity * flight)
		await seconds(0.7)
		tries += 1
	expect("wolf-defeated", defeated.at >= 0, {"casts_at_wolf": tries})
	await seconds(0.8)
	var before: int = counts.impacts
	for i in 9:
		await click(Vector2(700 + 12 * i, GROUND_Y))
		await frames(7)    # with the click's 4 frames: 11 frames = 0.367 s per cast, just over the 0.35 s cooldown
	await seconds(1.2)
	expect("effect-a-play", counts.impacts - before >= 8 and counts.trails_detached == counts.casts,
		counts.merged({"rapid_impacts": counts.impacts - before}))

	# 3. Effect B: a rightward shot that times out and fades in view, a leftward shot into the wall, a pause mid-flight.
	await fresh("trail")
	await walk_right_to(300.0)
	await click(Vector2(640, STAFF_Y))
	await seconds(2.6)
	await click(Vector2(0, STAFF_Y))
	await seconds(1.8)
	await click(Vector2(640, STAFF_Y))
	await seconds(0.5)
	await esc()
	var paused_ok := paused
	await seconds(1.5)
	await esc()
	await seconds(2.4)
	counts.pauses = 1 if paused_ok and not paused else 0
	expect("trail", counts.casts == 3 and counts.trails_detached == 3 and counts.impacts == 1 and counts.pauses == 1,
		counts.duplicate())

	note("end", {"failures": failures})
	log_file.close()
	main.queue_free()
	await frames(2)
	quit(1 if failures.size() > 0 else 0)

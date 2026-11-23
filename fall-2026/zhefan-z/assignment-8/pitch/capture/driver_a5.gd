extends SceneTree
## Scripted-input capture driver for the Assignment 8 pitch film: the Assignment 5 hurt tint at revision 2b68e0a.
## Adapted by Claude Code from capture/driver.gd (the Assignment 7 film's driver): the same SubViewport harness, key
## injection and frame log, with the clip, afterimage and hitbox fields removed (they do not exist at 2b68e0a).
## Runs the real game scene, res://game/main.tscn, on an isolated copy of the project at 2b68e0a, and plays it only
## through the normal input path (Input.parse_input_event key events: D walk, Space jump). It observes positions and
## states to choose its inputs; it never moves the player or the wolf, calls take_damage(), or sets any game, shader or
## effect value. It READS the hurt-tint shader's `intensity` uniform for the frame log; hurt_tint_driver.gd sets it.
## `test_mode` is set on Main only so that a fail would not reload the scene under this script (main.gd:79, 95).
## Harness, not game: the game runs inside its own 640x360 SubViewport, shown 1:1 by a TextureRect that fills the
## window. Record with Movie Maker, windowed, one rendered frame per physics tick:
##   godot --path <capture copy> --script <this file> --write-movie <abs>/frame.png --fixed-fps 60 --resolution 1280x720
##     -- <inputs.jsonl> <frames.jsonl>
## One segment, "hurt": walk right, jump the pit, keep walking at the wolf after it starts to growl, so its lunge lands;
## then step back (A) out of its sight and stand while the invulnerability (and the tint) runs out. Quits 1 if an
## expectation fails.

const MAIN := "res://game/main.tscn"

var main: Node
var vp: SubViewport
var player: Node2D
var wolf: Node2D
var frame := 0
var seg_frame := 0
var log_file: FileAccess
var frames_file: FileAccess
var failures: Array[String] = []
var segment := ""
var seen := {}


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	log_file = FileAccess.open(args[0] if args.size() > 0 else "user://capture_inputs.jsonl", FileAccess.WRITE)
	frames_file = FileAccess.open(args[1] if args.size() > 1 else "user://capture_frames.jsonl", FileAccess.WRITE)
	process_frame.connect(_on_frame)
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


func tint() -> float:
	var m: ShaderMaterial = player.get_node("Sprite2D").material
	if m == null:
		return -1.0
	var v: Variant = m.get_shader_parameter("intensity")
	return 0.0 if v == null else float(v)   # null until hurt_tint_driver.gd first sets it


func _on_frame() -> void:
	var row := {"f": frame, "seg": segment, "sf": seg_frame, "phys": Engine.get_physics_frames()}
	if is_instance_valid(player):
		row.merge({"px": snappedf(player.global_position.x, 0.01), "py": snappedf(player.global_position.y, 0.01),
			"ps": Player.State.keys()[player.state], "php": player.hp,
			"inv": snappedf(player.invulnerable, 0.0001), "tint": snappedf(tint(), 0.0001),
			"vis": player.get_node("Sprite2D").visible})
	if is_instance_valid(wolf):
		row.merge({"wx": snappedf(wolf.global_position.x, 0.01), "ws": Wolf.State.keys()[wolf.state],
			"wface": wolf.facing, "whp": wolf.hp})
	elif segment != "":
		row["ws"] = "FREED"
	if is_instance_valid(main):
		row["cam_x"] = snappedf(main.camera.get_screen_center_position().x, 0.01)
	frames_file.store_line(JSON.stringify(row))
	_observe(row)
	frame += 1
	seg_frame += 1


func _observe(row: Dictionary) -> void:
	if segment == "" or not row.has("ps"):
		return
	if seen.has("last_php") and row.php < seen.last_php:
		note("player_hit", {"hp_before": seen.last_php, "hp_after": row.php, "wolf_state": row.get("ws", ""),
			"tint": row.tint, "player_x": row.px, "wolf_x": row.get("wx", 0.0)})
		seen.hits = seen.get("hits", 0) + 1
		seen.hit_frame = row.f
	seen.last_php = row.php
	seen.max_tint = maxf(seen.get("max_tint", 0.0), row.tint)
	if row.tint > 0.0:
		seen.tint_frames = seen.get("tint_frames", 0) + 1
		seen.last_tint_frame = row.f
	var ws: String = row.get("ws", "")
	if seen.get("last_ws", "") != ws:
		note("wolf_state", {"state": ws, "facing": row.get("wface", 0), "wolf_x": row.get("wx", 0.0), "player_x": row.px})
		seen.last_ws = ws
	var ps: String = row.ps
	if seen.get("last_ps", "") != ps:
		note("player_state", {"state": ps, "player_x": row.px, "tint": row.tint})
		seen.last_ps = ps


func note(kind: String, data := {}) -> void:
	var row := {"frame": frame, "segment": segment, "seg_frame": seg_frame, "kind": kind}
	row.merge(data)
	log_file.store_line(JSON.stringify(row))
	log_file.flush()


func frames(n: int) -> void:
	for i in n:
		await process_frame


func seconds(s: float) -> void:
	await frames(int(round(s * 60.0)))


func expect(id: String, ok: bool, data := {}) -> void:
	note("expect", {"id": id, "ok": ok}.merged(data))
	if not ok:
		failures.append(id)


func fresh(name: String) -> void:
	segment = name
	seg_frame = 0
	seen = {}
	main = load(MAIN).instantiate()
	main.test_mode = true
	vp.add_child(main)
	player = main.player
	wolf = main.get_node("Level/Wolf")
	note("segment_start", {"player": [player.global_position.x, player.global_position.y],
		"wolf": [wolf.global_position.x, wolf.global_position.y]})
	mouse_move(Vector2(main.camera.get_screen_center_position().x + 290.0, 30.0))   # crosshair parked top right
	await frames(20)


func mouse_move(world: Vector2) -> void:
	var ev := InputEventMouseMotion.new()
	var local: Vector2 = vp.get_canvas_transform() * world
	ev.position = local
	ev.global_position = local
	vp.push_input(ev)


func key(code: Key, pressed: bool) -> void:
	var ev := InputEventKey.new()
	ev.keycode = code
	ev.physical_keycode = code
	ev.pressed = pressed
	Input.parse_input_event(ev)
	vp.push_input(ev.duplicate())
	note("key", {"key": OS.get_keycode_string(code), "pressed": pressed,
		"player_x": snappedf(player.global_position.x, 0.1) if is_instance_valid(player) else -1.0})


## Hold D until the player reaches x or `until` returns true (observed, not set); press Space once at jump_at.
func walk_right(x: float, jump_at := INF, until := Callable()) -> void:
	key(KEY_D, true)
	var jumped := false
	var guard := 0
	while player.global_position.x < x and guard < 900:
		if until.is_valid() and until.call():
			break
		if not jumped and player.global_position.x >= jump_at:
			key(KEY_SPACE, true)
			await frames(14)
			key(KEY_SPACE, false)
			jumped = true
			continue
		await frames(1)
		guard += 1
	key(KEY_D, false)


func run() -> void:
	note("start", {"engine": Engine.get_version_info().string, "window": [root.size.x, root.size.y],
		"physics_ticks_per_second": Engine.physics_ticks_per_second})
	await fresh("hurt")
	var hp0: int = player.hp
	await walk_right(1100.0, 492.0, func() -> bool: return player.hp < hp0)
	await frames(20)
	key(KEY_A, true)      # step back out of the wolf's sight (to x <= 620, right of the pit), so it does not lunge again
	var guard := 0
	while player.global_position.x > 620.0 and guard < 300:
		await frames(1)
		guard += 1
	key(KEY_A, false)
	await seconds(1.0)
	expect("hurt", seen.get("hits", 0) == 1 and player.hp == hp0 - 1 and seen.get("max_tint", 0.0) > 0.5
		and seen.get("tint_frames", 0) > 0 and tint() == 0.0 and not player.is_failing,
		{"hits": seen.get("hits", 0), "player_hp": player.hp, "max_tint": seen.get("max_tint", 0.0),
		 "tint_frames": seen.get("tint_frames", 0), "hit_frame": seen.get("hit_frame", -1),
		 "last_tint_frame": seen.get("last_tint_frame", -1)})
	note("end", {"failures": failures})
	log_file.close()
	segment = ""
	main.queue_free()
	player = null
	wolf = null
	await frames(2)
	frames_file.close()
	quit(1 if failures.size() > 0 else 0)

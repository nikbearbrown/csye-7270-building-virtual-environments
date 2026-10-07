extends Node
## Film capture driver — an autoload added ONLY to an isolated copy of the game
## for the godot-gamedev film. It plays the real main scene through the keyboard
## path: synthetic InputEventKey objects pushed through Input.parse_input_event
## and flushed at once, so each press lands on the tick it was decided.
## It READS positions, velocities and states to decide when to press. It never
## writes a position, velocity, state, heart count or collision shape, and never
## calls a gameplay method. Every take asserts its outcome and exits non-zero on
## failure. Without "--take" on the command line it does nothing.
##
##   Godot --path <copy> --write-movie run-01.avi --fixed-fps 30 -- --take golden --log run-01.jsonl

const KEYS := {
	&"move_right": KEY_D, &"move_left": KEY_A, &"jump": KEY_SPACE, &"slash": KEY_J,
	&"restart": KEY_ENTER, &"pause": KEY_ESCAPE, &"mute_music": KEY_M,
	&"mute_sfx": KEY_N, &"toggle_debug": KEY_F1,
}
const DT := 1.0 / 60.0

var take := ""
var stop_after := ""
var still_dir := ""
var frame := 0
var failures: Array[String] = []
var _log: FileAccess
var _seen := {}
var _held := {}


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	var args := OS.get_cmdline_user_args()
	var log_path := ""
	for i in args.size():
		match args[i]:
			"--take": take = args[i + 1]
			"--log": log_path = args[i + 1]
			"--stop-after": stop_after = args[i + 1]
			"--stills": still_dir = args[i + 1]
	if take == "":
		set_process(false)
		return
	_log = FileAccess.open(log_path, FileAccess.WRITE)
	_row({"kind": "meta", "take": take, "stop_after": stop_after, "physics_hz": Engine.physics_ticks_per_second,
		"engine": Engine.get_version_info().string, "window": str(DisplayServer.window_get_size())})
	_run.call_deferred()


# ---------------------------------------------------------------- observation

func main() -> Node:
	return get_tree().current_scene


func rudy() -> Node:
	var m := main()
	return m.get_node_or_null("Rudy") if m else null


func level_node(path: String) -> Node:
	return main().get_node("Level1/" + path)


func _process(_delta: float) -> void:
	var m := main()
	var r := rudy()
	if r == null:
		frame += 1
		return
	var started: Array[String] = []
	var sfx: Node = get_node("/root/Sfx")
	for id in sfx.counts:
		for i in sfx.counts[id] - _seen.get(id, 0):
			started.append(String(id))
		_seen[id] = sfx.counts[id]
	var music: Node = get_node("/root/Music")
	_row({"kind": "state", "f": frame, "t": snappedf(frame / 30.0, 0.0001),
		"x": snappedf(r.global_position.x, 0.01), "y": snappedf(r.global_position.y, 0.01),
		"vx": roundi(r.velocity.x), "vy": roundi(r.velocity.y), "floor": r.is_on_floor(),
		"facing": r.facing, "pose": String(r.pose), "mode": r.Mode.keys()[r.mode],
		"hearts": r.hearts, "gear": r.Gear.keys()[r.gear], "state": m.State.keys()[m.state],
		"checkpoint": m.checkpoint_name, "paused": get_tree().paused,
		"music_db": snappedf(music.volume_db(), 0.01), "music_playing": music.player().playing,
		"music_muted": AudioServer.is_bus_mute(AudioServer.get_bus_index(&"Music")),
		"sfx_muted": AudioServer.is_bus_mute(AudioServer.get_bus_index(&"SFX")),
		"sounds": started, "camera_x": snappedf((m.get_node("Camera") as Camera2D).get_screen_center_position().x, 0.1)})
	frame += 1


func _row(d: Dictionary) -> void:
	if _log:
		_log.store_line(JSON.stringify(d))


# ---------------------------------------------------------------- input

func _key(action: StringName, pressed: bool) -> void:
	var e := InputEventKey.new()
	e.physical_keycode = KEYS[action]
	e.keycode = KEYS[action]
	e.pressed = pressed
	Input.parse_input_event(e)
	Input.flush_buffered_events()
	if pressed:
		_held[action] = true
	else:
		_held.erase(action)
	_row({"kind": "input", "f": frame, "physics_tick": Engine.get_physics_frames(), "action": String(action),
		"key": OS.get_keycode_string(KEYS[action]), "pressed": pressed,
		"x": snappedf(rudy().global_position.x, 0.01) if rudy() else null})


func press(a: StringName) -> void:
	if not _held.has(a):
		_key(a, true)


func release(a: StringName) -> void:
	if _held.has(a):
		_key(a, false)


func release_all() -> void:
	for a in _held.keys():
		_key(a, false)


## A physics-read key (move, jump, slash): pressed at the start of this tick.
func tap_tick(a: StringName, ticks := 3) -> void:
	press(a)
	await ticks_(ticks)
	release(a)


## A process-read key (Enter, Esc, M, N, F1): pressed before this frame's _process.
func tap_frame(a: StringName) -> void:
	await get_tree().process_frame
	press(a)
	await get_tree().process_frame
	await get_tree().process_frame
	release(a)


func ticks_(n: int) -> void:
	for i in n:
		await get_tree().physics_frame


func frames_(n: int) -> void:
	for i in n:
		await get_tree().process_frame


func until(cond: Callable, label: String, max_ticks := 1800) -> bool:
	for i in max_ticks:
		if cond.call():
			_row({"kind": "mark", "f": frame, "label": label})
			return true
		await get_tree().physics_frame
	check(false, "timed out: " + label)
	return false


func check(ok: bool, what: String) -> void:
	_row({"kind": "check", "f": frame, "ok": ok, "what": what})
	if not ok:
		failures.append(what)
		push_error("film driver: FAILED " + what)


func mark(label: String) -> void:
	_row({"kind": "mark", "f": frame, "label": label})


# ---------------------------------------------------------------- prediction

## Ticks until Rudy's soles, jumping now at full run speed, first come down
## through the goblin's top; and the gap between them then. Rudy's integration
## is copied from rudy.gd (gravity before the move); the goblin's patrol from
## goblin.gd. Read-only: nothing is written.
func stomp_gap(g: Node) -> float:
	var r := rudy()
	var rx: float = r.global_position.x
	var vx: float = r.velocity.x
	var y := 0.0
	var vy: float = -r.jump_velocity
	var gx: float = g.global_position.x
	var gf: int = g.facing
	var start: float = g.get("_start_x")
	var top: float = Goblin.HEIGHT
	for k in 120:
		if k > 0:
			vy += (r.fall_gravity if vy >= 0.0 else r.gravity) * DT
		y -= vy * DT # height above the ground
		rx += vx * DT
		gx += gf * g.speed * DT
		if gx >= start + g.patrol_distance:
			gf = -1
		elif gx <= start:
			gf = 1
		if vy > 0.0 and y < top:
			return gx - rx
	return INF


# ---------------------------------------------------------------- takes

func _run() -> void:
	await frames_(2)
	match take:
		"golden":
			await _golden()
		"costs":
			await _costs()
		"controls":
			await _controls()
		"outline":
			await _outline()
		_:
			check(false, "unknown take " + take)
	release_all()
	await frames_(2)
	_row({"kind": "result", "f": frame, "failures": failures, "ok": failures.is_empty()})
	_log.close()
	_log = null
	print("film driver: take %s %s (%d frames)" % [take, "OK" if failures.is_empty() else "FAILED " + str(failures), frame])
	get_tree().quit(0 if failures.is_empty() else 1)


func _enter_from_title(hold_frames: int) -> void:
	check(main().state == main().State.TITLE, "opens on the title")
	await frames_(hold_frames)
	await tap_frame(&"restart")
	await until(func() -> bool: return main().state == main().State.PLAYING, "Enter starts play")


## Full level, all kills, no damage, to the end card; Enter plays again.
func _golden() -> void:
	await _enter_from_title(75)
	await ticks_(12)
	press(&"move_right")
	var done := {}
	var ga: Node = level_node("Enemies/GoblinA")
	var gb: Node = level_node("Enemies/GoblinB")
	var gc: Node = level_node("Enemies/GoblinC")
	while main().state == main().State.PLAYING:
		var r := rudy()
		var rx: float = r.global_position.x
		var ground: bool = r.is_on_floor()
		if ground and not done.has("spikesA") and rx >= 880.0:
			done.spikesA = true
			mark("jump over SpikesA")
			tap_tick(&"jump", 2)
		elif ground and done.has("spikesA") and not ga.dead and rx > 1150.0 and absf(r.velocity.x - r.run_speed) < 1.0 and absf(stomp_gap(ga)) < 12.0:
			mark("jump to stomp GoblinA")
			tap_tick(&"jump", 2)
			await ticks_(3)
		elif r.gear == r.Gear.SWORD and not gb.dead and gb.global_position.x - rx > 0.0 and gb.global_position.x - rx <= 115.0 and not r.is_slashing():
			mark("slash GoblinB")
			tap_tick(&"slash", 2)
			await ticks_(3)
		elif ground and not done.has("cliff1") and rx >= 4235.0 and rx < 4300.0:
			done.cliff1 = true
			mark("jump cliff 1")
			tap_tick(&"jump", 2)
		elif ground and not done.has("spikesB") and rx >= 4960.0 and rx < 5100.0:
			done.spikesB = true
			mark("jump over SpikesB")
			tap_tick(&"jump", 2)
		elif r.gear == r.Gear.SWORD and not gc.dead and gc.global_position.x - rx > 0.0 and gc.global_position.x - rx <= 115.0 and not r.is_slashing():
			mark("slash GoblinC")
			tap_tick(&"slash", 2)
			await ticks_(3)
		elif ground and not done.has("cliff2") and rx >= 6335.0 and rx < 6400.0:
			done.cliff2 = true
			mark("jump cliff 2")
			tap_tick(&"jump", 2)
		if stop_after == "slashB" and gb.dead:
			await ticks_(70)
			release_all()
			check(rudy().hearts == 3 and ga.dead and gb.dead, "stomp A and slash B, no damage")
			return
		await ticks_(1)
	release(&"move_right")
	check(main().state == main().State.COMPLETE, "reached the teleport circle")
	check(ga.dead and gb.dead and gc.dead, "all three goblins defeated")
	check(rudy().hearts == 3, "no heart lost")
	var hud: Node = main().get_node("Hud")
	await until(func() -> bool: return hud.is_showing_end_card(), "end card shown")
	await frames_(60)
	var old_id := main().get_instance_id()
	await tap_frame(&"restart")
	await until(func() -> bool: return main() != null and main().get_instance_id() != old_id and rudy() != null, "Enter plays again")
	await frames_(45)
	check(main().state == main().State.PLAYING and not main().get_node("Hud").is_showing_title(), "replay starts in play, no title")


## A spike hit, the gear knocked away, a fall to the waystone, the last heart.
func _costs() -> void:
	await _enter_from_title(30)
	await ticks_(10)
	press(&"move_right")
	await until(func() -> bool: return rudy().mode == rudy().Mode.HURT, "walks into SpikesA")
	check(rudy().hearts == 2, "spikes cost a heart (3 -> 2)")
	release(&"move_right")
	await until(func() -> bool: return rudy().mode == rudy().Mode.PLAY, "control back after the knockback")
	press(&"move_left")
	await until(func() -> bool: return rudy().global_position.x < 760.0, "backs off to x < 760")
	release(&"move_left")
	await ticks_(4)
	press(&"move_right")
	await until(func() -> bool: return rudy().is_on_floor() and rudy().global_position.x >= 880.0, "run-up")
	mark("jump over SpikesA")
	await tap_tick(&"jump", 2)
	var ga: Node = level_node("Enemies/GoblinA")
	var gb: Node = level_node("Enemies/GoblinB")
	await until(func() -> bool: return rudy().is_on_floor() and rudy().global_position.x > 1150.0, "landed past SpikesA")
	await until(func() -> bool: return rudy().is_on_floor() and absf(rudy().velocity.x - rudy().run_speed) < 1.0 and absf(stomp_gap(ga)) < 12.0, "stomp window on GoblinA")
	await tap_tick(&"jump", 2)
	await until(func() -> bool: return ga.dead, "GoblinA stomped")
	await until(func() -> bool: return rudy().gear == rudy().Gear.SWORD, "sword picked up")
	await until(func() -> bool: return rudy().mode == rudy().Mode.HURT, "runs into GoblinB without slashing")
	check(rudy().gear == rudy().Gear.NONE and rudy().hearts == 2, "the hit takes the gear, not a heart")
	release(&"move_right")
	await until(func() -> bool: return rudy().mode == rudy().Mode.PLAY, "control back")
	press(&"move_left")
	await until(func() -> bool: return gb.global_position.x - rudy().global_position.x >= 420.0, "backs off from GoblinB")
	release(&"move_left")
	await ticks_(4)
	press(&"move_right")
	await until(func() -> bool: return rudy().is_on_floor() and absf(rudy().velocity.x - rudy().run_speed) < 1.0 and absf(stomp_gap(gb)) < 12.0, "stomp window on GoblinB")
	await tap_tick(&"jump", 2)
	await until(func() -> bool: return gb.dead, "GoblinB stomped")
	var ws: Node = level_node("Waystone")
	await until(func() -> bool: return ws.lit, "waystone lit")
	await until(func() -> bool: return main().state == main().State.DYING, "runs off cliff 1")
	release(&"move_right")
	check(rudy().hearts == 1, "the fall costs a heart (2 -> 1)")
	await until(func() -> bool: return main().state == main().State.PLAYING, "back in play")
	check(absf(rudy().global_position.x - 4120.0) < 1.0 and rudy().hearts == 1, "respawned at the waystone with 1 heart")
	await ticks_(20)
	press(&"move_left")
	await until(func() -> bool: return rudy().mode == rudy().Mode.DEFEATED, "walks into GoblinB with the last heart")
	release(&"move_left")
	check(rudy().hearts == 0, "last heart gone")
	await until(func() -> bool: return main().state == main().State.PLAYING, "level starts over")
	check(absf(rudy().global_position.x - 300.0) < 1.0 and rudy().hearts == 3 and not ws.lit, "back at the opening, 3 hearts, waystone dark")
	await frames_(50)


## Turning on the spot, poses, a held jump, pause, and the two mutes.
func _controls() -> void:
	await frames_(30)
	await tap_frame(&"toggle_debug")
	await _enter_from_title(30)
	await ticks_(30)
	mark("tap left")
	await tap_tick(&"move_left", 3)
	await ticks_(40)
	check(rudy().facing == -1 and absf(rudy().global_position.x - 300.0) < 1.0, "a tap turns him on the spot")
	mark("tap right")
	await tap_tick(&"move_right", 3)
	await ticks_(40)
	mark("run")
	press(&"move_right")
	await ticks_(30)
	release(&"move_right")
	await until(func() -> bool: return rudy().velocity.x == 0.0, "stopped")
	await ticks_(30)
	mark("jump in place")
	await tap_tick(&"jump", 2)
	await until(func() -> bool: return rudy().is_on_floor() and rudy().velocity.y == 0.0, "landed")
	await ticks_(30)
	mark("jump held for 1.5 s")
	var jumps_before: int = get_node("/root/Sfx").count(&"jump")
	press(&"jump")
	await ticks_(90)
	release(&"jump")
	check(get_node("/root/Sfx").count(&"jump") == jumps_before + 1, "a held key jumps once, one sound")
	await ticks_(30)
	mark("running jump")
	press(&"move_right")
	await until(func() -> bool: return rudy().global_position.x >= 860.0, "run-up to the spikes")
	await tap_tick(&"jump", 2)
	await until(func() -> bool: return rudy().is_on_floor() and rudy().velocity.y == 0.0, "landed")
	release(&"move_right")
	check(rudy().hearts == 3, "the running jump clears SpikesA")
	await ticks_(40)
	mark("pause")
	await tap_frame(&"pause")
	check(get_tree().paused, "Esc pauses")
	await frames_(60)
	await tap_frame(&"pause")
	check(not get_tree().paused, "Esc resumes")
	await frames_(30)
	mark("music muted")
	await tap_frame(&"mute_music")
	await frames_(15)
	await tap_tick(&"jump", 2)
	await frames_(40)
	await tap_frame(&"mute_music")
	await frames_(30)
	mark("effects muted")
	await tap_frame(&"mute_sfx")
	await frames_(15)
	var before: int = get_node("/root/Sfx").count(&"jump")
	await tap_tick(&"jump", 2)
	await until(func() -> bool: return not rudy().is_on_floor(), "silent jump leaves the ground")
	check(get_node("/root/Sfx").count(&"jump") == before + 1, "muted, the jump still calls Sfx.play once")
	await frames_(40)
	await tap_frame(&"mute_sfx")
	await frames_(20)
	await tap_frame(&"toggle_debug")
	await frames_(20)


## Diagnostic stills: the same frame with the outline at its source width and at 0.
func _outline() -> void:
	await _enter_from_title(10)
	press(&"move_right")
	await until(func() -> bool: return rudy().global_position.x >= 640.0, "walks onto the wheat")
	release(&"move_right")
	await until(func() -> bool: return rudy().velocity.x == 0.0, "stopped")
	await frames_(40)
	await _still("outline-on")
	var mat: ShaderMaterial = load("res://systems/art/outline.tres")
	var width: float = mat.get_shader_parameter("width")
	check(width == 8.0, "outline.tres width is 8")
	mat.set_shader_parameter("width", 0.0)
	mark("DIAGNOSTIC: outline width set to 0 at runtime")
	await frames_(3)
	await _still("outline-off")
	mat.set_shader_parameter("width", width)
	await frames_(3)


func _still(label: String) -> void:
	await RenderingServer.frame_post_draw
	var img := get_viewport().get_texture().get_image()
	var path := still_dir.path_join(label + ".png")
	img.save_png(path)
	_row({"kind": "still", "f": frame, "path": path, "size": str(img.get_size()), "x": rudy().global_position.x})

extends SceneTree
## Scripted-input capture driver for the Assignment 7 film (Brutalist godot-waikthrough capture contract, used by
## godot-gamedev). Adapted from the Assignment 6 film's driver (docs/a6/youtube/claude-liam-walker-magic-particles-gamedev/
## capture/driver.gd). Runs the real game scene, res://game/main.tscn, on an isolated copy of the project at the film's
## revision (ad7935f; capture/run-01 was made with the earlier version of this file at f860fed), and plays it only through
## the normal input path: Input.parse_input_event with key events (A/D walk,
## Space jump) and mouse events (motion to the aim point, then a left click to cast). It observes positions and states to
## choose its inputs; it never moves the player or the wolf, calls cast(), take_damage() or play(), or sets any game,
## clip or effect value. `test_mode` is set on Main only so that a fail would not reload the scene under this script
## (main.gd:79, 95).
## Harness, not game: the game runs inside its own 640x360 SubViewport, shown 1:1 by a TextureRect that fills the
## window (the Assignment 6 method: injected mouse motion reaches the aim without moving the OS cursor). Keys go through
## Input.parse_input_event (the actions the player reads) and are also pushed into the game's viewport. The SubViewport
## is pausable, so the game pauses exactly as in a normal run. No overlay is drawn: the game frames are untouched.
## Record with Movie Maker, windowed, one rendered frame per physics tick:
##   godot --path <capture copy> --script <this file> --write-movie <abs>/frame.png --fixed-fps 60 --resolution 1280x720
##     -- <inputs.jsonl> <frames.jsonl>
## Writes one JSON line per input, observed event and expectation to the first user argument, and one line per rendered
## frame (the state the frame shows: player and wolf state, position, clip frame, hitbox, ghosts, fireballs alive) to the
## second. Quits 1 if an expectation fails, so an exhausted run is never taken as success.
## Segments: run, lunges, cancel (a fireball hit in GROWL) as in run-01; then lunge_hit (a hit in LUNGE) and recover_hit
## (a hit in RECOVER), added for run-02. A wolf hit is resolved at the start of a physics tick, before the wolf's own
## update, so the phase a hit lands in is the state the wolf ended the previous tick in: at 60 fps one rendered frame is
## one tick, so it is the previous frame's state (logged as "wolf_hit" with prev_state, the state on the hit tick, the
## clip frame and the ticks since GROWL entry). The click times after the sighting (LUNGE_HIT_DELAY, RECOVER_HIT_DELAY)
## were found by trial runs of this file, headless, with the optional user arguments
##   only=lunge_hit,recover_hit lunge_delay=<frames> recover_delay=<frames>
## (trials only; the recorded run passes just the two log paths and uses the constants below).

const MAIN := "res://game/main.tscn"
const GHOST := "LungeGhost"
## Frames from the sighting (the wolf's GROWL entry) to the click, found by trial runs (see the header).
const LUNGE_HIT_DELAY := 14
const RECOVER_HIT_DELAY := 40

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
var counts := {}
var seen := {}          # per segment: observations collected frame by frame
var opts := {}          # optional key=value user arguments (trial runs only)


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	log_file = FileAccess.open(args[0] if args.size() > 0 else "user://capture_inputs.jsonl", FileAccess.WRITE)
	frames_file = FileAccess.open(args[1] if args.size() > 1 else "user://capture_frames.jsonl", FileAccess.WRITE)
	for a in args.slice(2):
		var kv := a.split("=", true, 1)
		if kv.size() == 2:
			opts[kv[0]] = kv[1]
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


## One line per rendered frame: the state that frame shows (process_frame is emitted after this frame's physics ticks
## and before it is drawn). `frame` counts from the first frame, as Movie Maker numbers its PNGs (checked in CAPTURE.md).
func _on_frame() -> void:
	var row := {"f": frame, "seg": segment, "sf": seg_frame, "phys": Engine.get_physics_frames()}
	if is_instance_valid(player):
		row.merge({"px": snappedf(player.global_position.x, 0.01), "py": snappedf(player.global_position.y, 0.01),
			"ps": Player.State.keys()[player.state], "pclip": str(player.anim.assigned_animation),
			"pfr": player.sprite.frame, "php": player.hp})
	if is_instance_valid(wolf):
		row.merge({"wx": snappedf(wolf.global_position.x, 0.01), "ws": Wolf.State.keys()[wolf.state],
			"wface": wolf.facing, "wclip": str(wolf.anim.assigned_animation),
			"wcf": roundi(wolf.anim.current_animation_position * 60.0), "mon": wolf.lunge_hitbox.monitoring,
			"whp": wolf.hp})
	elif segment != "":
		row["ws"] = "FREED"
	if is_instance_valid(main):
		var g := 0
		var fb := 0
		for c in main.get_node("Level").get_children():
			if str(c.name).begins_with(GHOST):
				g += 1
			elif c is Fireball:
				fb += 1
		row["ghosts"] = g
		row["fireballs"] = fb
		row["cam_x"] = snappedf(main.camera.get_screen_center_position().x, 0.01)
	frames_file.store_line(JSON.stringify(row))
	_observe(row)
	frame += 1
	seg_frame += 1


func _observe(row: Dictionary) -> void:
	if segment == "" or not row.has("ws"):
		return
	var ws: String = row.ws
	if ws == "GROWL" and seen.get("last_ws", "") != "GROWL":
		seen.growl_frame = row.f
	if row.has("whp") and seen.has("last_whp") and row.whp < seen.last_whp:
		var hit := {"prev_state": seen.get("last_ws", ""), "state": ws, "clip_frame": row.get("wcf", -1),
			"since_growl": row.f - seen.get("growl_frame", row.f), "hp_before": seen.last_whp, "hp_after": row.whp,
			"monitoring": row.get("mon", false), "wolf_x": row.get("wx", 0.0), "player_x": row.get("px", 0.0)}
		note("wolf_hit", hit)
		seen["hits"] = seen.get("hits", []) + [hit]
	if row.has("whp"):
		seen.last_whp = row.whp
	if ws == "LUNGE":
		seen.lunge_frames = seen.get("lunge_frames", 0) + 1
	if ws == "RECOVER":
		seen.recover_frames = seen.get("recover_frames", 0) + 1
		if seen.get("last_ws", "") != "RECOVER":
			seen.recover_entry_clip_frame = row.get("wcf", -1)
	if seen.get("last_ws", "") != ws:
		note("wolf_state", {"state": ws, "facing": row.get("wface", 0), "clip_frame": row.get("wcf", -1),
			"wolf_x": row.get("wx", 0.0), "player_x": row.get("px", 0.0)})
		seen.last_ws = ws
		seen[ws + "_count"] = seen.get(ws + "_count", 0) + 1
		if ws == "LUNGE":
			seen["lunge_facings"] = seen.get("lunge_facings", []) + [row.wface]
	if row.get("mon", false):
		seen.monitoring_frames = seen.get("monitoring_frames", 0) + 1
	seen.max_ghosts = maxi(seen.get("max_ghosts", 0), row.get("ghosts", 0))
	if row.has("ps"):
		var ps: String = row.ps
		if seen.get("last_ps", "") != ps:
			note("player_state", {"state": ps, "clip": row.pclip, "sprite_frame": row.pfr, "player_x": row.px})
			seen.last_ps = ps
			seen["p_" + ps] = seen.get("p_" + ps, 0) + 1


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
	if is_instance_valid(main):
		segment = ""
		main.queue_free()
		player = null
		wolf = null
		await frames(2)
	segment = name
	seg_frame = 0
	seen = {}
	counts = {"casts": 0}
	main = load(MAIN).instantiate()
	main.test_mode = true
	vp.add_child(main)
	player = main.player
	wolf = main.get_node("Level/Wolf")
	player.cast_fired.connect(func(o: Vector2, d: Vector2) -> void:
		counts.casts += 1
		note("cast_fired", {"origin": [snappedf(o.x, 0.1), snappedf(o.y, 0.1)], "dir": [snappedf(d.x, 0.001), snappedf(d.y, 0.001)],
			"wolf_state": Wolf.State.keys()[wolf.state] if is_instance_valid(wolf) else "-"}))
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


func click(world: Vector2) -> void:
	mouse_move(world)
	await frames(1)
	var seen_aim: Vector2 = main.get_global_mouse_position()
	var p: Vector2 = root.get_final_transform() * (vp.get_canvas_transform() * world)
	note("click", {"aim": [snappedf(world.x, 0.1), snappedf(world.y, 0.1)], "mouse_world_seen": [snappedf(seen_aim.x, 0.1), snappedf(seen_aim.y, 0.1)],
		"wolf_state": Wolf.State.keys()[wolf.state] if is_instance_valid(wolf) else "-"})
	for pressed: bool in [true, false]:
		var ev := InputEventMouseButton.new()
		ev.button_index = MOUSE_BUTTON_LEFT
		ev.pressed = pressed
		ev.position = p
		ev.global_position = p
		Input.parse_input_event(ev)
		await frames(2)


func key(code: Key, pressed: bool) -> void:
	var ev := InputEventKey.new()
	ev.keycode = code
	ev.physical_keycode = code
	ev.pressed = pressed
	Input.parse_input_event(ev)
	vp.push_input(ev.duplicate())
	note("key", {"key": OS.get_keycode_string(code), "pressed": pressed,
		"player_x": snappedf(player.global_position.x, 0.1) if is_instance_valid(player) else -1.0})


func tap(code: Key, hold: int) -> void:
	key(code, true)
	await frames(hold)
	key(code, false)


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


func wolf_is(s: String) -> bool:
	return is_instance_valid(wolf) and Wolf.State.keys()[wolf.state] == s


func wait_wolf(s: String, limit: int) -> int:
	var n := 0
	while not wolf_is(s) and n < limit:
		await frames(1)
		n += 1
	return n


func wants(seg: String) -> bool:
	return not opts.has("only") or seg in str(opts.only).split(",")


func run() -> void:
	note("start", {"engine": Engine.get_version_info().string, "window": [root.size.x, root.size.y],
		"physics_ticks_per_second": Engine.physics_ticks_per_second, "options": opts})
	if wants("run"):
		await seg_run()
	if wants("lunges"):
		await seg_lunges()
	if wants("cancel"):
		await seg_cancel()
	if wants("lunge_hit"):
		await seg_lunge_hit(int(opts.get("lunge_delay", LUNGE_HIT_DELAY)))
	if wants("recover_hit"):
		await seg_recover_hit(int(opts.get("recover_delay", RECOVER_HIT_DELAY)))

	note("end", {"failures": failures})
	log_file.close()
	segment = ""
	main.queue_free()
	player = null
	wolf = null
	await frames(2)
	frames_file.close()
	quit(1 if failures.size() > 0 else 0)


func seg_run() -> void:
	# 1. The run cycle in play: run, stop, run, jump the pit, land, run, stop. Torches and embers behind.
	await fresh("run")
	await walk_right(220.0)
	await seconds(0.7)
	await walk_right(640.0, 492.0)
	await seconds(1.0)
	expect("run", seen.get("p_RUN", 0) >= 3 and seen.get("p_RISE", 0) >= 1 and seen.get("p_FALL", 0) >= 1
		and player.global_position.x > 600.0 and not player.is_failing and not wolf_is("GROWL") and seen.get("GROWL_count", 0) == 0,
		{"run_entries": seen.get("p_RUN", 0), "rise": seen.get("p_RISE", 0), "fall": seen.get("p_FALL", 0),
		 "player_x": snappedf(player.global_position.x, 0.1)})


func seg_lunges() -> void:
	# 2. Both facings: stop where the wolf first sees the mage, step back so the leftward lunge misses, then run right
	#    past the recovering wolf; it growls again, turns to follow her and lunges to the right.
	await fresh("lunges")
	await walk_right(1100.0, 492.0, func() -> bool: return wolf_is("GROWL"))
	note("sighted", {"dx": snappedf(wolf.global_position.x - player.global_position.x, 0.01)})
	await frames(2)
	await tap(KEY_A, 24)
	await wait_wolf("RECOVER", 120)
	await walk_right(1100.0, INF, func() -> bool: return wolf_is("LUNGE") and wolf.facing > 0)
	await wait_wolf("RECOVER", 120)
	await wait_wolf("PATROL", 120)
	await seconds(0.5)
	var facings: Array = seen.get("lunge_facings", [])
	expect("lunges", facings.size() >= 2 and facings[0] == -1 and facings.has(1) and seen.get("max_ghosts", 0) >= 3
		and seen.get("RECOVER_count", 0) >= 2 and not player.is_failing,
		{"lunge_facings": facings, "max_ghosts_alive": seen.get("max_ghosts", 0), "recovers": seen.get("RECOVER_count", 0),
		 "player_hp": player.hp})


func seg_cancel() -> void:
	# 3. An early cast: the moment the wolf starts to growl, a click on its body; the fireball lands during the growl and
	#    the lunge is cancelled (CHANGE-BRIEF "Behaviour change"). Then step back out of sight.
	await fresh("cancel")
	await walk_right(1100.0, 492.0, func() -> bool: return wolf_is("GROWL"))
	var dx: float = wolf.global_position.x - player.global_position.x
	note("sighted", {"dx": snappedf(dx, 0.01)})
	var hp_before: int = wolf.hp
	await click(wolf.global_position + Vector2(8.0 * wolf.facing, -14.0))
	var growl_frames := 0
	while wolf_is("GROWL") and growl_frames < 60:
		await frames(1)
		growl_frames += 1
	var after: String = Wolf.State.keys()[wolf.state]
	note("growl_ended", {"next_state": after, "wolf_hp": wolf.hp})
	if player.global_position.x > 640.0:
		await tap(KEY_A, 30)
	await wait_wolf("PATROL", 90)
	var h := one_hit()
	expect("cancel", counts.casts == 1 and after == "RECOVER" and wolf.hp == hp_before - 1 and seen.get("LUNGE_count", 0) == 0
		and seen.get("monitoring_frames", 0) == 0 and not h.is_empty() and h.prev_state == "GROWL" and h.state == "RECOVER"
		and h.clip_frame == 53,
		{"casts": counts.casts, "state_after_growl": after, "wolf_hp": wolf.hp, "lunges": seen.get("LUNGE_count", 0),
		 "monitoring_frames": seen.get("monitoring_frames", 0), "sight_dx": snappedf(dx, 0.01), "hit": h})
	await seconds(0.6)


## Walk and jump the pit as in the cancel segment, stop at the sighting, step back (A held 24 frames from the second frame
## after the sighting, as in the lunges segment) and click on the wolf `delay` frames after the sighting. Returns the
## wolf's HP before the hit.
func sight_step_back_and_click(delay: int) -> int:
	await walk_right(1100.0, 492.0, func() -> bool: return wolf_is("GROWL"))
	note("sighted", {"dx": snappedf(wolf.global_position.x - player.global_position.x, 0.01)})
	var hp_before: int = wolf.hp
	var t := 0
	await frames(2)
	t += 2
	key(KEY_A, true)
	var a_held := true
	while t < delay:
		await frames(1)
		t += 1
		if a_held and t >= 26:
			key(KEY_A, false)
			a_held = false
	await click(wolf.global_position + Vector2(8.0 * wolf.facing, -14.0))
	t += 5
	while a_held and t < 26:
		await frames(1)
		t += 1
	if a_held:
		key(KEY_A, false)
	return hp_before


func one_hit() -> Dictionary:
	var hits: Array = seen.get("hits", [])
	return hits[0] if hits.size() == 1 else {}


func seg_lunge_hit(delay: int) -> void:
	# 4. A hit in LUNGE: the lunge is committed (CHANGE-BRIEF "Behaviour change"): the wolf loses HP and keeps dashing
	#    for its full 22 ticks, then recovers as usual.
	await fresh("lunge_hit")
	var hp_before := await sight_step_back_and_click(delay)
	await wait_wolf("PATROL", 150)
	await seconds(0.5)
	var h := one_hit()
	expect("lunge_hit", counts.casts == 1 and not h.is_empty() and h.prev_state == "LUNGE" and h.state == "LUNGE"
		and wolf.hp == hp_before - 1 and seen.get("LUNGE_count", 0) == 1 and seen.get("lunge_frames", 0) == 22
		and seen.get("RECOVER_count", 0) == 1 and seen.get("recover_entry_clip_frame", -1) == 53 and not player.is_failing,
		{"delay": delay, "casts": counts.casts, "hit": h, "wolf_hp": wolf.hp, "lunge_frames": seen.get("lunge_frames", 0),
		 "recover_entry_clip_frame": seen.get("recover_entry_clip_frame", -1), "player_hp": player.hp})


func seg_recover_hit(delay: int) -> void:
	# 5. A hit in RECOVER: only HP changes; the wolf stands for its full 36 ticks and the clip plays on.
	await fresh("recover_hit")
	var hp_before := await sight_step_back_and_click(delay)
	await wait_wolf("PATROL", 150)
	await seconds(0.5)
	var h := one_hit()
	expect("recover_hit", counts.casts == 1 and not h.is_empty() and h.prev_state == "RECOVER" and h.state == "RECOVER"
		and wolf.hp == hp_before - 1 and seen.get("LUNGE_count", 0) == 1 and seen.get("lunge_frames", 0) == 22
		and seen.get("recover_frames", 0) == 36 and not player.is_failing,
		{"delay": delay, "casts": counts.casts, "hit": h, "wolf_hp": wolf.hp, "recover_frames": seen.get("recover_frames", 0),
		 "player_hp": player.hp})

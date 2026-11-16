extends SceneTree
## Assignment 7 pin (CHANGE-BRIEF "Pin first"): today's player and wolf behaviour, physics tick by physics tick, recorded
## before any A7 change. From fall-2026/zhefan-z/assignment-7/ in Git Bash:
##   PIN_MODE=record ./scripts/run-test.sh test_pin_behaviour.gd 60   # writes logs/pin/<scenario>.json
##   ./scripts/run-test.sh test_pin_behaviour.gd 30                   # check (the default); also 60 and 144
## Check mode compares each tick with logs/pin/<scenario>.json and prints the first differing tick and field.
## Prints one JSON line per check and "WALKER TESTS: N checks / F failures"; exit code 1 on any failure. Lines with
## "observation" instead of "status" are printed, not asserted (phase lengths, what a hit does in each phase).
##
## Driven through the real game loop: game/main.tscn is instanced, and every input is a real event through
## Input.parse_input_event (D / Space keys; mouse motion to the aim point, then a left click). Nothing here calls a player
## or wolf function or writes their state; the only writes are the two start positions, before the first tick, as the
## earlier suites do (tests/test_fireball_impact.gd:112).
##
## Timing. Tick 0 is the first physics tick of the new scene. An event scheduled for tick N is parsed in the process
## frame that follows tick N-1 (or, for N = 0, the frame that adds the scene); the engine flushes it at the start of the
## next frame, before tick N. At --fixed-fps 30 a frame runs two ticks, so only even ticks are reachable from a process
## frame: every scheduled tick is even, and a check fails if an event goes out late.
## Sampling. A Sampler with process_physics_priority 1000 records after Player and Wolf in each tick's _physics_process:
## a fireball hit (body_entered, flushed before the tick's scripts) shows in that tick; a set_deferred value such as the
## hitbox's monitoring = false on RECOVER (features/wolf/wolf.gd:110) shows from the next tick.
## Comparison: positions and velocities to 0.01 (px, px/s); states, HP and monitoring exactly.

const GROUND_TOP := 327.0
const EPS := 0.01
const FIELDS := ["p_state", "p_pos", "p_vel", "w_state", "w_pos", "w_hp", "w_mon"]


## Records one row per physics tick: player state, position, velocity; wolf state, position, HP, LungeHitbox.monitoring.
class Sampler extends Node:
	var ticks := 0
	var rows: Array[Dictionary] = []
	var player: Player
	var wolf: Wolf
	var hitbox: Area2D

	func _init() -> void:
		process_physics_priority = 1000

	func _physics_process(_delta: float) -> void:
		var row := {"t": ticks, "p_state": Player.State.keys()[player.state],
			"p_pos": v2(player.global_position), "p_vel": v2(player.velocity)}
		if is_instance_valid(wolf):
			row.merge({"w_state": Wolf.State.keys()[wolf.state], "w_pos": v2(wolf.global_position), "w_hp": wolf.hp,
				"w_mon": hitbox.monitoring})
		else:
			row.merge({"w_state": "FREED", "w_pos": null, "w_hp": null, "w_mon": null})
		rows.append(row)
		ticks += 1

	static func v2(v: Vector2) -> Array:
		return [snappedf(v.x, 0.0001), snappedf(v.y, 0.0001)]


var mode := "check"
var fps := 0
var pin_dir := ""
var main: Node
var sampler: Sampler
var results: Array[Dictionary] = []
var failures := 0


func _initialize() -> void:
	call_deferred("run")


func check(id: String, passed: bool, observed: Dictionary) -> void:
	results.append({"id": id, "status": "PASS" if passed else "FAIL", "observed": observed})
	if not passed:
		failures += 1
	print(JSON.stringify(results.back()))


func observe(id: String, observed: Dictionary) -> void:
	print(JSON.stringify({"id": id, "observation": observed}))


## Each scenario: the player's and the wolf's start x, the trace length in ticks, and the input events by tick.
## Event kinds: ["key", tick, keycode, pressed], ["aim", tick, world point], ["click", tick, pressed].
## Player 680 / wolf 800: the wolf sees her at once (dx 120 = SIGHT_X, wolf.gd:19) and its lunge (77 px) stops short of
## her, so the three phase-hit scenarios differ only in when the fireball lands.
func scenarios() -> Array[Dictionary]:
	return [
		{"name": "walk_right_stop", "player_x": 200.0, "wolf_x": 860.0, "length": 120, "events": [
			["key", 10, KEY_D, true], ["key", 70, KEY_D, false]]},
		{"name": "jump", "player_x": 200.0, "wolf_x": 860.0, "length": 90, "events": [
			["key", 10, KEY_SPACE, true], ["key", 60, KEY_SPACE, false]]},
		{"name": "cast", "player_x": 200.0, "wolf_x": 860.0, "length": 90, "events": [
			["aim", 10, Vector2(300, 340)], ["click", 10, true], ["click", 14, false]]},
		{"name": "take_lunge", "player_x": 780.0, "wolf_x": 860.0, "length": 180, "events": []},
		{"name": "hit_growl", "player_x": 680.0, "wolf_x": 800.0, "length": 150, "events": [
			["aim", 4, Vector2(790, 313)], ["click", 4, true], ["click", 8, false]]},
		{"name": "hit_lunge", "player_x": 680.0, "wolf_x": 800.0, "length": 150, "events": [
			["aim", 24, Vector2(740, 313)], ["click", 24, true], ["click", 28, false]]},
		{"name": "hit_recover", "player_x": 680.0, "wolf_x": 800.0, "length": 150, "events": [
			["aim", 56, Vector2(712, 313)], ["click", 56, true], ["click", 60, false]]},
		# The pin ends 32 ticks after the killing hit: the wolf is freed by a SceneTree timer on the process clock
		# (wolf.gd:150), so the tick it leaves the tree depends on the frame rate. The tail runs on unpinned and
		# reports that tick as an observation.
		{"name": "kill", "player_x": 680.0, "wolf_x": 800.0, "length": 75, "tail": 60, "events": [
			["aim", 4, Vector2(790, 313)], ["click", 4, true], ["click", 8, false],
			["aim", 30, Vector2(740, 313)], ["click", 30, true], ["click", 34, false]]},
	]


func key(code: Key, pressed: bool) -> void:
	var ev := InputEventKey.new()
	ev.keycode = code
	ev.physical_keycode = code
	ev.pressed = pressed
	Input.parse_input_event(ev)


## World -> screen through the camera, as tests/test_fireball_impact.gd:126-132 does.
func screen_of(world: Vector2) -> Vector2:
	return world - Vector2(main.camera.get_screen_center_position().x - 320.0, 0.0)


var _mouse_screen := Vector2.ZERO


func send(e: Array) -> void:
	match e[0]:
		"key":
			key(e[2], e[3])
		"aim":
			_mouse_screen = screen_of(e[2])
			var motion := InputEventMouseMotion.new()
			motion.position = _mouse_screen
			motion.global_position = _mouse_screen
			Input.parse_input_event(motion)
		"click":
			var ev := InputEventMouseButton.new()
			ev.button_index = MOUSE_BUTTON_LEFT
			ev.pressed = e[2]
			ev.position = _mouse_screen
			ev.global_position = _mouse_screen
			Input.parse_input_event(ev)


func release_all() -> void:
	for code: Key in [KEY_D, KEY_A, KEY_SPACE]:
		key(code, false)
	send(["click", 0, false])


## Runs one scenario in a fresh main scene; returns {rows (the pinned ticks), all (with the unpinned tail), late}.
func play(sc: Dictionary) -> Dictionary:
	main = load("res://game/main.tscn").instantiate()
	main.test_mode = true
	root.add_child(main)
	var player: Player = main.player
	var wolf: Wolf = main.get_node("Level/Wolf")
	player.global_position = Vector2(sc.player_x, GROUND_TOP)
	wolf.global_position = Vector2(sc.wolf_x, GROUND_TOP)
	sampler = Sampler.new()
	sampler.player = player
	sampler.wolf = wolf
	sampler.hitbox = wolf.get_node("LungeHitbox")
	root.add_child(sampler)
	var pending: Array = sc.events.duplicate()
	var late: Array = []
	var total: int = sc.length + sc.get("tail", 0)
	while sampler.ticks < total:
		while not pending.is_empty() and pending[0][1] <= sampler.ticks:
			var e: Array = pending.pop_front()
			if e[1] != sampler.ticks:
				late.append({"event": str(e), "sent_before_tick": sampler.ticks})
			send(e)
		await process_frame
	var all := sampler.rows.slice(0, total)
	release_all()
	main.queue_free()
	sampler.queue_free()
	await process_frame
	await process_frame
	return {"rows": all.slice(0, sc.length), "all": all, "late": late}


## Run-length list of one field: [[value, first tick, ticks], ...].
func runs(rows: Array, field: String) -> Array:
	var out: Array = []
	for r: Dictionary in rows:
		if out.is_empty() or out.back()[0] != r[field]:
			out.append([r[field], r.t, 0])
		out.back()[2] += 1
	return out


## Every wolf HP drop: the phase it was in on the tick before, the state on the hit tick, and what came after.
func hits(rows: Array) -> Array:
	var out: Array = []
	for i in range(1, rows.size()):
		if rows[i].w_hp != null and rows[i - 1].w_hp != null and rows[i].w_hp < rows[i - 1].w_hp:
			out.append({"tick": i, "hp": rows[i].w_hp, "phase_when_hit": rows[i - 1].w_state,
				"state_on_hit_tick": rows[i].w_state,
				"phases_after": runs(rows.slice(i), "w_state").map(func(r: Array) -> String: return "%s x%d" % [r[0], r[2]])})
	return out


## The first field that differs on the first differing tick, or {} if none.
func first_difference(pinned: Array, now: Array) -> Dictionary:
	for i in mini(pinned.size(), now.size()):
		for f: String in FIELDS:
			var a: Variant = pinned[i][f]
			var b: Variant = now[i][f]
			if not same(a, b):
				return {"tick": i, "field": f, "pinned": a, "now": b}
	if pinned.size() != now.size():
		return {"tick": mini(pinned.size(), now.size()), "field": "length", "pinned": pinned.size(), "now": now.size()}
	return {}


func same(a: Variant, b: Variant) -> bool:
	if a is Array and b is Array and a.size() == 2 and b.size() == 2:
		return absf(float(a[0]) - float(b[0])) <= EPS and absf(float(a[1]) - float(b[1])) <= EPS
	if a == null or b == null:
		return a == null and b == null
	if (a is float or a is int) and (b is float or b is int):
		return float(a) == float(b)
	return a == b


func save(sc: Dictionary, rows: Array) -> void:
	var lines: PackedStringArray = []
	lines.append("{")
	lines.append('"scenario": %s,' % JSON.stringify(sc.name))
	lines.append('"recorded_at_fps": %d,' % fps)
	lines.append('"player_x": %s, "wolf_x": %s, "length": %d,' % [sc.player_x, sc.wolf_x, sc.length])
	lines.append('"events": %s,' % JSON.stringify(sc.events.map(func(e: Array) -> String: return str(e))))
	lines.append('"fields": %s,' % JSON.stringify(["t"] + FIELDS))
	lines.append('"ticks": [')
	for i in rows.size():
		var r: Dictionary = rows[i]
		var cells := [r.t, r.p_state, r.p_pos, r.p_vel, r.w_state, r.w_pos, r.w_hp, r.w_mon]
		lines.append(JSON.stringify(cells) + ("," if i < rows.size() - 1 else ""))
	lines.append("]")
	lines.append("}")
	var f := FileAccess.open(pin_dir.path_join(sc.name + ".json"), FileAccess.WRITE)
	f.store_string("\n".join(lines) + "\n")
	f.close()


func load_pin(name: String) -> Array:
	var path := pin_dir.path_join(name + ".json")
	if not FileAccess.file_exists(path):
		return []
	var data: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not data is Dictionary:
		return []
	var out: Array = []
	for cells: Array in data.ticks:
		var row := {"t": int(cells[0])}
		for k in FIELDS.size():
			row[FIELDS[k]] = cells[k + 1]
		out.append(row)
	return out


func run() -> void:
	mode = "record" if OS.get_environment("PIN_MODE") == "record" else "check"
	pin_dir = ProjectSettings.globalize_path("res://").path_join("../logs/pin").simplify_path()
	# --fixed-fps is not in OS.get_cmdline_args(): read it from the most common frame delta (tests/test_hurt_tint.gd:191).
	var counts := {}
	for i in 40:
		await process_frame
		var d := root.get_process_delta_time()
		counts[d] = counts.get(d, 0) + 1
	var mode_delta: float = counts.keys().reduce(func(a: float, b: float) -> float: return a if counts[a] >= counts[b] else b)
	fps = roundi(1.0 / mode_delta)
	print(JSON.stringify({"mode": mode, "fps": fps, "physics_ticks_per_second": Engine.physics_ticks_per_second,
		"pin_dir": pin_dir}))
	if mode == "record":
		DirAccess.make_dir_recursive_absolute(pin_dir)

	for sc: Dictionary in scenarios():
		for e: Array in sc.events:
			assert(e[1] % 2 == 0, "scheduled ticks must be even")
		var out: Dictionary = await play(sc)
		var rows: Array = out.rows
		check("%s-inputs-on-schedule" % sc.name, out.late.is_empty() and rows.size() == sc.length,
			{"late": out.late, "ticks": rows.size()})
		var all: Array = out.all
		observe("%s-phases" % sc.name, {"pinned_ticks": rows.size(), "observed_ticks": all.size(),
			"player": runs(all, "p_state").map(func(r: Array) -> String: return "%s@%d x%d" % r),
			"wolf": runs(all, "w_state").map(func(r: Array) -> String: return "%s@%d x%d" % r),
			"wolf_hits": hits(all)})
		if mode == "record":
			save(sc, rows)
			check("%s-recorded" % sc.name, FileAccess.file_exists(pin_dir.path_join(sc.name + ".json")),
				{"file": "logs/pin/%s.json" % sc.name, "ticks": rows.size()})
		else:
			var pinned := load_pin(sc.name)
			var diff := first_difference(pinned, rows) if not pinned.is_empty() else {"field": "missing pin file"}
			check("%s-matches-pin" % sc.name, diff.is_empty(),
				{"ticks": rows.size(), "first_difference": diff} if diff else {"ticks": rows.size()})

	print("WALKER TESTS: %d checks / %d failures" % [results.size(), failures])
	quit(1 if failures else 0)

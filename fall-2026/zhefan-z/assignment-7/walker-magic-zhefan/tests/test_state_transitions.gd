extends SceneTree
## Assignment 7: every transition in CHANGE-BRIEF.md's state-machine table (revision 2026-11-13) occurs from real input
## through the real game loop, and the clip the table names is playing on the tick after.
## game/main.tscn is instanced per scenario; every input is a real event through Input.parse_input_event (D / Space
## keys; mouse motion to the aim point, then a left click), as tests/test_pin_behaviour.gd does. Nothing here calls
## _set_state(), _enter(), take_damage(), win(), fail() or any other transition function; the only writes are the
## player's and the wolf's start positions, before the first tick, as the pin does.
## A Sampler (process_physics_priority 1000, after Player and Wolf) records each tick's state and clip. The clip is read
## through current_animation; when a one-shot clip has already ended (current_animation empty), assigned_animation is
## read instead and the row says so. A transition from A to B is the first tick t whose state is B after a tick in A;
## the check reads tick t + 1 and requires the state still B there.
## Scenarios reuse the pin's positions and inputs where they reach a transition (walk_right_stop, jump, cast,
## take_lunge, hit_growl, kill); three more reach what the pin does not: a running jump (RUN -> RISE, FALL -> RUN),
## a walk into the pit (FAIL, fail_pit) and a walk into the exit (WIN; out of the wolf's sight).
## Every event is on an even tick, so the schedule holds at --fixed-fps 30 (two ticks per frame).
## From fall-2026/zhefan-z/assignment-7/, at 30, 60 and 144 fps:
##   ./scripts/run-test.sh test_state_transitions.gd 60
## Prints one JSON line per check and "WALKER TESTS: N checks / F failures"; exit code 1 on any failure.

const GROUND_TOP := 327.0

## [entity, from states (any of), to state, clips the table names for the target state]
const TABLE := [
	["mage", ["IDLE"], "RUN", ["run"]],
	["mage", ["RUN"], "IDLE", ["idle"]],
	["mage", ["RUN"], "RISE", ["rise"]],
	["mage", ["RISE"], "FALL", ["fall"]],
	["mage", ["FALL"], "IDLE", ["idle"]],
	["mage", ["FALL"], "RUN", ["run"]],
	["mage", ["*"], "CAST", ["cast"]],
	["mage", ["*"], "HURT", ["hurt"]],
	["mage", ["*"], "FAIL", ["fail", "fail_pit"]],
	["mage", ["*"], "WIN", ["win"]],
	["wolf", ["PATROL"], "GROWL", ["lunge"]],
	["wolf", ["GROWL"], "LUNGE", ["lunge"]],
	["wolf", ["LUNGE"], "RECOVER", ["lunge"]],
	["wolf", ["RECOVER"], "PATROL", ["patrol"]],
	["wolf", ["GROWL"], "RECOVER", ["lunge"]],
	["wolf", ["*"], "DEAD", ["dead"]],
]


class Sampler extends Node:
	var ticks := 0
	var rows: Array[Dictionary] = []
	var player: Player
	var wolf: Wolf

	func _init() -> void:
		process_physics_priority = 1000

	func _physics_process(_delta: float) -> void:
		var row := {"t": ticks}
		row.merge(read("mage", player, Player.State.keys()[player.state], player.anim))
		if is_instance_valid(wolf):
			row.merge(read("wolf", wolf, Wolf.State.keys()[wolf.state], wolf.anim))
		else:
			row.merge({"wolf_state": "FREED", "wolf_clip": "", "wolf_clip_ended": false, "wolf_pos": 0.0})
		rows.append(row)
		ticks += 1

	static func read(who: String, _node: Node, state: String, ap: AnimationPlayer) -> Dictionary:
		var current := str(ap.current_animation)
		return {who + "_state": state, who + "_clip": current if current != "" else str(ap.assigned_animation),
			who + "_clip_ended": current == "", who + "_pos": ap.current_animation_position}


var results: Array[Dictionary] = []
var failures := 0
var main: Node
var _mouse_screen := Vector2.ZERO


func _initialize() -> void:
	call_deferred("run")


func check(id: String, passed: bool, observed: Dictionary) -> void:
	results.append({"id": id, "status": "PASS" if passed else "FAIL", "observed": observed})
	if not passed:
		failures += 1
	print(JSON.stringify(results.back()))


func scenarios() -> Array[Dictionary]:
	return [
		# From the pin (tests/test_pin_behaviour.gd scenarios()), same positions and inputs.
		{"name": "walk_right_stop", "player_x": 200.0, "wolf_x": 860.0, "length": 120, "events": [
			["key", 10, KEY_D, true], ["key", 70, KEY_D, false]]},
		{"name": "jump", "player_x": 200.0, "wolf_x": 860.0, "length": 90, "events": [
			["key", 10, KEY_SPACE, true], ["key", 60, KEY_SPACE, false]]},
		{"name": "cast", "player_x": 200.0, "wolf_x": 860.0, "length": 90, "events": [
			["aim", 10, Vector2(300, 340)], ["click", 10, true], ["click", 14, false]]},
		{"name": "take_lunge", "player_x": 780.0, "wolf_x": 860.0, "length": 180, "events": []},
		{"name": "hit_growl", "player_x": 680.0, "wolf_x": 800.0, "length": 150, "events": [
			["aim", 4, Vector2(790, 313)], ["click", 4, true], ["click", 8, false]]},
		# Added here: two hits while the wolf still patrols (horizontal shots at its body height, y 313). The pin's own
		# `kill` no longer kills: its first hit lands in GROWL and cancels the lunge, so its second shot misses
		# (TEST-REPORT, Pins).
		{"name": "kill_in_patrol", "player_x": 680.0, "wolf_x": 860.0, "length": 120, "events": [
			["aim", 10, Vector2(900, 313)], ["click", 10, true], ["click", 14, false],
			["aim", 40, Vector2(900, 313)], ["click", 40, true], ["click", 44, false]]},
		# Added here: the wolf's full cycle from patrol (the edges test's reference positions). With the mage in sight
		# PATROL lasts one tick before the next GROWL (tick 169 in the edges reference), so she jumps before RECOVER
		# ends: while she is more than 40 px above the wolf (SIGHT_Y) it cannot see her, and PATROL holds.
		{"name": "wolf_cycle", "player_x": 680.0, "wolf_x": 860.0, "length": 200, "events": [
			["key", 154, KEY_SPACE, true], ["key", 170, KEY_SPACE, false]]},
		# Added here: jump while running and land while still running, then stop.
		{"name": "running_jump", "player_x": 200.0, "wolf_x": 860.0, "length": 140, "events": [
			["key", 10, KEY_D, true], ["key", 30, KEY_SPACE, true], ["key", 40, KEY_SPACE, false],
			["key", 100, KEY_D, false]]},
		# Added here: walk right into the pit gap (520-580).
		{"name": "into_the_pit", "player_x": 450.0, "wolf_x": 860.0, "length": 120, "events": [
			["key", 10, KEY_D, true]]},
		# Added here: walk right into the exit (1236), more than 120 px from the wolf's patrol (760-960).
		{"name": "to_the_exit", "player_x": 1150.0, "wolf_x": 860.0, "length": 120, "events": [
			["key", 10, KEY_D, true]]},
	]


func key(code: Key, pressed: bool) -> void:
	var ev := InputEventKey.new()
	ev.keycode = code
	ev.physical_keycode = code
	ev.pressed = pressed
	Input.parse_input_event(ev)


func screen_of(world: Vector2) -> Vector2:
	return world - Vector2(main.camera.get_screen_center_position().x - 320.0, 0.0)


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


func play(sc: Dictionary) -> Dictionary:
	main = load("res://game/main.tscn").instantiate()
	main.test_mode = true
	root.add_child(main)
	var player: Player = main.player
	var wolf: Wolf = main.get_node("Level/Wolf")
	player.global_position = Vector2(sc.player_x, GROUND_TOP)
	wolf.global_position = Vector2(sc.wolf_x, GROUND_TOP)
	var sampler := Sampler.new()
	sampler.player = player
	sampler.wolf = wolf
	root.add_child(sampler)
	var pending: Array = sc.events.duplicate()
	var late := []
	while sampler.ticks < sc.length:
		while not pending.is_empty() and pending[0][1] <= sampler.ticks:
			var e: Array = pending.pop_front()
			if e[1] != sampler.ticks:
				late.append({"event": str(e), "sent_before_tick": sampler.ticks})
			send(e)
		await process_frame
	var rows := sampler.rows.slice(0, sc.length)
	release_all()
	main.queue_free()
	sampler.queue_free()
	await process_frame
	await process_frame
	return {"rows": rows, "late": late}


## Run-length list of one field: "VALUE@first_tick xticks".
func runs(rows: Array, field: String) -> Array:
	var out := []
	for r: Dictionary in rows:
		if out.is_empty() or out.back()[0] != r[field]:
			out.append([r[field], r.t, 0])
		out.back()[2] += 1
	return out.map(func(x: Array) -> String: return "%s@%d x%d" % x)


func run() -> void:
	await process_frame
	var played := {}
	var late := {}
	for sc: Dictionary in scenarios():
		var out: Dictionary = await play(sc)
		played[sc.name] = out.rows
		if not out.late.is_empty():
			late[sc.name] = out.late
	check("every-event-on-its-tick", late.is_empty(), {"late": late})

	for row: Array in TABLE:
		var who: String = row[0]
		var froms: Array = row[1]
		var to: String = row[2]
		var clips: Array = row[3]
		var id := "%s-%s-to-%s" % [who, "any" if froms == ["*"] else "-or-".join(froms), to]
		# Every occurrence in every scenario; the first whose new state still holds on the tick after is the one checked
		# (a state can last a single tick, e.g. RUN after a knockback landing); the others are counted.
		var occurrences := []
		for sc_name: String in played:
			var rows: Array = played[sc_name]
			for t in range(1, rows.size() - 1):
				var prev: String = rows[t - 1][who + "_state"]
				var cur: String = rows[t][who + "_state"]
				if cur == to and prev != to and (froms == ["*"] or prev in froms):
					var nxt: Dictionary = rows[t + 1]
					occurrences.append({"scenario": sc_name, "tick": t, "from": prev,
						"state_on_tick_after": nxt[who + "_state"], "clip_on_tick_after": nxt[who + "_clip"],
						"clip_had_ended": nxt[who + "_clip_ended"],
						"clip_frame_on_tick_after": roundi(nxt[who + "_pos"] * 60.0), "expected_clips": clips,
						"states": runs(rows.slice(maxi(t - 3, 0), mini(t + 4, rows.size())), who + "_state")})
		var held := occurrences.filter(func(o: Dictionary) -> bool: return o.state_on_tick_after == to)
		var found: Dictionary = held[0] if not held.is_empty() else (occurrences[0] if not occurrences.is_empty() else {})
		if not found.is_empty():
			found["occurrences"] = occurrences.size()
			found["occurrences_holding_a_tick"] = held.size()
		if found.is_empty():
			var seen := {}
			for sc_name: String in played:
				seen[sc_name] = runs(played[sc_name], who + "_state")
			check(id, false, {"not_reached_with_real_input": true, "expected_clips": clips, "states_seen": seen})
			continue
		check(id, found.state_on_tick_after == to and found.clip_on_tick_after in clips, found)

	print("WALKER TESTS: %d checks / %d failures" % [results.size(), failures])
	quit(1 if failures else 0)

extends SceneTree
## Assignment 7 edges test (CHANGE-BRIEF Tests: Edges): the growl interrupt and the clips at the phase boundaries,
## through the real game loop with real input (Input.parse_input_event: mouse clicks to cast, D / Space, Esc).
## Nothing here calls a wolf or player function or writes their state; the only writes are the start positions.
## Setup: player at 680, wolf at 860 patrolling left; it first sees her at dx <= 120 and growls (tick g0), lunges
## (l0) and recovers (r0), as measured in a reference run with no input.
## A fireball hit is resolved at the start of a physics tick, before the wolf's own update, so a hit "on the k-th tick
## of a phase" is one that lands while the wolf has been in that phase for k ticks: for the hit tick h, the state
## recorded at the end of tick h - 1 is that phase. Casts are timed by search: each target hit tick is reached by
## trying cast ticks (even ticks only, so the same schedule is valid at 30 fps) and small aim offsets, every try a full
## run of the game; the fireball must arrive exactly on the target tick.
## Cases: hits on the first and last GROWL tick (cancel: RECOVER on the hit tick, the clip in the recovery section,
## the hitbox never armed); on the first and last LUNGE tick (no cancel); on the first RECOVER tick (only HP changes);
## at every phase boundary of the lunge clip (GROWL start at 0, GROWL -> LUNGE at 31, LUNGE -> RECOVER at 53,
## RECOVER -> PATROL at 89), a hit one tick before, on and one tick after it, each with the brief's rule for its phase;
## a killing hit in GROWL, LUNGE and RECOVER (DEAD, the dead clip, hitbox off from the next tick); a real Esc mid-lunge
## (the wolf's position, state and clip position freeze on the same tick and resume aligned); RUN -> jump -> land -> RUN
## restarts the run cycle at frame 0; the clip frame equals the wolf's phase tick on every tick of the lunge clip,
## for a growl that starts with the AnimationPlayer idle and one that starts while the patrol clip is still playing.
## From fall-2026/zhefan-z/assignment-7/, at 30, 60 and 144 fps:
##   ./scripts/run-test.sh test_anim_edges.gd 60 300
## Prints one JSON line per check and "WALKER TESTS: N checks / F failures"; exit code 1 on any failure.

const GROUND_TOP := 327.0
const PLAYER_X := 680.0
const WOLF_X := 860.0
const RECOVER_FRAME := 53
## Aim offsets tried, in order: (dx, dy) from the wolf's body centre at the moment of the click.
const AIM := [[0.0, 0.0], [0.0, -6.0], [0.0, 6.0], [0.0, -12.0], [0.0, 12.0], [0.0, -3.0], [0.0, 3.0], [0.0, -9.0],
	[0.0, 9.0], [-10.0, 0.0], [10.0, 0.0], [-20.0, 0.0], [20.0, 0.0], [-10.0, -8.0], [10.0, 8.0], [-30.0, 0.0],
	[30.0, 0.0], [0.0, -15.0], [0.0, 15.0], [-20.0, 10.0], [20.0, -10.0]]


class Sampler extends Node:
	var ticks := 0
	var rows: Array[Dictionary] = []
	var player: Player
	var wolf: Wolf

	func _init() -> void:
		process_physics_priority = 1000

	func _physics_process(_delta: float) -> void:
		var row := {"t": ticks, "p_state": Player.State.keys()[player.state], "p_clip": str(player.anim.assigned_animation),
			"p_pos": player.anim.current_animation_position, "p_frame": player.sprite.frame}
		if is_instance_valid(wolf):
			row.merge({"w_state": Wolf.State.keys()[wolf.state], "w_hp": wolf.hp, "w_x": wolf.global_position.x,
				"w_mon": wolf.lunge_hitbox.monitoring, "w_clip": str(wolf.anim.assigned_animation),
				"w_pos": wolf.anim.current_animation_position})
		else:
			row.merge({"w_state": "FREED", "w_hp": 0, "w_x": 0.0, "w_mon": false, "w_clip": "", "w_pos": 0.0})
		rows.append(row)
		ticks += 1


## Runs while the tree is paused too: one row per process frame.
class FrameProbe extends Node:
	var rows: Array[Dictionary] = []
	var wolf: Wolf
	var sampler: Sampler

	func _init() -> void:
		process_mode = Node.PROCESS_MODE_ALWAYS

	func _process(_delta: float) -> void:
		if get_tree().paused and is_instance_valid(wolf):
			rows.append({"tick": sampler.ticks, "w_x": wolf.global_position.x, "w_state": Wolf.State.keys()[wolf.state],
				"w_pos": wolf.anim.current_animation_position})


var results: Array[Dictionary] = []
var failures := 0
var runs_made := 0
var found_cache := {}


func _initialize() -> void:
	call_deferred("run")


func check(id: String, passed: bool, observed: Dictionary) -> void:
	results.append({"id": id, "status": "PASS" if passed else "FAIL", "observed": observed})
	if not passed:
		failures += 1
	print(JSON.stringify(results.back()))


func key(code: Key, pressed: bool) -> void:
	var ev := InputEventKey.new()
	ev.keycode = code
	ev.physical_keycode = code
	ev.pressed = pressed
	Input.parse_input_event(ev)


func mouse(main: Node, world: Vector2, pressed: Variant) -> void:
	var screen := world - Vector2(main.camera.get_screen_center_position().x - 320.0, 0.0)
	var motion := InputEventMouseMotion.new()
	motion.position = screen
	motion.global_position = screen
	Input.parse_input_event(motion)
	if pressed != null:
		var ev := InputEventMouseButton.new()
		ev.button_index = MOUSE_BUTTON_LEFT
		ev.pressed = pressed
		ev.position = screen
		ev.global_position = screen
		Input.parse_input_event(ev)


## One run of the game. events: ["cast", tick, [dx, dy]] (aim at the wolf's body centre + (dx, dy) at that moment,
## click held 4 ticks), ["key", tick, keycode, pressed], ["esc_pause", tick, frames_paused]. Every tick must be even.
func play(events: Array, length: int, player_x := PLAYER_X) -> Dictionary:
	runs_made += 1
	var main: Node = load("res://game/main.tscn").instantiate()
	main.test_mode = true
	root.add_child(main)
	var player: Player = main.player
	var wolf: Wolf = main.get_node("Level/Wolf")
	player.global_position = Vector2(player_x, GROUND_TOP)
	wolf.global_position = Vector2(WOLF_X, GROUND_TOP)
	var sampler := Sampler.new()
	sampler.player = player
	sampler.wolf = wolf
	root.add_child(sampler)
	var probe := FrameProbe.new()
	probe.wolf = wolf
	probe.sampler = sampler
	root.add_child(probe)
	var pending: Array = events.duplicate()
	pending.sort_custom(func(a: Array, b: Array) -> bool: return a[1] < b[1])
	var releases: Array = []
	var late := false
	while sampler.ticks < length:
		while not releases.is_empty() and releases[0] <= sampler.ticks:
			releases.pop_front()
			mouse(main, Vector2(-100, -100), false)
		while not pending.is_empty() and pending[0][1] <= sampler.ticks:
			var e: Array = pending.pop_front()
			late = late or e[1] != sampler.ticks
			match e[0]:
				"cast":
					if is_instance_valid(wolf):
						mouse(main, wolf.global_position + Vector2(8 * wolf.facing + e[2][0], -14 + e[2][1]), true)
						releases.append(e[1] + 4)
				"key":
					key(e[2], e[3])
				"esc_pause":
					key(KEY_ESCAPE, true)
					key(KEY_ESCAPE, false)
					while not paused:
						await process_frame
					for i in e[2]:
						await process_frame
					key(KEY_ESCAPE, true)
					key(KEY_ESCAPE, false)
					while paused:
						await process_frame
		await process_frame
	for code: Key in [KEY_D, KEY_SPACE]:
		key(code, false)
	mouse(main, Vector2(-100, -100), false)
	var out := {"rows": sampler.rows.slice(0, length), "paused_frames": probe.rows, "late": late}
	main.queue_free()
	sampler.queue_free()
	probe.queue_free()
	await process_frame
	await process_frame
	return out


func first_row(rows: Array, state: String, from := 0) -> int:
	for t in range(from, rows.size()):
		if rows[t].w_state == state:
			return t
	return -1


## Hit ticks: every tick where the wolf's HP dropped.
func hit_ticks(rows: Array) -> Array:
	var out := []
	for t in range(1, rows.size()):
		if rows[t].w_hp < rows[t - 1].w_hp:
			out.append(t)
	return out


## Finds a cast (even tick, aim offset) whose fireball hits on `target`, after the `prefix` events. Returns
## {"events", "rows"} of the run that hit, or {} if none did.
func cast_for(target: int, prefix: Array, length: int) -> Dictionary:
	# A search already made for the same target (the boundary cases repeat some of the cases above) is reused.
	var memo_key := str([target, prefix, length])
	if found_cache.has(memo_key):
		return found_cache[memo_key]
	var result: Dictionary = await _cast_search(target, prefix, length)
	found_cache[memo_key] = result
	return result


func _cast_search(target: int, prefix: Array, length: int) -> Dictionary:
	var tried := {}
	for aim: Array in AIM:
		var c := (target - 20) & ~1
		for step in 8:
			if c < 2 or tried.has([c, aim]):
				break
			tried[[c, aim]] = true
			var events := prefix + [["cast", c, aim]]
			var out: Dictionary = await play(events, mini(length, target + 4))
			var hits := hit_ticks(out.rows).filter(func(t: int) -> bool: return t > (prefix.map(func(e: Array) -> int: return e[1]).max() if not prefix.is_empty() else 0) + 2)
			var hits_after_prefix := hits.filter(func(t: int) -> bool: return t > c)
			if hits_after_prefix.is_empty():
				break
			var h: int = hits_after_prefix[0]
			if h == target:
				var full: Dictionary = await play(events, length)
				return {"events": events, "rows": full.rows, "cast_tick": c, "aim": aim}
			var nc := (c + (target - h)) & ~1
			if nc == c:
				break
			c = nc
	return {}


func frame_of(pos: float) -> int:
	return roundi(pos * 60.0)


func states(rows: Array) -> Array:
	return rows.map(func(r: Dictionary) -> String: return r.w_state)


func runs(rows: Array) -> Array:
	var out := []
	for r: Dictionary in rows:
		if out.is_empty() or out.back()[0] != r.w_state:
			out.append([r.w_state, r.t, 0])
		out.back()[2] += 1
	return out.map(func(x: Array) -> String: return "%s@%d x%d" % x)


func run() -> void:
	await process_frame
	var length := 200
	var ref: Dictionary = await play([], length)
	var rows: Array = ref.rows
	var g0 := first_row(rows, "GROWL")
	var l0 := first_row(rows, "LUNGE", g0)
	var r0 := first_row(rows, "RECOVER", l0)
	var p0 := first_row(rows, "PATROL", r0)
	check("reference-phases", g0 > 0 and l0 - g0 == 31 and r0 - l0 == 22 and p0 - r0 == 36 and not ref.late,
		{"growl_tick": g0, "lunge_tick": l0, "recover_tick": r0, "patrol_tick": p0, "wolf": runs(rows.slice(0, p0 + 2))})

	# The clip frame equals the wolf's phase tick (ticks since GROWL entry) on every GROWL, LUNGE and RECOVER tick, for
	# the first growl (the AnimationPlayer idle before it) and the second (it follows one PATROL tick, while the patrol
	# clip is still playing).
	var g1 := first_row(rows, "GROWL", p0)
	var off := []
	var checked := 0
	for span: Array in [[g0, p0], [g1, length]]:
		for t in range(span[0], span[1]):
			if rows[t].w_state == "PATROL":
				break
			checked += 1
			if rows[t].w_clip != "lunge" or frame_of(rows[t].w_pos) != t - span[0]:
				off.append({"t": t, "phase_tick": t - span[0], "clip": rows[t].w_clip, "frame": frame_of(rows[t].w_pos)})
	check("clip-frame-equals-phase-tick-on-every-lunge-clip-tick", off.is_empty() and g1 == p0 + 1,
		{"ticks_checked": checked, "second_growl_tick": g1, "mismatches": off.slice(0, 5),
		"frame_at_growl_entry": frame_of(rows[g0].w_pos), "frame_at_lunge_entry": frame_of(rows[l0].w_pos),
		"frame_at_recover_entry": frame_of(rows[r0].w_pos), "frame_at_second_growl_entry": frame_of(rows[g1].w_pos)})

	# Non-lethal hits at the boundaries. Target hit tick h: the state at the end of h - 1 is the phase.
	var cases := [
		["growl-first", g0 + 1, "GROWL", true], ["growl-last", l0, "GROWL", true],
		["lunge-first", l0 + 1, "LUNGE", false], ["lunge-last", r0, "LUNGE", false],
		["recover-first", r0 + 1, "RECOVER", false]]
	for c: Array in cases:
		var found: Dictionary = await cast_for(c[1], [], length)
		if found.is_empty():
			check("%s-hit-arrives-on-target" % c[0], false, {"target_tick": c[1]})
			continue
		var hr: Array = found.rows
		var h: int = c[1]
		var phase_tick := 0
		while h - 2 - phase_tick >= 0 and hr[h - 2 - phase_tick].w_state == c[2]:
			phase_tick += 1
		var base := {"hit_tick": h, "cast_tick": found.cast_tick, "aim": found.aim, "phase_when_hit": hr[h - 1].w_state,
			"phase_tick_when_hit": phase_tick, "state_on_hit_tick": hr[h].w_state, "hp": hr[h].w_hp}
		var hit_ok: bool = hr[h - 1].w_state == c[2] and hr[h].w_hp == 1 and hit_ticks(hr) == [h]
		if c[3]:
			# Cancel: RECOVER on the hit tick, the clip in the recovery section, the hitbox never armed, no lunge.
			var next_patrol := first_row(hr, "PATROL", h)
			var armed := hr.slice(g0, next_patrol).filter(func(r: Dictionary) -> bool: return r.w_mon).size()
			var lunged := hr.slice(h, next_patrol).filter(func(r: Dictionary) -> bool: return r.w_state == "LUNGE").size()
			base.merge({"clip_frame_on_hit_tick": frame_of(hr[h].w_pos), "clip": hr[h].w_clip,
				"recover_ticks": next_patrol - h, "armed_ticks": armed, "lunge_ticks_after_hit": lunged,
				"wolf": runs(hr.slice(g0, next_patrol + 1))})
			check("%s-hit-cancels-the-lunge" % c[0], hit_ok and hr[h].w_state == "RECOVER" and hr[h].w_clip == "lunge"
				and frame_of(hr[h].w_pos) == RECOVER_FRAME and armed == 0 and lunged == 0, base)
		else:
			var same_states := states(hr) == states(rows)
			var same_x := range(length).all(func(t: int) -> bool: return absf(hr[t].w_x - rows[t].w_x) < 0.01)
			var same_clip := range(length).all(func(t: int) -> bool:
				return hr[t].w_clip == rows[t].w_clip and absf(hr[t].w_pos - rows[t].w_pos) < 1e-4)
			base.merge({"states_as_reference": same_states, "positions_as_reference": same_x, "clip_as_reference": same_clip})
			var id := "%s-hit-only-hp" % c[0] if c[2] == "RECOVER" else "%s-hit-no-cancel" % c[0]
			check(id, hit_ok and same_states and same_x and same_clip, base)

	# Every phase boundary of the lunge clip, a hit one tick before, on and one tick after it (CHANGE-BRIEF per-phase
	# interrupts). Boundary b is the first tick of the new phase, g0 + b. A hit on tick h is resolved before the wolf's
	# update that tick, so the interrupt follows the phase the wolf ended tick h - 1 in: "on" the boundary is still the
	# phase before it. Expected phase and rule per case are written out here from the brief, not read from the run.
	var boundaries := [["growl-start", 0, g0, ["PATROL", "PATROL", "GROWL"]],
		["growl-to-lunge", 31, l0, ["GROWL", "GROWL", "LUNGE"]],
		["lunge-to-recover", 53, r0, ["LUNGE", "LUNGE", "RECOVER"]],
		["recover-to-patrol", 89, p0, ["RECOVER", "RECOVER", "PATROL"]]]
	var rule_of := {"GROWL": "cancel", "LUNGE": "no-cancel", "RECOVER": "hp-only", "PATROL": "hp-only"}
	for bd: Array in boundaries:
		for side: int in [-1, 0, 1]:
			var where: String = ["before", "on", "after"][side + 1]
			var h: int = bd[2] + side
			var want_phase: String = bd[3][side + 1]
			var rule: String = rule_of[want_phase]
			var id := "boundary-%s-%s-%s" % [bd[0], where, rule]
			var found: Dictionary = await cast_for(h, [], length)
			if found.is_empty():
				check(id, false, {"target_tick": h, "boundary_frame": bd[1]})
				continue
			var hr: Array = found.rows
			var base := {"boundary_frame": bd[1], "boundary_tick": bd[2], "hit_tick": h, "hit_clip_frame": h - g0,
				"cast_tick": found.cast_tick, "aim": found.aim, "phase_when_hit": hr[h - 1].w_state,
				"expected_phase": want_phase, "state_on_hit_tick": hr[h].w_state, "hp": hr[h].w_hp}
			var hit_ok: bool = bd[2] - g0 == bd[1] and hr[h - 1].w_state == want_phase and hr[h].w_hp == 1 \
				and hit_ticks(hr) == [h]
			if rule == "cancel":
				var next_patrol := first_row(hr, "PATROL", h)
				var armed := hr.slice(g0, next_patrol).filter(func(r: Dictionary) -> bool: return r.w_mon).size()
				var lunged := hr.slice(h, next_patrol).filter(func(r: Dictionary) -> bool: return r.w_state == "LUNGE").size()
				base.merge({"clip_frame_on_hit_tick": frame_of(hr[h].w_pos), "clip": hr[h].w_clip,
					"armed_ticks": armed, "lunge_ticks_after_hit": lunged, "wolf": runs(hr.slice(g0, next_patrol + 1))})
				check(id, hit_ok and hr[h].w_state == "RECOVER" and hr[h].w_clip == "lunge"
					and frame_of(hr[h].w_pos) == RECOVER_FRAME and armed == 0 and lunged == 0, base)
			else:
				var same_states := states(hr) == states(rows)
				var same_x := range(length).all(func(t: int) -> bool: return absf(hr[t].w_x - rows[t].w_x) < 0.01)
				var same_clip := range(length).all(func(t: int) -> bool:
					return hr[t].w_clip == rows[t].w_clip and absf(hr[t].w_pos - rows[t].w_pos) < 1e-4)
				var same_mon := range(length).all(func(t: int) -> bool: return hr[t].w_mon == rows[t].w_mon)
				base.merge({"states_as_reference": same_states, "positions_as_reference": same_x,
					"clip_as_reference": same_clip, "hitbox_as_reference": same_mon})
				check(id, hit_ok and same_states and same_x and same_clip and same_mon, base)

	# Killing hits: a first hit in PATROL (cast at tick 10) leaves 1 HP, then the second lands in the phase.
	var prefix := [["cast", 10, [0.0, 0.0]]]
	var pre: Dictionary = await play(prefix, g0)
	var pre_hits := hit_ticks(pre.rows)
	var patrol_hit_ok: bool = pre_hits.size() == 1 and pre.rows[pre_hits[0] - 1].w_state == "PATROL" \
		and pre.rows.back().w_hp == 1 and states(pre.rows) == states(rows.slice(0, g0))
	check("first-hit-in-patrol-leaves-1-hp", patrol_hit_ok, {"hit_ticks": pre_hits,
		"state_when_hit": pre.rows[pre_hits[0] - 1].w_state if not pre_hits.is_empty() else null})
	for kc: Array in [["growl", g0 + 10, "GROWL"], ["lunge", l0 + 8, "LUNGE"], ["recover", r0 + 10, "RECOVER"]]:
		var found: Dictionary = await cast_for(kc[1], prefix, length)
		if found.is_empty():
			check("kill-in-%s-hit-arrives-on-target" % kc[0], false, {"target_tick": kc[1]})
			continue
		var hr: Array = found.rows
		var h: int = kc[1]
		var mon_after := hr.slice(h + 1, mini(h + 30, length)).filter(func(r: Dictionary) -> bool: return r.w_mon).size()
		check("kill-in-%s-dead-clip-hitbox-off" % kc[0], hr[h - 1].w_state == kc[2] and hr[h].w_state == "DEAD"
			and hr[h].w_hp == 0 and hr[h].w_clip == "dead" and mon_after == 0,
			{"hit_tick": h, "cast_tick": found.cast_tick, "phase_when_hit": hr[h - 1].w_state, "state_on_hit_tick": hr[h].w_state,
			"clip": hr[h].w_clip, "monitoring_on_hit_tick": hr[h].w_mon, "monitoring_ticks_after": mon_after})

	# Real Esc mid-lunge: everything freezes on the same tick and resumes aligned.
	var esc_tick := (l0 + 8) & ~1
	var paused_run: Dictionary = await play([["esc_pause", esc_tick, 12]], length)
	var pr: Array = paused_run.rows
	var frozen: Array = paused_run.paused_frames
	var still := frozen.size() >= 12 and frozen.all(func(f: Dictionary) -> bool:
		return f.w_x == frozen[0].w_x and f.w_state == frozen[0].w_state and f.w_pos == frozen[0].w_pos and f.tick == frozen[0].tick)
	var aligned := states(pr) == states(rows) and range(length).all(func(t: int) -> bool:
		return absf(pr[t].w_x - rows[t].w_x) < 0.01 and absf(pr[t].w_pos - rows[t].w_pos) < 1e-4)
	var last_before: int = frozen[0].tick - 1 if not frozen.is_empty() else -1
	check("esc-mid-lunge-freezes-and-resumes-aligned", still and aligned and last_before >= l0 and last_before < r0,
		{"esc_sent_before_tick": esc_tick, "paused_frames": frozen.size(), "frozen_after_tick": last_before,
		"frozen": frozen[0] if not frozen.is_empty() else null,
		"row_before_pause": {"x": snappedf(pr[last_before].w_x, 0.01), "clip_frame": frame_of(pr[last_before].w_pos)} if last_before >= 0 else null,
		"same_states_positions_and_clip_as_unpaused_run_tick_by_tick": aligned})

	# RUN -> jump -> land -> RUN restarts the run cycle at frame 0.
	var jr: Dictionary = await play([["key", 10, KEY_D, true], ["key", 32, KEY_SPACE, true], ["key", 42, KEY_SPACE, false],
		["key", 120, KEY_D, false]], 120, 200.0)
	var jrows: Array = jr.rows
	var p_runs := []
	for r: Dictionary in jrows:
		if p_runs.is_empty() or p_runs.back()[0] != r.p_state:
			p_runs.append([r.p_state, r.t, 0])
		p_runs.back()[2] += 1
	var reentry := -1
	var seen_air := false
	for r: Dictionary in jrows:
		if r.p_state in ["RISE", "FALL"]:
			seen_air = true
		elif seen_air and r.p_state == "RUN":
			reentry = r.t
			break
	var before_jump := -1
	for t in jrows.size():
		if jrows[t].p_state == "RISE":
			before_jump = t - 1
			break
	check("run-jump-land-run-restarts-at-frame-0", reentry > 0 and jrows[reentry].p_clip == "run"
		and jrows[reentry].p_pos == 0.0 and jrows[reentry].p_frame == 0 and jrows[before_jump].p_pos > 0.0
		and jrows[reentry + 1].p_pos > 0.0,
		{"player": p_runs.map(func(x: Array) -> String: return "%s@%d x%d" % x), "run_clip_pos_before_jump": jrows[before_jump].p_pos,
		"reentry_tick": reentry, "clip_pos_on_reentry": jrows[reentry].p_pos if reentry > 0 else null,
		"frame_on_reentry": jrows[reentry].p_frame if reentry > 0 else null})

	print(JSON.stringify({"id": "runs", "observation": {"game_runs": runs_made}}))
	print("WALKER TESTS: %d checks / %d failures" % [results.size(), failures])
	quit(1 if failures else 0)

extends SceneTree
## Assignment 5 headless check for the hurt tint (CHANGE-BRIEF.md section 2): the shader interface, the
## sprite's material, and rules R1-R9 plus the headless part of R10, failures F1 and F4.
## From fall-2026/zhefan-z/assignment-5/, at 30, 60 and 144 fps:
##   ./scripts/run-test.sh test_hurt_tint.gd 30
## Prints one JSON line per check and "WALKER TESTS: N checks / F failures"; exit code 1 on any failure.
## Headless uses a dummy renderer: every check reads the value the driver sends to the shader, never a pixel.
## The state is driven through the real game loop: wolf lunges land the hits, and key events go through
## Input.parse_input_event (D / A to walk, Esc to pause). Nothing here calls take_damage or the driver.

const SHADER_PATH := "res://shaders/hurt_tint.gdshader"
const WOLF_SCENE := preload("res://features/wolf/wolf.tscn")
const GROUND_TOP := 327.0
const PHYSICS_STEP := 1.0 / 60.0   # physics rate is not set in project.godot (CHANGE-BRIEF.md:26)
const EPS := 1e-5


## One row per frame, taken after every other _process() (the highest priority runs last), also while paused.
class Sampler extends Node:
	var probe: Callable
	var rows: Array[Dictionary] = []
	var game_time := 0.0   # sum of frame deltas while the tree is not paused

	func _init() -> void:
		process_priority = 1000
		process_mode = Node.PROCESS_MODE_ALWAYS

	func _process(delta: float) -> void:
		var paused := get_tree().paused
		if not paused:
			game_time += delta
		var row: Dictionary = probe.call()
		row.merge({"t": game_time, "d": delta, "paused": paused})
		rows.append(row)


## Counts physics ticks that run while the tree is not paused (pausable, like the player). R7 measures the
## paused window with it (CHANGE-BRIEF revision 2026-10-23 "R7: measure the paused window in physics ticks").
class TickCounter extends Node:
	var count := 0

	func _init() -> void:
		process_mode = Node.PROCESS_MODE_PAUSABLE

	func _physics_process(_delta: float) -> void:
		count += 1


var fps := 60.0
var tol := 1.0 / 60.0   # R4: one frame period, widened to one physics step above 60 fps
var main: Node
var player: Player
var wolf: Wolf
var wolf2: Wolf
var sampler: Sampler
var ticks: TickCounter
var hurts := 0
var fails := 0
var fail_reason := ""
var clears := 0
var results: Array[Dictionary] = []
var failures := 0


func _initialize() -> void:
	call_deferred("run")


func check(id: String, passed: bool, observed: Dictionary) -> void:
	results.append({"id": id, "status": "PASS" if passed else "FAIL", "observed": observed})
	if not passed:
		failures += 1
	print(JSON.stringify(results.back()))


## Waits frame by frame until `cond` holds or `max_frames` pass; returns whether it held.
func until(cond: Callable, max_frames: int) -> bool:
	for i in max_frames:
		if cond.call():
			return true
		await process_frame
	return cond.call()


func key(code: Key, pressed: bool) -> void:
	var ev := InputEventKey.new()
	ev.keycode = code
	ev.physical_keycode = code
	ev.pressed = pressed
	Input.parse_input_event(ev)


func tap(code: Key) -> void:
	key(code, true)
	key(code, false)


## A new main scene with the player and the wolf placed, and a new sampler. Returns before the new
## scene's first _process(), so a caller can read the material as instantiated.
func fresh(player_x: float, wolf_x := 860.0) -> void:
	key(KEY_D, false)
	key(KEY_A, false)
	Engine.time_scale = 1.0
	paused = false
	if is_instance_valid(main):
		main.queue_free()
	if is_instance_valid(sampler):
		sampler.queue_free()
	if is_instance_valid(ticks):
		ticks.queue_free()
	await process_frame
	main = load("res://game/main.tscn").instantiate()
	main.test_mode = true
	root.add_child(main)
	player = main.player
	wolf = main.get_node("Level/Wolf")
	wolf2 = null
	player.global_position = Vector2(player_x, GROUND_TOP)
	wolf.global_position = Vector2(wolf_x, GROUND_TOP)
	hurts = 0
	fails = 0
	fail_reason = ""
	clears = 0
	player.hurt.connect(func(_hp: int) -> void: hurts += 1)
	player.failed.connect(func(r: String) -> void:
		fails += 1
		fail_reason = r)
	player.cleared.connect(func() -> void: clears += 1)
	ticks = TickCounter.new()
	root.add_child(ticks)
	sampler = Sampler.new()
	sampler.probe = sample
	root.add_child(sampler)


func sample() -> Dictionary:
	if not is_instance_valid(player):
		return {"i": -1.0, "inv": -1.0, "vis": false, "failing": false, "cleared": false, "hurts": hurts, "contact2": false}
	var v: Variant = (player.sprite.material as ShaderMaterial).get_shader_parameter("intensity")
	return {"i": -1.0 if v == null else float(v), "inv": player.invulnerable, "vis": player.sprite.visible,
		"failing": player.is_failing, "cleared": player.is_cleared, "hurts": hurts,
		"contact2": wolf2 != null and is_instance_valid(wolf2) and wolf2._hit_this_lunge,
		"ticks": ticks.count if is_instance_valid(ticks) else -1}


func first(from: int, pred: Callable) -> int:
	for k in range(maxi(from, 0), sampler.rows.size()):
		if pred.call(sampler.rows[k]):
			return k
	return -1


func since(k: int) -> float:
	return sampler.game_time - sampler.rows[k].t


func frames_for(seconds: float) -> int:
	return int(ceil(seconds * fps / Engine.time_scale)) + 2


## Holds a walking key until a wolf's lunge lands, then releases it. The hit row is recorded once this returns.
func walk_until_hit(walk_key: Key) -> bool:
	key(walk_key, true)
	var ok: bool = await until(func() -> bool: return hurts > 0, frames_for(6.0))
	key(walk_key, false)
	await process_frame
	return ok


## Indices into sampler.rows: h = first row after a hit landed, p = first row with intensity > 0,
## z = first row after p with intensity == 0, zi = first row after p with invulnerable == 0.
func window() -> Dictionary:
	var h := first(0, func(r: Dictionary) -> bool: return r.hurts >= 1)
	var p := first(0, func(r: Dictionary) -> bool: return r.i > 0.0)
	var z := first(p, func(r: Dictionary) -> bool: return r.i == 0.0) if p >= 0 else -1
	var zi := first(p, func(r: Dictionary) -> bool: return r.inv == 0.0) if p >= 0 else -1
	return {"h": h, "p": p, "z": z, "zi": zi}


func non_increasing(from: int, to: int) -> bool:
	for k in range(from + 1, to + 1):
		if sampler.rows[k].i > sampler.rows[k - 1].i + EPS:
			return false
	return true


func run() -> void:
	Controls.ensure()
	await process_frame   # get_shader_uniform_list() needs the main loop running

	# The frame rate: --fixed-fps is not in OS.get_cmdline_args(), so it is read from the most common frame
	# delta over 40 frames (a few frames near startup differ slightly, from the engine's frame-timing smoothing).
	sampler = Sampler.new()
	sampler.probe = func() -> Dictionary: return {}
	root.add_child(sampler)
	await until(func() -> bool: return sampler.rows.size() >= 40, 45)
	var counts := {}
	for r: Dictionary in sampler.rows:
		var dk := snappedf(r.d, 0.0000001)
		counts[dk] = counts.get(dk, 0) + 1
	var mode_delta := 0.0
	for dk: float in counts:
		if mode_delta == 0.0 or counts[dk] > counts[mode_delta]:
			mode_delta = dk
	fps = roundf(1.0 / mode_delta)
	tol = PHYSICS_STEP if fps > 60.0 else 1.0 / fps
	check("fixed-fps-from-frame-delta", absf(mode_delta - 1.0 / fps) < 1e-6 and counts[mode_delta] >= 30,
		{"fps": fps, "most_common_delta": mode_delta, "frames_with_it": counts[mode_delta], "of_frames": sampler.rows.size()})

	# Uniform names and types, as the engine parses the shader.
	var shader := load(SHADER_PATH) as Shader
	var uniforms := {}
	for u: Dictionary in shader.get_shader_uniform_list():
		uniforms[u.name] = {"type": type_string(u.type), "hint": u.hint, "hint_string": u.hint_string}
	var range_ok := false
	if uniforms.has("intensity"):
		var parts: PackedStringArray = String(uniforms.intensity.hint_string).split(",")
		range_ok = uniforms.intensity.hint == PROPERTY_HINT_RANGE and parts.size() >= 2 \
			and is_equal_approx(parts[0].to_float(), 0.0) and is_equal_approx(parts[1].to_float(), 1.0)
	check("shader-uniform-names-and-types", uniforms.size() == 2 and uniforms.has("tint_color")
		and uniforms.tint_color.type == type_string(TYPE_COLOR) and uniforms.has("intensity")
		and uniforms.intensity.type == type_string(TYPE_FLOAT) and range_ok, {"uniforms": uniforms})

	# Defaults, read from the source text (a headless engine does not report them). F1: intensity starts at 0.0.
	var src := FileAccess.get_file_as_string(SHADER_PATH)
	var decls := {}
	var decl_re := RegEx.create_from_string("uniform\\s+(\\w+)\\s+(\\w+)\\s*:\\s*([^=;]+?)\\s*=\\s*([^;]+);")
	var num_re := RegEx.create_from_string("(?<![\\w.])-?\\d+(\\.\\d*)?")   # not the 4 in "vec4("
	for m in decl_re.search_all(src):
		var nums: Array[float] = []
		for n in num_re.search_all(m.get_string(4)):
			nums.append(n.get_string().to_float())
		decls[m.get_string(2)] = {"type": m.get_string(1), "hints": m.get_string(3).strip_edges(), "default": nums}
	var tint_ok: bool = decls.has("tint_color") and decls.tint_color.type == "vec4" \
		and "source_color" in decls.tint_color.hints and decls.tint_color.default == [1.0, 0.0, 0.0, 1.0]
	var intensity_ok: bool = decls.has("intensity") and decls.intensity.type == "float" \
		and decls.intensity.default == [0.0]
	check("shader-source-defaults", tint_ok and intensity_ok, {"declarations": decls})

	# The sprite's material: the hand-written shader, unique per scene instance.
	await fresh(700)
	var mat := player.sprite.material as ShaderMaterial
	check("sprite-has-local-shader-material", mat != null and mat.shader != null
		and mat.shader.resource_path == SHADER_PATH and mat.resource_local_to_scene,
		{"material": str(mat), "shader": mat.shader.resource_path if mat and mat.shader else "",
		"local_to_scene": mat.resource_local_to_scene if mat else false})

	# One hit: walk right (D) into the wolf's lunge. After the hit the wolf is stopped so it cannot hit again.
	var hit := await walk_until_hit(KEY_D)
	wolf.set_physics_process(false)
	var w := window()
	await until(func() -> bool: return since(w.h) >= 1.5, frames_for(2.0))
	w = window()
	var rows := sampler.rows
	var before := rows.slice(0, maxi(w.h, 0)).map(func(r: Dictionary) -> float: return r.i)
	check("F1-zero-before-any-hit", hit and w.h > 0 and before.all(func(i: float) -> bool: return i == 0.0),
		{"hit_landed": hit, "frames_before_hit": w.h, "max_before": before.max() if before else null})
	var p_ok: bool = w.p >= 0 and w.z > w.p
	var i0: float = rows[w.p].i if p_ok else -1.0
	var r1_min := 1.0 - (1.0 / fps + PHYSICS_STEP)
	check("R1-value-when-state-begins", p_ok and w.p == w.h and i0 >= r1_min - EPS and i0 <= 1.0,
		{"first_intensity": i0, "min_allowed": r1_min, "hit_row": w.h, "first_positive_row": w.p})
	var mapping_err := 0.0
	var linear_err := 0.0
	if p_ok:
		for k in range(w.p, w.z + 1):
			mapping_err = maxf(mapping_err, absf(rows[k].i - rows[k].inv / Tuning.INVULNERABLE_TIME))
			linear_err = maxf(linear_err, absf((i0 - rows[k].i) - (rows[k].t - rows[w.p].t)))
	check("R2-decreases-linearly-with-game-time", p_ok and non_increasing(w.p, w.z) and mapping_err < EPS
		and linear_err <= PHYSICS_STEP + EPS,
		{"max_abs(intensity - invulnerable/1.0)": mapping_err, "max_abs(drop - game_time)": linear_err, "allowed": PHYSICS_STEP})
	var after_zero := rows.slice(maxi(w.z, 0)).map(func(r: Dictionary) -> float: return r.i) if p_ok else []
	check("R3-zero-when-state-ends-and-stays", p_ok and w.z == w.zi and after_zero.all(func(i: float) -> bool: return i == 0.0)
		and rows.back().t - rows[w.z].t >= 0.3,
		{"first_zero_row": w.z, "first_invulnerable_zero_row": w.zi, "rows_after": after_zero.size(),
		"game_s_after": snappedf(rows.back().t - rows[w.z].t, 0.001) if p_ok else null})
	var dur: float = rows[w.z].t - rows[w.p].t if p_ok else -1.0
	check("R4-duration-1s-game-time", p_ok and absf(dur - 1.0) <= tol + EPS,
		{"fps": fps, "duration_s": snappedf(dur, 0.0001), "tolerance_s": snappedf(tol, 0.0001), "frames": w.z - w.p})
	var blink_ok := p_ok
	var hidden := 0
	if p_ok:
		for k in range(w.p, w.z + 1):
			var r: Dictionary = rows[k]
			var expect: bool = r.inv == 0.0 or int(r.inv / Tuning.BLINK_PERIOD) % 2 == 0
			blink_ok = blink_ok and r.vis == expect
			hidden += 0 if r.vis else 1
	check("R10-blink-unchanged", blink_ok and hidden > 0, {"frames_hidden_in_window": hidden, "matches_player_gd_81": blink_ok})

	# R5 retrigger: a second wolf, added at the hit, lunges into her while the state holds. The hit is ignored
	# (player.gd:152), so intensity keeps falling. The wolf sets _hit_this_lunge even when the hit is ignored.
	await fresh(700)
	key(KEY_D, true)
	hit = await until(func() -> bool: return hurts > 0, frames_for(6.0))
	key(KEY_D, false)
	wolf.set_physics_process(false)
	wolf2 = WOLF_SCENE.instantiate()
	wolf2.target = player
	main.get_node("Level").add_child(wolf2)
	wolf2.global_position = Vector2(maxf(player.global_position.x - 70.0, 600.0), GROUND_TOP)
	await process_frame
	w = window()
	await until(func() -> bool: return since(w.h) >= 1.3, frames_for(2.0))
	w = window()
	rows = sampler.rows
	var c := first(w.h, func(r: Dictionary) -> bool: return r.contact2)
	p_ok = hit and w.p >= 0 and w.z > w.p
	var c_ok: bool = c > w.p and p_ok and rows[c].inv > 0.0
	var max_after_contact := -1.0
	if c_ok:
		for k in range(c, rows.size()):
			max_after_contact = maxf(max_after_contact, rows[k].i)
	check("R5-retrigger-ignored", c_ok and hurts == 1 and player.hp == Tuning.MAX_HP - 1 and non_increasing(w.p, rows.size() - 1)
		and max_after_contact <= rows[c - 1].i + EPS,
		{"second_wolf_contact_row": c, "invulnerable_at_contact": rows[c].inv if c >= 0 else null,
		"intensity_before_contact": rows[c - 1].i if c > 0 else null, "max_intensity_from_contact": max_after_contact,
		"hurts": hurts, "hp": player.hp})

	# R6 time scale: under time_scale 0.5 the state lasts 1.0 s of game time and 2.0 s of real (frame) time.
	await fresh(700)
	Engine.time_scale = 0.5
	hit = await walk_until_hit(KEY_D)
	wolf.set_physics_process(false)
	w = window()
	await until(func() -> bool: return since(w.h) >= 1.3, frames_for(1.5))
	w = window()
	rows = sampler.rows
	p_ok = hit and w.p >= 0 and w.z > w.p
	var game_dur: float = rows[w.z].t - rows[w.p].t if p_ok else -1.0
	var real_dur: float = (w.z - w.p) / fps if p_ok else -1.0
	check("R6-time-scale-0.5", p_ok and absf(game_dur - 1.0) <= tol + EPS and absf(real_dur - 2.0) <= tol / 0.5 + EPS,
		{"game_s": snappedf(game_dur, 0.0001), "real_s": snappedf(real_dur, 0.0001), "frame_delta": rows[w.p].d if p_ok else null,
		"game_tolerance_s": snappedf(tol, 0.0001), "real_tolerance_s": snappedf(tol / 0.5, 0.0001)})
	Engine.time_scale = 1.0

	# R7 pause: Esc about 0.3 s into the state, 30 paused frames, Esc again.
	await fresh(700)
	hit = await walk_until_hit(KEY_D)
	wolf.set_physics_process(false)
	w = window()
	await until(func() -> bool: return since(w.h) >= 0.3, frames_for(1.0))
	tap(KEY_ESCAPE)
	await until(func() -> bool: return sampler.rows.filter(func(r: Dictionary) -> bool: return r.paused).size() >= 30, frames_for(1.0))
	tap(KEY_ESCAPE)
	await until(func() -> bool: return not paused and since(w.h) >= 1.3, frames_for(2.0))
	w = window()
	rows = sampler.rows
	var first_paused := first(0, func(r: Dictionary) -> bool: return r.paused)
	var last_paused := -1
	for k in rows.size():
		if rows[k].paused:
			last_paused = k
	var paused_rows := rows.filter(func(r: Dictionary) -> bool: return r.paused)
	var held: float = rows[first_paused - 1].i if first_paused > 0 else -1.0
	var holds: bool = paused_rows.size() >= 30 and paused_rows.all(func(r: Dictionary) -> bool: return r.i == held)
	var resumed := first(last_paused + 1, func(r: Dictionary) -> bool: return r.i < held - EPS) if last_paused >= 0 else -1
	p_ok = hit and w.p >= 0 and w.z > w.p
	var pause_dur: float = rows[w.z].t - rows[w.p].t if p_ok else -1.0   # observed only (revision 2026-10-23)
	var tick_rise: int = rows[w.z].ticks - rows[w.p].ticks if p_ok else -1
	check("R7-pause-holds-then-resumes", p_ok and holds and held > 0.0 and resumed > last_paused
		and (tick_rise == 59 or tick_rise == 60),
		{"paused_frames": paused_rows.size(), "held_intensity": held, "first_drop_after_resume_row": resumed,
		"physics_ticks_first_tinted_to_first_zero": tick_rise, "game_s_unpaused": snappedf(pause_dur, 0.0001)})

	# R8 / F4: the hit that takes HP to 0. fail() freezes invulnerable at 1.0; intensity must be 0.0 anyway.
	await fresh(700)
	player.hp = 1   # test setup: the next landed hit is the last one
	hit = await walk_until_hit(KEY_D)
	w = window()
	await until(func() -> bool: return since(w.h) >= 1.2, frames_for(1.5))
	rows = sampler.rows
	var from_hit := rows.slice(maxi(w.h, 0))
	check("R8-F4-zero-on-hp0-fail", hit and w.h >= 0 and fails == 1 and fail_reason == "Out of HP"
		and from_hit.all(func(r: Dictionary) -> bool: return r.i == 0.0 and r.failing and r.inv == rows[w.h].inv)
		and rows[w.h].inv > 0.0,
		{"fails": fails, "reason": fail_reason, "frozen_invulnerable": rows[w.h].inv if w.h >= 0 else null,
		"max_intensity_from_hit": from_hit.map(func(r: Dictionary) -> float: return r.i).max() if from_hit else null,
		"frames_checked": from_hit.size()})

	# R8 / F4: a pit fall during the state. The wolf stands right of the pit edge (x 580) and knocks her left;
	# then she holds A into the pit.
	await fresh(600, 660)
	wolf.patrol_left = 620.0
	wolf.patrol_right = 700.0
	hit = await until(func() -> bool: return hurts > 0, frames_for(4.0))
	key(KEY_A, true)
	var fell: bool = await until(func() -> bool: return fails > 0, frames_for(3.0))
	key(KEY_A, false)
	var f_wait_start := sampler.game_time
	await until(func() -> bool: return sampler.game_time - f_wait_start >= 0.5, frames_for(1.0))
	rows = sampler.rows
	w = window()
	var f := first(0, func(r: Dictionary) -> bool: return r.failing)
	var tinted_before: bool = w.p >= 0 and f > w.p
	check("R8-F4-zero-on-pit-fail-during-state", hit and fell and fail_reason == "Fell into the dark" and tinted_before
		and rows[f].inv > 0.0 and rows.slice(f).all(func(r: Dictionary) -> bool: return r.i == 0.0),
		{"reason": fail_reason, "invulnerable_at_fail": rows[f].inv if f >= 0 else null,
		"intensity_row_before_fail": rows[f - 1].i if f > 0 else null, "game_s_hit_to_fail": snappedf(rows[f].t - rows[w.h].t, 0.001) if f >= 0 and w.h >= 0 else null})

	# R8: clearing during the state. The wolf stands left of her near the exit and knocks her right; she holds D.
	await fresh(1180, 1110)
	wolf.patrol_left = 1080.0
	wolf.patrol_right = 1140.0
	hit = await until(func() -> bool: return hurts > 0, frames_for(4.0))
	key(KEY_D, true)
	var won: bool = await until(func() -> bool: return clears > 0, frames_for(3.0))
	key(KEY_D, false)
	var g_wait_start := sampler.game_time
	await until(func() -> bool: return sampler.game_time - g_wait_start >= 0.5, frames_for(1.0))
	rows = sampler.rows
	w = window()
	var g := first(0, func(r: Dictionary) -> bool: return r.cleared)
	check("R8-zero-on-clear-during-state", hit and won and clears == 1 and w.p >= 0 and g > w.p
		and rows[g - 1].inv > 0.0 and rows[g - 1].i > 0.0 and rows.slice(g).all(func(r: Dictionary) -> bool: return r.i == 0.0),
		{"clears": clears, "invulnerable_row_before_clear": rows[g - 1].inv if g > 0 else null,
		"intensity_row_before_clear": rows[g - 1].i if g > 0 else null, "game_s_hit_to_clear": snappedf(rows[g].t - rows[w.h].t, 0.001) if g >= 0 and w.h >= 0 else null})

	# R9: reload mid-state. The new scene's material is a different object, starts unset (the shader default,
	# 0.0 per the source text), and its first sampled frame reads 0.0.
	await fresh(700)
	hit = await walk_until_hit(KEY_D)
	wolf.set_physics_process(false)
	w = window()
	await until(func() -> bool: return since(w.h) >= 0.2, frames_for(1.0))
	var old_mat := player.sprite.material as ShaderMaterial
	var old_i: float = old_mat.get_shader_parameter("intensity")
	await fresh(700)
	var new_mat := player.sprite.material as ShaderMaterial
	var unset: Variant = new_mat.get_shader_parameter("intensity")
	await until(func() -> bool: return sampler.rows.size() >= 1, 5)
	var first_i: float = sampler.rows[0].i if sampler.rows.size() > 0 else -1.0
	check("R9-reload-starts-at-default", hit and old_i > 0.0 and new_mat != old_mat and (unset == null or unset == 0.0)
		and first_i == 0.0,
		{"old_intensity": old_i, "same_material_object": new_mat == old_mat, "new_before_first_frame": unset,
		"new_first_frame": first_i})

	print("WALKER TESTS: %d checks / %d failures" % [results.size(), failures])
	quit(1 if failures else 0)

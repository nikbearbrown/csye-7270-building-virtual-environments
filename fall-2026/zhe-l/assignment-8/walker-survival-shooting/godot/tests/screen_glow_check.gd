extends SceneTree

const SHADER_PATH := "res://shaders/pad_base_light.gdshader"
const BASE_SCENE := "res://base.tscn"
const HUMANOID_SCENE := "res://characters/human/humanoid/humanoid.tscn"
const PARAM := &"pad_light_data"
const LIT := 0.39
const OFF := 0.0
const MOVE_SECONDS := 20.0 / 30.0
const READ_LAG_FRAMES := 1
const ONE_TO_TWO_SECONDS := (28.0 - 16.0) / 30.0
const BLEND_SECONDS := 0.2
const SLOW_TIME_SCALE := 0.5
const TAP_SECONDS := 0.1
const HOLD_SECONDS := 0.5
const SETTLE_SECONDS := 1.0
const QUICK_BACK_SECONDS := 0.1
const EPS := 0.0001

var failures := 0
var player: Humanoid
var other: Humanoid
var player_mat: ShaderMaterial
var other_mat: ShaderMaterial
var sampler: Sampler
var change_physics_frame := -1
var change_hold := -1

class Sampler extends Node:
	var player: Humanoid
	var player_mat: ShaderMaterial
	var other_mat: ShaderMaterial
	var game_time := 0.0
	var frame_delta := 0.0
	var samples: Array[Dictionary] = []

	func _process(delta: float) -> void:
		game_time += delta
		frame_delta = delta
		samples.append({
			"t": game_time,
			"pf": Engine.get_physics_frames(),
			"hold": player.get_tablet_hold(),
			"pad": float(player_mat.get_shader_parameter(&"pad_light_data")),
			"other": float(other_mat.get_shader_parameter(&"pad_light_data")),
		})


class IdleBrain extends Node:
	var body: Humanoid

	func _physics_process(delta: float) -> void:
		body.apply_intent(CharacterIntent.new(), delta)


func _initialize() -> void:
	_run()


func _run() -> void:
	_check_shader()
	await _build_scene()
	_check_materials()
	await _scenario()
	print("== %s: %d failure(s) ==" % ["ALL PASS" if failures == 0 else "FAILED", failures])
	quit(1 if failures > 0 else 0)


func _check(ok: bool, what: String) -> void:
	print(("  PASS  " if ok else "  FAIL  ") + what)
	if not ok:
		failures += 1


func _check_shader() -> void:
	var shader: Shader = load(SHADER_PATH)
	var uniforms := {}
	for u in shader.get_shader_uniform_list():
		uniforms[u["name"]] = u
	_check(uniforms.has("cold_white") and uniforms["cold_white"]["type"] == TYPE_COLOR,
		"uniform cold_white exists and is a colour (source_color)")
	_check(uniforms.has("pad_light_data") and uniforms["pad_light_data"]["type"] == TYPE_FLOAT,
		"uniform pad_light_data exists and is a float")
	_check(uniforms.has("pad_light_data") and uniforms["pad_light_data"]["hint"] == PROPERTY_HINT_RANGE
		and String(uniforms["pad_light_data"]["hint_string"]).begins_with("0.0,1.0"),
		"pad_light_data has hint_range(0.0, 1.0)")
	var source := FileAccess.get_file_as_string(SHADER_PATH)
	var re_color := RegEx.create_from_string(
		"uniform\\s+vec4\\s+cold_white\\s*:\\s*source_color\\s*=\\s*vec4\\(\\s*0\\.902\\s*,\\s*0\\.969\\s*,\\s*0\\.969\\s*,\\s*1\\.0\\s*\\)")
	var re_float := RegEx.create_from_string(
		"uniform\\s+float\\s+pad_light_data\\s*:\\s*hint_range\\(\\s*0\\.0\\s*,\\s*1\\.0\\s*\\)\\s*=\\s*0\\.0\\s*;")
	_check(re_color.search(source) != null, "source: cold_white has source_color and default vec4(0.902, 0.969, 0.969, 1.0)")
	_check(re_float.search(source) != null, "source: pad_light_data default is 0.0")


func _build_scene() -> void:
	var base: Node = load(BASE_SCENE).instantiate()
	root.add_child(base)
	player = base.get_node("Player")
	other = load(HUMANOID_SCENE).instantiate()
	other.position = Vector3(-3.0, 0.25, 1.5)
	base.add_child(other)
	var brain := IdleBrain.new()
	brain.body = other
	other.add_child(brain)
	await process_frame
	player_mat = player.get_tablet().get_screen().get_surface_override_material(0)
	other_mat = other.get_tablet().get_screen().get_surface_override_material(0)
	player.tablet_hold_changed.connect(_on_hold_changed)
	sampler = Sampler.new()
	sampler.process_priority = 1000
	sampler.player = player
	sampler.player_mat = player_mat
	sampler.other_mat = other_mat
	root.add_child(sampler)
	await process_frame


func _check_materials() -> void:
	_check(player_mat != null and player_mat.shader != null and player_mat.shader.resource_path == SHADER_PATH,
		"player Screen uses a ShaderMaterial with pad_base_light.gdshader")
	_check(player_mat != null and player_mat.resource_local_to_scene, "Screen material has Local To Scene")
	_check(player_mat != other_mat, "the two bodies' screen materials are different objects")


func _on_hold_changed(_old_hold: Humanoid.TabletHold, new_hold: Humanoid.TabletHold) -> void:
	change_physics_frame = Engine.get_physics_frames()
	change_hold = new_hold


func _tab(pressed: bool) -> void:
	var event := InputEventKey.new()
	event.physical_keycode = KEY_TAB
	event.pressed = pressed
	Input.parse_input_event(event)


func _wait(seconds: float) -> void:
	var end := sampler.game_time + seconds
	while sampler.game_time < end - EPS:
		await process_frame


func _press(hold_seconds: float) -> void:
	_tab(true)
	await _wait(hold_seconds)
	var physics_before := Engine.get_physics_frames()
	_tab(false)
	while Engine.get_physics_frames() <= physics_before:
		await process_frame
	await process_frame


func _first_lit(from_index: int) -> int:
	for i in range(from_index, sampler.samples.size()):
		if absf(sampler.samples[i]["pad"] - LIT) < EPS:
			return i
	return -1


func _any_pad(from_index: int, value: float) -> bool:
	for i in range(from_index, sampler.samples.size()):
		if absf(sampler.samples[i]["pad"] - value) < EPS:
			return true
	return false


func _lit_delay(lit_index: int) -> float:
	var ticks: int = sampler.samples[lit_index]["pf"] - change_physics_frame + 1
	return ticks * Engine.time_scale / float(Engine.physics_ticks_per_second)


func _scenario() -> void:
	await _wait(0.2)
	var fps := 1.0 / sampler.frame_delta
	var tolerance := sampler.frame_delta + EPS
	print("  (fps %.0f, frame period %.4f s, physics %d ticks/s)" % [fps, sampler.frame_delta, Engine.physics_ticks_per_second])
	_check(not _any_pad(0, LIT) and absf(sampler.samples[-1]["pad"] - OFF) < EPS, "4  NONE at start: screen 0.0")

	var start := sampler.samples.size()
	await _press(TAP_SECONDS)
	var changed_at := sampler.samples.size() - 1
	await _wait(SETTLE_SECONDS)
	var lit := _first_lit(start)
	_check(change_hold == Humanoid.TabletHold.ONE_HAND, "5  short press: NONE -> ONE_HAND")
	_check(lit > changed_at, "5  screen still 0.0 on the frame the state changed")
	if lit >= 0:
		var delay := _lit_delay(lit)
		print("     lit %.4f s after the state change (frame-based: %.4f s)" % [delay, sampler.samples[lit]["t"] - sampler.samples[changed_at]["t"]])
		_check(absf(delay - (MOVE_SECONDS + READ_LAG_FRAMES * sampler.frame_delta)) <= tolerance, "5  lit %.2f s + 1 frame (measured read lag) +- one frame after the state change" % MOVE_SECONDS)
	_check(lit >= 0 and absf(sampler.samples[lit]["pad"] - player.get_tablet().light_strength_percentage) < EPS,
		"12 lit value equals light_strength_percentage (0.39)")

	for step in [[HOLD_SECONDS, Humanoid.TabletHold.TWO_HAND, "long press: ONE_HAND -> TWO_HAND", ONE_TO_TWO_SECONDS + READ_LAG_FRAMES * sampler.frame_delta],
			[TAP_SECONDS, Humanoid.TabletHold.ONE_HAND, "short press: TWO_HAND -> ONE_HAND", BLEND_SECONDS]]:
		start = sampler.samples.size()
		await _press(step[0])
		_check(change_hold == step[1], "6  " + step[2])
		await _wait(SETTLE_SECONDS)
		_check(_any_pad(start, OFF), "6  dark while switching (%s)" % step[2])
		lit = _first_lit(start)
		_check(lit >= 0 and _lit_delay(lit) <= step[3] + 2.0 * tolerance, "6  lit again in time (%s)" % step[2])
		_check(absf(sampler.samples[-1]["pad"] - LIT) < EPS, "6  lit once settled (%s)" % step[2])

	start = sampler.samples.size()
	await _press(TAP_SECONDS)
	_check(change_hold == Humanoid.TabletHold.NONE, "7  short press: ONE_HAND -> NONE")
	var first_none := -1
	for i in range(start, sampler.samples.size()):
		if sampler.samples[i]["hold"] == Humanoid.TabletHold.NONE:
			first_none = i
			break
	_check(first_none >= 0 and absf(sampler.samples[first_none]["pad"] - OFF) < EPS, "7  0.0 on the same frame the state becomes NONE")
	await _wait(SETTLE_SECONDS)

	start = sampler.samples.size()
	await _press(TAP_SECONDS)
	await _wait(QUICK_BACK_SECONDS)
	await _press(TAP_SECONDS)
	_check(change_hold == Humanoid.TabletHold.NONE, "8  out and back: ends in NONE")
	await _wait(SETTLE_SECONDS)
	_check(not _any_pad(start, LIT), "8  put away before reaching the hand: never lit")

	await _press(TAP_SECONDS)
	await _wait(SETTLE_SECONDS)
	await _press(TAP_SECONDS)
	await _wait(QUICK_BACK_SECONDS)
	start = sampler.samples.size()
	await _press(TAP_SECONDS)
	_check(change_hold == Humanoid.TabletHold.ONE_HAND, "9  taken out again mid-way")
	await _wait(SETTLE_SECONDS)
	lit = _first_lit(start)
	if lit >= 0:
		print("     lit %.4f s after the second take-out" % _lit_delay(lit))
	_check(lit >= 0 and absf(_lit_delay(lit) - (MOVE_SECONDS + READ_LAG_FRAMES * sampler.frame_delta)) <= tolerance, "9  restart: lit %.2f s + 1 frame +- one frame after the last take-out" % MOVE_SECONDS)
	await _press(TAP_SECONDS)
	await _wait(SETTLE_SECONDS)

	Engine.time_scale = SLOW_TIME_SCALE
	start = sampler.samples.size()
	await _press(TAP_SECONDS)
	await _wait(SETTLE_SECONDS)
	lit = _first_lit(start)
	if lit >= 0:
		var scaled := _lit_delay(lit)
		print("     time_scale %.1f: lit %.4f s scaled game time = %.4f s real time" % [SLOW_TIME_SCALE, scaled, scaled / SLOW_TIME_SCALE])
		_check(absf(scaled - (MOVE_SECONDS + READ_LAG_FRAMES * sampler.frame_delta)) <= tolerance, "11 time_scale %.1f: %.2f s + 1 frame of scaled game time" % [SLOW_TIME_SCALE, MOVE_SECONDS])
	else:
		_check(false, "11 time_scale %.1f: screen never lit" % SLOW_TIME_SCALE)
	Engine.time_scale = 1.0
	await _press(TAP_SECONDS)
	await _wait(SETTLE_SECONDS)

	var other_lit := false
	for s in sampler.samples:
		if absf(s["other"] - OFF) > EPS:
			other_lit = true
	_check(not other_lit, "10 the second body's screen stayed 0.0 on every frame (%d frames)" % sampler.samples.size())

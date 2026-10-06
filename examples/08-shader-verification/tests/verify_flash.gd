extends SceneTree
## Student-written verification for the Chapter 6 failure flash (not the agent's test).
## Run at several pinned frame rates:
##   godot --headless --path godot --script res://tests/verify_flash.gd --fixed-fps 30
##   (repeat with 60 and 144)
## Then grep the log: any "SHADER ERROR" line is a failure whatever the exit code says.
## Headless = dummy renderer: this measures the uniform the shader receives, never pixels.

const Game = preload("res://game/session.gd")
const SHADER_PATH := "res://features/player/clawd_flash.gdshader"
var failures := 0


class Sampler extends Node:
	## Runs after every other _process in the frame, so the flash value and the
	## session countdown it reads belong to the same frame.
	var game: Node2D
	var mat: ShaderMaterial
	var rows: Array = []
	var frame := 0

	func _ready() -> void:
		process_priority = 1000

	func _process(delta: float) -> void:
		frame += 1
		rows.append({"frame": frame, "delta": delta, "state": game.state, "remaining": game.retry_remaining, "flash": float(mat.get_shader_parameter("flash_amount"))})


func check(id: String, passed: bool, observed) -> void:
	print(JSON.stringify({"id": id, "status": "PASS" if passed else "FAIL", "observed": observed}))
	if not passed:
		failures += 1


func _initialize() -> void:
	run.call_deferred()


func uniform_checks() -> void:
	var shader: Shader = load(SHADER_PATH)
	var mat := ShaderMaterial.new()
	mat.shader = shader # first use: the headless shader parser runs here
	var by_name := {}
	for u in shader.get_shader_uniform_list():
		by_name[u.name] = u
	# A shader that fails to parse reports an empty uniform list.
	check("uniform list has both uniforms (parse succeeded)", by_name.size() == 2, by_name.keys())
	var fa: Dictionary = by_name.get("flash_amount", {})
	check("flash_amount is float with a 0..1 range hint", fa.get("type") == TYPE_FLOAT and fa.get("hint") == PROPERTY_HINT_RANGE and str(fa.get("hint_string", "")).begins_with("0.0,1.0"), fa)
	var fc: Dictionary = by_name.get("flash_color", {})
	check("flash_color is a Color uniform", fc.get("type") == TYPE_COLOR, fc)
	# Defaults are not readable from the dummy renderer; read the source text.
	var rx := RegEx.create_from_string("uniform\\s+vec4\\s+flash_color[^=]*=\\s*vec4\\(([^)]*)\\)")
	var m := rx.search(shader.code)
	var parsed := []
	var ok := false
	if m:
		for part in m.get_string(1).split(","):
			parsed.append(float(part))
		var want := Color("25354a")
		ok = absf(parsed[0] - want.r) < 0.5 / 255.0 and absf(parsed[1] - want.g) < 0.5 / 255.0 and absf(parsed[2] - want.b) < 0.5 / 255.0
	check("flash_color default is #25354a (from source text)", ok, parsed)


func run() -> void:
	uniform_checks()
	var game: Node2D = Game.new()
	game.test_mode = true
	root.add_child(game)
	await process_frame
	game.start_session()
	for i in range(4):
		await process_frame
	var mat := game.player.material as ShaderMaterial
	check("Clawd carries the flash ShaderMaterial", mat != null and mat.shader != null and mat.shader.resource_path == SHADER_PATH, str(mat))
	var sampler := Sampler.new()
	sampler.game = game
	sampler.mat = mat
	root.add_child(sampler)
	for i in range(3):
		await process_frame
	check("flash is 0 while playing", sampler.rows.all(func(r): return r.state == Game.State.PLAYING and is_zero_approx(r.flash)), sampler.rows.size())

	# A real failure: drop Clawd below the level's fall line; the session detects it.
	sampler.rows.clear()
	game.player.position.y = float(game.level.fall_y) + 5.0
	var guard := 0
	while guard < 400:
		await process_frame
		guard += 1
		if sampler.rows.size() > 2 and sampler.rows[-1].state == Game.State.PLAYING and sampler.rows.any(func(r): return r.state == Game.State.DYING):
			break
	var dying: Array = sampler.rows.filter(func(r): return r.state == Game.State.DYING)
	var after: Array = sampler.rows.filter(func(r): return r.state == Game.State.PLAYING and r.frame > dying[-1].frame) if dying.size() > 0 else []
	var max_gap := 0.0
	for r in dying:
		max_gap = maxf(max_gap, absf(r.flash - clampf(r.remaining / 0.55, 0.0, 1.0)))
	var seconds := 0.0
	for r in dying:
		seconds += r.delta
	var fps: float = snappedf(dying.size() / seconds, 0.1) if seconds > 0.0 else 0.0
	print(JSON.stringify({"average_frame_rate": fps, "frames_in_failure": dying.size(), "seconds_in_failure": seconds, "first_flash": dying[0].flash if dying.size() else -1, "last_flash_before_retry": dying[-1].flash if dying.size() else -1, "max_gap_vs_countdown": max_gap}))
	check("first failure frame flash >= 0.96", dying.size() > 0 and dying[0].flash >= 0.96, dying[0].flash if dying.size() else null)
	check("flash equals countdown / 0.55 on every failure frame", dying.size() > 0 and max_gap < 0.0001, max_gap)
	check("failure lasts 0.55 s of game time (within one 30 fps frame)", absf(seconds - 0.55) <= 1.0 / 30.0 + 0.0001, seconds)
	check("last failure frame flash <= 0.07", dying.size() > 0 and dying[-1].flash <= 0.07, dying[-1].flash if dying.size() else null)
	check("flash is 0 on the first frame after the retry", after.size() > 0 and is_zero_approx(after[0].flash), after[0].flash if after.size() else null)

	# A real R key event in the middle of a failure.
	sampler.rows.clear()
	game.player.position.y = float(game.level.fall_y) + 5.0
	guard = 0
	while guard < 60:
		await process_frame
		guard += 1
		if sampler.rows.size() > 0 and sampler.rows[-1].state == Game.State.DYING and sampler.rows[-1].flash < 0.8:
			break
	var before: float = sampler.rows[-1].flash
	for pressed in [true, false]:
		var ev := InputEventKey.new()
		ev.physical_keycode = KEY_R
		ev.keycode = KEY_R
		ev.pressed = pressed
		root.push_input(ev, true)
		await process_frame
	var now: Dictionary = sampler.rows[-1]
	check("R during failure: flash was on, then 0 in the next frame", before > 0.3 and now.state == Game.State.PLAYING and is_zero_approx(now.flash), [before, now])

	sampler.queue_free()
	game.queue_free()
	await process_frame
	print("VERIFY_FLASH failures=", failures)
	quit(1 if failures else 0)

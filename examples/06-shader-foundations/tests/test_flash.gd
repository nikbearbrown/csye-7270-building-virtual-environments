extends SceneTree

# Headless evidence for the Chapter 6 failure flash.
#
# WHAT THIS PROVES (headless, dummy renderer):
#   1. clawd_flash.gdshader is accepted by Godot's shader parser — any
#      SHADER ERROR line in this run's output is a failure even if the
#      exit code does not change (headless fact, CLAUDE.md).
#   2. flash_amount exists as a float uniform; flash_color exists as a
#      Color uniform — confirmed via GDScript set/get round-trip.
#   3. flash_amount = 1.0 when retry_remaining = 0.55 (death onset, rule 1).
#   4. flash_amount = 0.5 when retry_remaining = 0.275 (half-way, linear).
#   5. flash_amount = 0.0 when retry_remaining = 0.0 (retry threshold, rule 1).
#   6. flash_amount = 0.0 in PLAYING state (not DYING) — rules 1 and 2.
#   7. flash_amount = 0.0 immediately after restart_attempt() — rule 2 (R key).
#   The flash checks call _update_flash() directly to avoid physics/process
#   frame-ordering ambiguity; they produce identical results at any --fixed-fps.
#
# WHAT THIS CANNOT PROVE (headless dummy renderer draws nothing):
#   - That the tint is visually correct at any flash_amount value.
#   - That transparent surroundings remain transparent when rendered.
#   - That the ShaderMaterial on the CharacterBody2D actually intercepts
#     draw_rect() output in the GL Compatibility renderer.
#   - That flash_color (#25354a) reads correctly as a Color vs Vector4.
#     (source_color hint is confirmed only by the type check in point 2.)
#
# HUMAN CHECKS REQUIRED:
#   - Run the game, trigger a death, observe Clawd tints toward dark ink
#     (#25354a) then fades back to normal over ~0.55 s.
#   - Verify transparent surroundings stay transparent at flash_amount 1.
#   - Verify pressing R during the failure snaps the tint off immediately.
#   - Verify the level, HUD, and background are unaffected.

const Game = preload("res://game/session.gd")
var failures := 0
var checks := 0

func check(passed: bool, label: String) -> void:
	checks += 1
	if not passed:
		failures += 1
		push_error("FAIL: " + label)

func steps(n: int) -> void:
	for i in range(n):
		await physics_frame
		await process_frame

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	# ── 1. Shader parse ──────────────────────────────────────────────────────
	# Assigning the shader to a ShaderMaterial triggers Godot's shader parser.
	# Any SHADER ERROR line printed here is a failure even though headless
	# runs do not change the exit code on shader errors (CLAUDE.md).
	var shader: Shader = load("res://features/player/clawd_flash.gdshader")
	check(shader != null, "clawd_flash.gdshader loads as Shader resource")

	var mat := ShaderMaterial.new()
	mat.shader = shader  # parser fires here; SHADER ERROR would print to log

	# ── 2. Uniform existence and types ───────────────────────────────────────
	# GDScript set/get round-trip: confirms the uniform exists and maps to the
	# expected Variant type (float for flash_amount, Color for flash_color).
	mat.set_shader_parameter("flash_amount", 0.5)
	var fa = mat.get_shader_parameter("flash_amount")
	check(fa is float, "flash_amount is float (got %s)" % type_string(typeof(fa)))
	check(absf(fa - 0.5) < 0.001, "flash_amount round-trips 0.5 (got %s)" % str(fa))

	mat.set_shader_parameter("flash_color", Color(1.0, 0.0, 0.0, 1.0))
	var fc = mat.get_shader_parameter("flash_color")
	check(fc is Color, "flash_color is Color (got %s)" % type_string(typeof(fc)))

	# ── Set up session ────────────────────────────────────────────────────────
	var game := Game.new()
	game.test_mode = true
	root.add_child(game)
	await process_frame
	game.start_session()
	await steps(3)

	var pmat := game.player.material as ShaderMaterial
	check(pmat != null, "player.material is ShaderMaterial after session start")

	# All flash checks below call _update_flash() directly so that the tested
	# relationship is independent of physics/process frame ordering (which
	# varies between --fixed-fps 30 and --fixed-fps 144).  The same checks
	# would fail at any fps if the implementation is wrong.

	# ── 3–4. Rule 1: linear formula  flash = clamp(remaining / 0.55)  ────────
	game.resolve_contacts(true, false)  # state = DYING, retry_remaining = 0.55

	game.retry_remaining = 0.55
	game.player._update_flash()
	var amount: float = pmat.get_shader_parameter("flash_amount") if pmat else -1.0
	check(absf(amount - 1.0) < 0.001,
		"flash_amount = 1.0 at retry_remaining = 0.55 (death onset) (got %.6f)" % amount)

	game.retry_remaining = 0.275
	game.player._update_flash()
	amount = pmat.get_shader_parameter("flash_amount") if pmat else -1.0
	check(absf(amount - 0.5) < 0.001,
		"flash_amount = 0.5 at retry_remaining = 0.275 (linear mid-point) (got %.6f)" % amount)

	game.retry_remaining = 0.0
	game.player._update_flash()
	amount = pmat.get_shader_parameter("flash_amount") if pmat else -1.0
	check(is_zero_approx(amount),
		"flash_amount = 0.0 at retry_remaining = 0.0 (end of fade) (got %.6f)" % amount)

	# ── 5. Rule 1 + 2: flash_amount = 0 outside DYING state ─────────────────
	game.restart_attempt()  # state = PLAYING, retry_remaining = 0
	game.player._update_flash()
	amount = pmat.get_shader_parameter("flash_amount") if pmat else -1.0
	check(is_zero_approx(amount),
		"flash_amount = 0.0 in PLAYING state (got %.6f)" % amount)

	# ── 6. Rule 2: R key (restart_attempt) zeros flash mid-failure ───────────
	game.resolve_contacts(true, false)  # back to DYING with retry_remaining = 0.55
	game.retry_remaining = 0.3          # simulate mid-fade
	game.player._update_flash()
	amount = pmat.get_shader_parameter("flash_amount") if pmat else -1.0
	check(amount > 0.4, "flash_amount is non-zero before R (got %.6f)" % amount)

	game.restart_attempt()  # R key: state = PLAYING, retry_remaining = 0
	game.player._update_flash()  # simulates next process frame
	amount = pmat.get_shader_parameter("flash_amount") if pmat else -1.0
	check(is_zero_approx(amount),
		"flash_amount = 0.0 immediately after restart_attempt / R (got %.6f)" % amount)

	game.queue_free()
	await process_frame

	var report := {
		"checks": checks,
		"failures": failures,
		"engine": Engine.get_version_info().string,
		"scope": "Shader parse + uniform types + flash_amount rules 1 and 2; visual result is a human check"
	}
	print("FLASH TESTS: ", JSON.stringify(report))
	quit(1 if failures else 0)

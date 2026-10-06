extends SceneTree

var failures := 0

func _initialize() -> void:
	call_deferred("run")

func check(ok: bool, label: String) -> void:
	if not ok:
		failures += 1
	print("PASS " if ok else "FAIL ", label)

func click(button: Button) -> void:
	for down in [true, false]:
		var event := InputEventMouseButton.new()
		event.position = button.get_global_rect().get_center()
		event.global_position = event.position
		event.button_index = MOUSE_BUTTON_LEFT
		event.pressed = down
		root.push_input(event, true)
		await process_frame

func run() -> void:
	seed(123)
	root.size = Vector2i(480, 720)
	var game: Node = load("res://main.tscn").instantiate()
	root.add_child(game)
	await process_frame
	await process_frame

	var player: Area2D = game.get_node("Player")
	var burst: GPUParticles2D = game.get_node("DeathBurst")

	# Static property checks — independent of rendering or gameplay state.
	check(burst.texture is GradientTexture2D, "texture is GradientTexture2D (soft round dot)")
	var mat := burst.process_material as ParticleProcessMaterial
	check(mat != null and mat.particle_flag_disable_z, "particle_flag_disable_z enabled for 2D")

	# Before any game starts the burst must be silent.
	check(not burst.emitting, "not emitting at load, before Start")

	await click(game.get_node("HUD/StartButton"))
	await process_frame

	# Still quiet after Start; fire has not been triggered yet.
	check(not burst.emitting, "not emitting after Start, before hit")

	# Capture the player's position now; force a hit with a frozen mob.
	var hit_pos := player.global_position
	var mob: RigidBody2D = load("res://mob.tscn").instantiate()
	mob.position = player.position
	mob.freeze = true
	game.add_child(mob)
	await create_timer(0.15).timeout

	# Headless note: GPUParticles2D.emitting reads back through the dummy
	# RenderingServer which always returns false in --headless mode.
	# These three checks verify CPU-side state that IS observable without a display.
	check(burst.emitting, "emitting after hit")
	check(burst.is_visible_in_tree(), "burst is_visible_in_tree after hit")
	check(burst.global_position.is_equal_approx(hit_pos), "burst global_position equals player hit position")

	# Wait up to lifetime + 0.5 s for the one-shot finished signal.
	# Use a Dictionary so the lambda captures a reference, not a value copy —
	# GDScript lambdas cannot reassign an outer local variable.
	var sig := {"done": false}
	burst.finished.connect(func(): sig.done = true, CONNECT_ONE_SHOT)
	await create_timer(burst.lifetime + 0.5).timeout
	check(sig.done, "finished signal arrives within lifetime + 0.5 s")

	# Wait out the rest of the HUD game-over flow before the restart button appears.
	# From mob addition: 0.15 + 1.1 + 1.1 = 2.35 s total, matching test_input.gd.
	await create_timer(1.1).timeout
	await click(game.get_node("HUD/StartButton"))
	await process_frame

	# Force a second death to confirm the burst re-fires.
	var mob2: RigidBody2D = load("res://mob.tscn").instantiate()
	mob2.position = player.position
	mob2.freeze = true
	game.add_child(mob2)
	await create_timer(0.15).timeout

	check(burst.emitting, "emits again on second death")

	game.get_node("Music").stop()
	game.get_node("DeathSound").stop()
	await create_timer(0.25).timeout
	print("RESULT failures=", failures, "; headless state and collision fixture, not footage")
	print("SCREEN CHECK (requires display): 32 white particles spray in all directions from")
	print("  the player's position at death, shrink and fade to transparent over 0.6 s,")
	print("  and the burst repeats identically on the second death.")
	quit(1 if failures else 0)

extends SceneTree
const Garden = preload("res://signal-garden/garden.gd")
var game: Node3D
var failures := 0
var rows: Array = []
func _initialize() -> void: call_deferred("run")
func steps(n: int) -> void:
	for i in range(n):
		await physics_frame
		await process_frame
func check(id: String, ok: bool, observation: Variant = "") -> void:
	rows.append({"id": id, "pass": ok, "observation": observation})
	print(JSON.stringify(rows.back()))
	if not ok: failures += 1
func press(action: String, n: int) -> void:
	Input.action_press(action)
	await steps(n)
	Input.action_release(action)
	await steps(1)
func reset() -> void:
	await press("garden_reset", 1)
	await steps(3)
func run() -> void:
	game = Garden.new()
	game.audio_enabled = false
	root.add_child(game)
	await steps(4)
	check("initial-state", not game.gate_open and not game.burst.emitting and not game.ambient.emitting)
	check("model-rig", game.rig.skeleton.get_bone_count() == 9, game.rig.skeleton.get_bone_count())
	check("AC-02-invalid-interaction-silent", game.sound.counts.charge == 0)
	await press("garden_action", 2)
	check("AC-02-outside-pad", not game.charging and game.sound.counts.charge == 0)
	var start_x: float = game.player.position.x
	Input.action_press("garden_right")
	await steps(30)
	check("AC-01-input-motion", absf(game.player.position.x - start_x - 1.5) <= 0.10, game.player.position.x - start_x)
	check("animation-walk", game.state == "walk" and game.rig.current == "walk")
	check("rig-bone-actually-moves", game.rig.skeleton.get_bone_pose_rotation(game.rig.skeleton.find_bone("Leg.1")).get_angle() > 0.1)
	Input.action_release("garden_right")
	await steps(2)
	await press("garden_right", 160)
	check("AC-04-closed-gate-blocks", game.player.position.x < 0.6, game.player.position.x)
	await reset()
	check("AC-05-reset-start", game.player.position.distance_to(game.get_node("StartReference").position) < 0.05)
	await press("garden_right", 40)
	check("pad-reached-by-input", absf(game.player.position.x + 2.0) < 0.12, str(game.player.position))
	var before: Vector3 = game.player.position
	Input.action_press("garden_action")
	await steps(18)
	check("TIMING-charge-midpoint", game.charging and not game.gate_open, game.charge)
	check("shader-midpoint", absf(float(game.pad_material.get_shader_parameter("activation")) - 0.5) < 0.07)
	check("animation-charge", game.rig.current == "charge")
	Input.action_press("garden_right")
	await steps(10)
	check("INVARIANT-committed-action-locks-motion", game.player.position.distance_to(before) < 0.02)
	Input.action_release("garden_right")
	await steps(10)
	check("AC-03-gate-open", game.gate_open and not game.charging)
	check("held-action-single-trigger", game.action_count == 1 and game.sound.counts.charge == 1 and game.sound.counts.gate == 1)
	check("particles-real-gate-event", game.burst.emitting and game.burst.is_visible_in_tree() and game.ambient.emitting)
	Input.action_release("garden_action")
	await steps(2)
	await press("garden_action", 1)
	check("repeat-action-on-open-gate-ignored", game.action_count == 1)
	game.visible = false
	await steps(2)
	check("ambient-stops-when-hidden", not game.ambient.emitting)
	game.visible = true
	await steps(50)
	check("burst-finishes", not game.burst.emitting)
	check("simple-gate-animation", absf(game.gate_mesh.position.y - 3.0) < 0.01)
	await press("garden_right", 140)
	check("AC-04-input-finish", game.won and game.finish_count == 1 and game.sound.counts.finish == 1, game.player.position.x)
	check("animation-celebrate", game.rig.current == "celebrate")
	check("ambient-stops-at-finish", not game.ambient.emitting)
	for name in ["idle", "walk", "celebrate"]:
		var clip: Animation = game.rig.animator.get_animation(name)
		var seam := clip.loop_mode == Animation.LOOP_LINEAR
		for t in range(clip.get_track_count()):
			seam = seam and clip.track_get_key_value(t, 0).is_equal_approx(clip.track_get_key_value(t, clip.track_get_key_count(t)-1))
		check("cycle-seam-"+name, seam)
	await reset()
	await press("garden_right", 40)
	await press("garden_action", 10)
	await press("garden_reset", 1)
	check("reset-interrupts-action", not game.charging and not game.gate_open and game.charge == 0.0)
	await steps(40)
	check("no-delayed-gate-after-reset", not game.gate_open)
	check("material-color-role", game.gate_mesh.material_override.albedo_texture.resource_path.ends_with("gate-color.png"))
	check("material-data-role", game.gate_mesh.material_override.roughness_texture.resource_path.ends_with("gate-roughness.png"))
	check("particle-resources", game.burst.mesh != null and game.ambient.mesh != null and game.burst.one_shot and game.burst.amount == 32 and game.ambient.amount == 48)
	print("RESULT %d checks / %d failures" % [rows.size(), failures])
	game.queue_free()
	await process_frame
	quit(1 if failures else 0)

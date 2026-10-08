extends SceneTree
## Independent check written by the human reviewer, not by the agent.
## Run with --fixed-fps 60 so one process frame is one physics tick.
## Fixture control is explicit: naturally spawned mobs are removed so that the
## only mob the player touches is the frozen fixture. Nothing calls a signal
## handler or writes the shield state.

var failures := 0

func _initialize() -> void:
	call_deferred("run")

func check(ok: bool, label: String) -> void:
	if not ok:
		failures += 1
	print("PASS " if ok else "FAIL ", label)

func key(code: Key, down: bool) -> void:
	var event := InputEventKey.new()
	event.physical_keycode = code
	event.pressed = down
	Input.parse_input_event(event)
	await physics_frame

func click(button: Button) -> void:
	for down in [true, false]:
		var event := InputEventMouseButton.new()
		event.position = button.get_global_rect().get_center()
		event.global_position = event.position
		event.button_index = MOUSE_BUTTON_LEFT
		event.pressed = down
		root.push_input(event, true)
		await physics_frame

func clear_natural_mobs(keep: Node) -> void:
	for m in get_nodes_in_group("mobs"):
		if m != keep:
			m.queue_free()

func run() -> void:
	seed(7270)
	root.size = Vector2i(480, 720)
	var game: Node = load("res://main.tscn").instantiate()
	root.add_child(game)
	await physics_frame
	await physics_frame
	var player: Area2D = game.get_node("Player")

	# 1. Layer and mask contract, read from the running nodes.
	var probe: Area2D = load("res://pickup.tscn").instantiate()
	var mob_probe: RigidBody2D = load("res://mob.tscn").instantiate()
	check(player.collision_layer == 1, "player collision_layer is still 1 (got %d)" % player.collision_layer)
	check(mob_probe.collision_mask == 0, "mob collision_mask is still 0 (got %d)" % mob_probe.collision_mask)
	check(probe.collision_layer != 1 and (probe.collision_layer & player.collision_mask) != 0,
		"pickup is on its own layer and inside the player's mask (pickup layer %d, player mask %d)" % [probe.collision_layer, player.collision_mask])
	check((mob_probe.collision_layer & player.collision_mask) != 0, "player's mask still includes the mob layer")
	probe.free()
	mob_probe.free()

	# 2. Collect with real input and time the shield in physics ticks.
	await click(game.get_node("HUD/StartButton"))
	var pickup: Area2D = load("res://pickup.tscn").instantiate()
	pickup.position = player.position + Vector2(100, 0)
	game.add_child(pickup)
	await physics_frame
	await key(KEY_D, true)
	var collected_tick := -1
	for i in 60:
		await physics_frame
		if player.shielded:
			collected_tick = Engine.get_physics_frames()
			break
	await key(KEY_D, false)
	check(collected_tick > 0, "real D input collected the pickup")

	var mob: RigidBody2D = load("res://mob.tscn").instantiate()
	mob.position = player.position
	mob.freeze = true
	game.add_child(mob)
	var hit_tick := -1
	for i in 400:
		await physics_frame
		clear_natural_mobs(mob)
		if not player.visible:
			hit_tick = Engine.get_physics_frames()
			break
	var ticks := hit_tick - collected_tick
	print("SHIELD_TICKS collected=", collected_tick, " hit=", hit_tick, " elapsed_ticks=", ticks,
		" physics_ticks_per_second=", Engine.physics_ticks_per_second)
	check(hit_tick > 0, "the overlapping fixture mob hits the player after the shield")
	check(ticks >= 177 and ticks <= 190, "hit lands 3.0 s after collection, within 10 ticks (elapsed %d ticks)" % ticks)

	# 3. A pickup spawned by the real PickupTimer lands inside the 480x720 view.
	await create_timer(2.5).timeout
	await click(game.get_node("HUD/StartButton"))
	var natural: Area2D = null
	for i in 60 * 9:
		await physics_frame
		clear_natural_mobs(null)
		var found := get_nodes_in_group("pickups")
		if not found.is_empty():
			natural = found[0]
			break
	check(natural != null, "PickupTimer spawned a pickup during normal play")
	if natural != null:
		print("NATURAL_PICKUP position=", natural.position)
		check(Rect2(0, 0, 480, 720).has_point(natural.position), "natural pickup is inside the viewport")

	game.get_node("Music").stop()
	game.get_node("DeathSound").stop()
	# --fixed-fps advances game timers faster than wall time; the audio thread
	# drains stopped playbacks in wall time, so wait in wall time before freeing.
	OS.delay_msec(300)
	await process_frame
	game.queue_free()
	await process_frame
	await process_frame
	print("RESULT failures=", failures, "; reviewer's own headless check, not footage")
	# Quit after this coroutine returns, so its local references are released first.
	quit.call_deferred(1 if failures else 0)

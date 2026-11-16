extends SceneTree
var game: Node3D
func _initialize() -> void: call_deferred("run")
func tick() -> void:
	await physics_frame
	await process_frame
func run() -> void:
	game = load("res://signal-garden/main.tscn").instantiate()
	game.audio_enabled = false
	root.add_child(game)
	await tick()
	Input.action_press("garden_right")
	while game.player.position.x < -2.1: await tick()
	Input.action_release("garden_right")
	await tick()
	var start := Engine.get_physics_frames()
	Input.action_press("garden_action")
	var max_error := 0.0
	var count := 0
	while not game.gate_open and count < 200:
		await tick()
		var seconds := float(Engine.get_physics_frames()-start)/60.0
		max_error = maxf(max_error, absf(float(game.pad_material.get_shader_parameter("activation")) - minf(1, seconds / 0.6)))
		count += 1
	Input.action_release("garden_action")
	var duration := float(Engine.get_physics_frames()-start)/60.0
	var ok: bool = game.gate_open and absf(duration - 0.6) <= 0.05 and max_error < 0.09
	print(JSON.stringify({"id":"independent-physics-clock","pass":ok,"render_frames":count,"duration_seconds":duration,"uniform_max_error":max_error,"physics_hz":60}))
	game.queue_free()
	await process_frame
	quit(0 if ok else 1)

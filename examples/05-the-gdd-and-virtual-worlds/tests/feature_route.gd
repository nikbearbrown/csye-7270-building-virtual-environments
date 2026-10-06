extends SceneTree

# Observes targets to choose input; never writes gameplay transforms/state.
func _initialize() -> void:
	call_deferred("run_route")

func run_route() -> void:
	var args = OS.get_cmdline_user_args()
	assert(args.size() == 1 and not FileAccess.file_exists(args[0]))
	seed(7375)
	var game = load("res://game.tscn").instantiate()
	root.add_child(game)
	current_scene = game
	var player = game.get_node("Player")
	var camera = player.get_node("Target/Camera3D")
	var rows: Array = []
	var jump_age := 100
	var max_coins := 0
	var enemy_hit := false
	var actions = ["move_forward","move_back","move_left","move_right","jump","shoot"]
	for frame in range(1800):
		await physics_frame
		var desired: Dictionary = {}
		var nearest: Node3D = null
		var distance := INF
		for coin in game.get_node("Coins").get_children():
			if coin.taken or coin.global_position.y > 0:
				continue
			var d: float = player.global_position.distance_to(coin.global_position)
			if d < distance:
				distance = d
				nearest = coin
		jump_age += 1
		if frame > 90 and nearest != null:
			var delta: Vector3 = nearest.global_position - player.global_position
			delta.y = 0
			var right: Vector3 = camera.global_basis.x
			var back: Vector3 = camera.global_basis.z
			right.y = 0
			back.y = 0
			var move := Vector2(delta.normalized().dot(right.normalized()),delta.normalized().dot(back.normalized()))
			desired["move_right" if move.x > 0 else "move_left"] = absf(move.x)
			desired["move_back" if move.y > 0 else "move_forward"] = absf(move.y)
			if player.is_on_floor() and jump_age > 90 and distance > 1:
				jump_age = 0
			if jump_age < 60:
				desired["jump"] = 1.0
			if frame % 30 == 0:
				desired["shoot"] = 1.0
		for action in actions:
			if desired.has(action):
				Input.action_press(action,desired[action])
			elif Input.is_action_pressed(action):
				Input.action_release(action)
		await process_frame
		var pressed: Dictionary = {}
		for action in actions:
			if Input.is_action_pressed(action):
				pressed[action] = Input.get_action_strength(action)
		var enemies: Array = []
		for enemy in game.get_node("Enemies").get_children():
			enemy_hit = enemy_hit or enemy.dying
			enemies.append({"name":enemy.name,"dying":enemy.dying})
		max_coins = maxi(max_coins,player.coins)
		var p: Vector3 = player.global_position
		rows.append({"frame":frame,"physics_tick":Engine.get_physics_frames(),
			"actions":pressed,"position":[p.x,p.y,p.z],"coins":player.coins,
			"target":str(nearest.name) if is_instance_valid(nearest) else "none",
			"enemies":enemies})
	for action in actions:
		Input.action_release(action)
	var report = {"method":"ordinary input, state-observing target selection; no gameplay state writes",
		"human_playtest":false,"max_coins":max_coins,"enemy_hit":enemy_hit,"frames":rows}
	var file = FileAccess.open(args[0],FileAccess.WRITE)
	file.store_string(JSON.stringify(report,"\t"))
	file.close()
	print("coins=",max_coins," enemy_hit=",enemy_hit)
	current_scene = null
	game.queue_free()
	await process_frame
	quit(0 if max_coins > 0 else 1)

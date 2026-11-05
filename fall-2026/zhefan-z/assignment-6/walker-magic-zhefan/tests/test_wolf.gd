extends SceneTree
## Headless checks for S4: wolf patrol, growl telegraph, lunge, player hurt/knockback/blink, HP 0,
## fireball hits, white flash, down image, removal, and the one-defeat guard.
##   Godot_v4.7.2-stable_win64_console.exe --path . --headless -s res://tests/test_wolf.gd
## Prints one JSON line per check and "WALKER TESTS: N checks / F failures"; exit code 1 on any failure.

const GROUND_TOP := 327.0

var main: Node
var player: Player
var wolf: Wolf
var results: Array[Dictionary] = []
var failures := 0
var hurts := 0
var fails := 0
var fail_reason := ""
var defeats := 0


func _initialize() -> void:
	call_deferred("run")


func check(id: String, passed: bool, observed: Dictionary) -> void:
	results.append({"id": id, "status": "PASS" if passed else "FAIL", "observed": observed})
	if not passed:
		failures += 1
	print(JSON.stringify(results.back()))


func steps(n: int) -> void:
	for i in n:
		await physics_frame


func fresh(player_x: float, wolf_x := 860.0) -> void:
	if is_instance_valid(main):
		main.queue_free()
		await process_frame
	main = load("res://game/main.tscn").instantiate()
	main.test_mode = true
	root.add_child(main)
	player = main.player
	wolf = main.get_node("Level/Wolf")
	player.use_scripted = true
	player.global_position = Vector2(player_x, GROUND_TOP)
	wolf.global_position = Vector2(wolf_x, GROUND_TOP)
	hurts = 0
	fails = 0
	fail_reason = ""
	defeats = 0
	player.hurt.connect(func(_hp: int) -> void: hurts += 1)
	player.failed.connect(func(r: String) -> void:
		fails += 1
		fail_reason = r)
	wolf.defeated.connect(func() -> void: defeats += 1)
	await steps(2)


func flash_value() -> float:
	return float((wolf.sprite.material as ShaderMaterial).get_shader_parameter("flash"))


func shoot_wolf() -> void:
	# A fireball placed just in front of the wolf, flying into it.
	var fb: Fireball = Player.FIREBALL.instantiate()
	fb.direction = Vector2.RIGHT
	fb.position = wolf.global_position + Vector2(-40, -14)
	main.add_child(fb)


func run() -> void:
	Controls.ensure()

	# Patrol: player far away; the wolf walks its limits with the run image and turns at each end.
	await fresh(100)
	var xs: Array[float] = []
	var facings := {}
	for i in 600:
		await physics_frame
		xs.append(wolf.global_position.x)
		facings[wolf.facing] = true
	check("patrol-between-limits-run-image", xs.min() >= 755.0 and xs.max() <= 965.0 and facings.size() == 2
		and wolf.state == Wolf.State.PATROL and wolf.sprite.texture == Wolf.TEX_RUN,
		{"x_min": snappedf(xs.min(), 0.1), "x_max": snappedf(xs.max(), 0.1), "turned": facings.keys()})

	# Telegraph: the player in sight -> growl (lunge image, standing still) for 0.5 s, then the lunge.
	await fresh(780, 860)
	var growl_frames := 0
	var moved_in_growl := 0.0
	var before_x := wolf.global_position.x
	var frames := 0
	while wolf.state != Wolf.State.LUNGE and frames < 120:
		await physics_frame
		frames += 1
		if wolf.state == Wolf.State.GROWL:
			growl_frames += 1
			moved_in_growl = maxf(moved_in_growl, absf(wolf.global_position.x - before_x))
		else:
			before_x = wolf.global_position.x
	check("growl-telegraph-before-lunge", growl_frames >= 29 and growl_frames <= 31 and moved_in_growl < 0.5
		and wolf.sprite.texture == Wolf.TEX_LUNGE and wolf.facing == -1,
		{"growl_frames": growl_frames, "growl_s": snappedf(growl_frames / 60.0, 0.01), "moved_px": moved_in_growl, "facing": wolf.facing})

	# The lunge hits once: 5 -> 4 HP, knockback away from the wolf, hurt image, then blinking.
	var px := player.global_position.x
	frames = 0
	while hurts == 0 and frames < 60:
		await physics_frame
		frames += 1
	var hurt_img := player.sprite.texture == Player.TEXTURES[Player.State.HURT]
	var kb := player.velocity
	await steps(6)
	var blink_seen := false
	for i in 50:
		await physics_frame
		blink_seen = blink_seen or not player.sprite.visible
	check("lunge-hits-once-with-knockback", hurts == 1 and player.hp == 4 and hurt_img and kb.x < 0.0 and kb.y < 0.0,
		{"hurts": hurts, "hp": player.hp, "hurt_image": hurt_img, "knockback": kb, "player_x_before": px})
	check("blinks-while-invulnerable", blink_seen, {"blink_seen": blink_seen})

	# In isolation (wolf stopped, so it cannot lunge again): visible and hittable again after 1 s.
	await fresh(200)
	wolf.set_physics_process(false)
	player.take_damage(1, 260)
	await steps(66)
	check("visible-and-hittable-after-1s", player.sprite.visible and player.invulnerable == 0.0,
		{"visible": player.sprite.visible, "invulnerable_left": player.invulnerable})

	# Two hits inside the invulnerability window count once.
	await fresh(200)
	player.take_damage(1, 260)
	player.take_damage(1, 260)
	await steps(10)
	player.take_damage(1, 260)
	check("hits-inside-invulnerability-count-once", hurts == 1 and player.hp == 4, {"hurts": hurts, "hp": player.hp})

	# HP 0: five landed hits -> "Out of HP" with the kneeling image, failed once.
	await fresh(200)
	for i in 5:
		player.take_damage(1, 260)
		player.invulnerable = 0.0
	player.take_damage(1, 260)
	check("hp-zero-fails-with-kneeling-image", fails == 1 and fail_reason == "Out of HP" and player.hp == 0
		and player.sprite.texture == Player.TEXTURES[Player.State.FAIL] and player.sprite.visible,
		{"fails": fails, "reason": fail_reason, "hp": player.hp, "hurts": hurts})

	# Fireballs: first hit flashes and leaves 1 HP; second hit -> down image, defeated once, removed.
	await fresh(100)
	wolf.set_physics_process(false)
	shoot_wolf()
	var flashed := false
	for i in 20:
		await physics_frame
		flashed = flashed or flash_value() > 0.5
	check("first-fireball-flashes-wolf-2-to-1", wolf.hp == 1 and flashed and not wolf.dead and defeats == 0,
		{"hp": wolf.hp, "flash_seen": flashed})
	await create_timer(0.2).timeout
	shoot_wolf()
	for i in 20:
		await physics_frame
		if wolf.dead:
			break
	check("second-fireball-defeats-wolf-down-image", wolf.dead and defeats == 1 and wolf.sprite.texture == Wolf.TEX_DOWN,
		{"dead": wolf.dead, "defeats": defeats})
	await physics_frame
	check("dead-wolf-leaves-enemy-layer", wolf.collision_layer == 0, {"collision_layer": wolf.collision_layer})
	await create_timer(0.8).timeout
	check("wolf-disappears-after-down-image", not is_instance_valid(wolf), {"still_in_tree": is_instance_valid(wolf)})

	# Two fireballs into a 1 HP wolf in the same frame: defeated once.
	await fresh(100)
	wolf.set_physics_process(false)
	wolf.hp = 1
	shoot_wolf()
	shoot_wolf()
	for i in 20:
		await physics_frame
	check("two-fireballs-same-frame-defeat-once", defeats == 1 and wolf.dead, {"defeats": defeats})

	# A dead or failing target is not attacked.
	await fresh(780, 860)
	player.fail("test")
	await steps(90)
	check("no-lunge-at-failed-player", hurts == 0 and wolf.state == Wolf.State.PATROL, {"hurts": hurts, "wolf_state": Wolf.State.keys()[wolf.state]})

	print("WALKER TESTS: %d checks / %d failures" % [results.size(), failures])
	quit(1 if failures else 0)

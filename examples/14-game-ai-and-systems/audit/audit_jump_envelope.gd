extends SceneTree
## Chapter-author audit of Lab B (written by hand, not by the agent).
## The agent's test_jump_envelope.gd measured on the original world.tscn
## level, not on a flat floor built from the Ground TileSet as the prompt asked,
## and explained its 128 px range as "not fully accelerated". This audit clears
## both layers, builds a flat 120-tile floor, and measures again, recording the
## takeoff speed so the explanation can be checked.

const TILE := 16.0
const ROW := 30


func _initialize() -> void:
	call_deferred("run")


func key(code: Key, pressed: bool) -> void:
	var e := InputEventKey.new()
	e.physical_keycode = code
	e.pressed = pressed
	Input.parse_input_event(e)


func run() -> void:
	var world: Node = load("res://world.tscn").instantiate()
	root.add_child(world)
	var ground: TileMapLayer = world.get_node("Ground")
	world.get_node("Secret").clear()
	world.get_node("SecretDetector").queue_free()
	ground.clear()
	for c in range(-5, 120):
		ground.set_cell(Vector2i(c, ROW), 0, Vector2i(0, 0))
	var player: CharacterBody2D = world.get_node("Player")
	player.position = Vector2(2.5 * TILE, ROW * TILE - 20)
	player.velocity = Vector2.ZERO
	for i in 60:
		await physics_frame
	print("on_floor_before_still_jump=", player.is_on_floor())
	var floor_y := player.position.y
	key(KEY_W, true)
	await physics_frame
	key(KEY_W, false)
	var peak := floor_y
	var frames := 0
	while frames < 240:
		await physics_frame
		frames += 1
		peak = minf(peak, player.position.y)
		if frames > 5 and player.is_on_floor():
			break
	print("still_jump rise_px=", snappedf(floor_y - peak, 0.1), " rise_tiles=", snappedf((floor_y - peak) / TILE, 0.01), " air_frames=", frames)
	for i in 30:
		await physics_frame
	# running jump: hold right for 0.5 s (60 physics frames at 120 Hz)
	key(KEY_D, true)
	for i in 60:
		await physics_frame
	var takeoff_x := player.position.x
	var takeoff_vx := player.velocity.x
	key(KEY_W, true)
	await physics_frame
	key(KEY_W, false)
	frames = 0
	while frames < 240:
		await physics_frame
		frames += 1
		if frames > 5 and player.is_on_floor():
			break
	key(KEY_D, false)
	var dx := player.position.x - takeoff_x
	print("running_jump takeoff_vx=", snappedf(takeoff_vx, 0.1), " range_px=", snappedf(dx, 0.1), " range_tiles=", snappedf(dx / TILE, 0.01), " air_frames=", frames, " landed_same_height=", is_equal_approx(snappedf(player.position.y, 0.5), snappedf(floor_y, 0.5)))
	quit(0)

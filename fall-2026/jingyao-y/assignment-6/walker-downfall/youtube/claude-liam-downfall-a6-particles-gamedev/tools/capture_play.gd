extends SceneTree
## FILM CAPTURE HELPER (A6 film only; not part of the game or its tests).
## Scripted-input fixture, not human play: the real game (game/main.tscn), the
## real loop and real left-mouse events, the same input path and fixture
## dummies as tests/test_hit_spark_state.gd. City floor (darkest ground),
## seed 2026 with every RNG stream seeded. Amiya (guard) holds the left
## button on a still dummy enemy (rapid cuts -> overlapping HitSparks), then
## lands one blow on a 1-HP dummy (the burst outlives the freed enemy).
## It never calls _hit_spark, CombatVfx.spawn or attack(); it only logs every
## HitSpark the game adds. Run windowed with Movie Maker (tools/run_captures.sh).

const SCENE := "res://effects/hit_spark.tscn"

var rig: Node
var game: GameManager
var frame := 0

func _initialize() -> void:
	node_added.connect(_on_added)
	call_deferred("run")

func _on_added(node: Node) -> void:
	if node.scene_file_path == SCENE:
		print("FILM_HITSPARK frame %d engine_frame %d at %s parent %s" % [frame, Engine.get_process_frames(), (node as Node3D).global_position, node.get_parent().name])

func step(n: int = 1) -> void:
	for i in range(n):
		await process_frame
		frame += 1

func find_game(node: Node) -> GameManager:
	if node is GameManager: return node
	for child in node.get_children():
		var found := find_game(child)
		if found != null: return found
	return null

func send(event: InputEvent) -> void:
	Input.parse_input_event(event)

func hover(point: Vector3) -> Vector2:
	var screen := game.camera.unproject_position(point) * root.get_visible_rect().size / game.get_viewport().get_visible_rect().size
	var motion := InputEventMouseMotion.new()
	motion.position = screen
	motion.global_position = screen
	motion.button_mask = MOUSE_BUTTON_MASK_LEFT if Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT) else 0
	send(motion)
	return screen

func mouse(point: Vector3, pressed: bool) -> void:
	var screen := hover(point)
	var event := InputEventMouseButton.new()
	event.button_index = MOUSE_BUTTON_LEFT
	event.position = screen
	event.global_position = screen
	event.pressed = pressed
	event.button_mask = MOUSE_BUTTON_MASK_LEFT if pressed else 0
	send(event)
	await step(1)

func hold_on(enemy: Enemy, frames: int) -> void:
	var point := enemy.global_position
	await mouse(point, true)
	for i in range(frames):
		if is_instance_valid(enemy): point = enemy.global_position
		hover(point)
		await step()
	await mouse(point, false)

func dummy(offset: Vector3, life: float) -> Enemy:
	var p := game.player
	var e := game._spawn_enemy(p.global_position + offset, false, false)
	e.global_position = p.global_position + offset
	e.max_health = life
	e.health = life
	e.defense = 0
	e.res = 0
	e.set_physics_process(false)
	return e

func run() -> void:
	rig = load("res://game/main.tscn").instantiate()
	rig.persist_sessions = false
	root.add_child(rig)
	await step(2)
	game = find_game(rig)
	game.fixed_map_seed = 2026
	game.seed_rng(2026)
	await game.start_contract("city")
	game._clear_field()
	var p := game.player
	p.set_operator(Operators.AMIYA_GUARD)
	p.clear_move_target()
	print("FILM_LOADED frame %d region %s player %s" % [frame, game.region_id, p.global_position])
	await step(20)
	var target := dummy(Vector3(-2, 0, 0), 1000000)
	await step(3)
	print("FILM_HOLD start frame %d" % frame)
	await hold_on(target, 120)
	print("FILM_HOLD end frame %d" % frame)
	await step(25)
	target.queue_free()
	var victim := dummy(Vector3(-2, 0, 0.6), 1.0)
	await step(3)
	print("FILM_KILL start frame %d" % frame)
	await hold_on(victim, 20)
	print("FILM_KILL end frame %d victim valid %s" % [frame, is_instance_valid(victim)])
	await step(200)

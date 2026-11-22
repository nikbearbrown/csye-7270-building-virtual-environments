extends Node
## Step 7 strip preview (fixture, agent, 2026-11-22), CHANGE-BRIEF.md "The
## frame strip — wave_release". The real game: res://game/main.tscn, the
## seed-1729 Chernobog mine floor (fixed_map_seed and game.seed_rng, the A6
## lesson), the field cleared, the camera at the game's default size and
## pitch (no zoom), Lappland with a full sword charge and one still enemy
## stand-in in reach to her west (screen left, the rig's own facing).
##
## Movie Maker records from the first frame, and loading the floor takes a
## variable number of frames, so the release cannot be pinned to capture frame
## 10 as the brief first said (brief r6). Instead the release is triggered 10
## capture frames after the floor is ready, by a real left click on the enemy
## (Input.parse_input_event), and every capture frame is logged to
## logs/wave_release_preview.log: capture frame, wave_state, wave_frame,
## waves out, charge, hitstop, sprite/billboard visibility. Read the trigger
## frame and each phase boundary from that log.
##
## The user runs the capture (it needs a window):
##   godot --path . res://previews/wave_release_preview.tscn \
##     --write-movie "<abs>/captures/wave_release/r0/frame.png" --fixed-fps 30 --quit-after 240

const ENEMY_OFFSET := Vector3(-2.0, 0, 0)
const TRIGGER_AFTER_READY := 10

var game: GameManager
var frame := 0
var ready_frame := -1
var trigger_frame := -1
var log_lines: PackedStringArray = []
var enemy: Enemy
## First capture frame of each state after the click (STARTUP, ACTIVE, RECOVERY, READY).
var firsts := {}
var last_state := -1

func _ready() -> void:
	var main: Node = load("res://game/main.tscn").instantiate()
	main.persist_sessions = false
	add_child(main)
	for i in range(10): await get_tree().process_frame
	game = _find_game(main)
	game.fixed_map_seed = 1729
	game.seed_rng(1729)
	await game.start_contract("mine")
	game._clear_field()
	for i in range(3): await get_tree().process_frame
	var p := game.player
	p.set_operator("lappland")
	var at := p.global_position + ENEMY_OFFSET
	enemy = game._spawn_enemy(at, false, false)
	enemy.global_position = at
	enemy.max_health = 100000000
	enemy.health = 100000000
	enemy.set_physics_process(false)
	p.sword_charge = p.wave_hits_needed()
	p._attack_cooldown = 0.0
	ready_frame = frame

func _process(_delta: float) -> void:
	if ready_frame >= 0 and is_instance_valid(game) and is_instance_valid(game.player):
		var p := game.player
		if trigger_frame < 0 and frame == ready_frame + TRIGGER_AFTER_READY:
			trigger_frame = frame
			_click(enemy.global_position, true)
		elif trigger_frame >= 0 and frame == trigger_frame + 1:
			_click(enemy.global_position, false)
		if trigger_frame >= 0 and p.wave_state != last_state:
			var key: String = Player.WaveState.keys()[p.wave_state]
			if not firsts.has(key) and (key != "READY" or firsts.has("STARTUP")): firsts[key] = frame
			last_state = p.wave_state
		var waves := 0
		for node in game.get_children():
			if node is SwordWave: waves += 1
		if trigger_frame >= 0 and frame <= trigger_frame + 3:
			log_lines.append("  debug: pressed %s ptr %s has_ptr %s under %s cooldown %.3f sim %s" % [Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT), game._pointer_position, game._has_pointer_position, game.pointer.enemy_under(), p._attack_cooldown, game.simulation_active()])
		log_lines.append("capture %d | design %s | state %s | wave_frame %d | waves %d | charge %d | hitstop %.3f | sprite %s | billboard %s" % [
			frame, str(frame - trigger_frame) if trigger_frame >= 0 else "-",
			Player.WaveState.keys()[p.wave_state], p.wave_frame, waves, p.sword_charge,
			p.hitstop_remaining, p._sprite.visible, p._wave_billboard.visible])
	frame += 1

func _click(point: Vector3, pressed: bool) -> void:
	var screen := game.camera.unproject_position(point) * get_tree().root.get_visible_rect().size / game.get_viewport().get_visible_rect().size
	# Input.parse_input_event feeds the polled button state the game reads
	# (Input.is_mouse_button_pressed); the same events are pushed into the root
	# window in its own coordinates so the pointer position reaches
	# GameManager._input through SubViewportContainer -> SubViewport (the
	# window's own dispatch put the pointer off the enemy: smoke run, 2026-11-22).
	var motion := InputEventMouseMotion.new()
	motion.position = screen
	motion.global_position = screen
	Input.parse_input_event(motion)
	get_tree().root.push_input(motion, true)
	var event := InputEventMouseButton.new()
	event.button_index = MOUSE_BUTTON_LEFT
	event.position = screen
	event.global_position = screen
	event.pressed = pressed
	event.button_mask = MOUSE_BUTTON_MASK_LEFT if pressed else 0
	Input.parse_input_event(event)
	get_tree().root.push_input(event, true)

func _exit_tree() -> void:
	var header := "# wave_release_preview: ready at capture frame %d, click pressed at capture frame %d; 30 fps capture = 1 design frame per capture frame, 60 Hz physics
# first capture frame of each state: %s (STARTUP includes the click's hitstop frames; ACTIVE = the wave leaves)" % [ready_frame, trigger_frame, str(firsts)]
	var file := FileAccess.open(ProjectSettings.globalize_path("res://logs/wave_release_preview.log"), FileAccess.WRITE)
	if file != null:
		file.store_string(header + "\n" + "\n".join(log_lines) + "\n")
		file.close()

func _find_game(node: Node) -> GameManager:
	if node is GameManager: return node
	for child in node.get_children():
		var found := _find_game(child)
		if found != null: return found
	return null

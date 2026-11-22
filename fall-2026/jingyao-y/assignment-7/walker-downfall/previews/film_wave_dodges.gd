extends Node
## FILM CAPTURE FIXTURE (A7 film only; not part of the game or its tests).
## Scripted-input capture, not human play: the real game (res://game/main.tscn),
## the real loop, a real left click on the enemy (Input.parse_input_event plus
## the same events pushed into the root window, as previews/wave_release_preview.gd)
## and a real "dash" action event for each dodge. Seed-1729 Chernobog mine
## floor, field cleared, Lappland, one still very-high-health stand-in enemy.
## Four takes of the release: T1 no dodge; T2 dodge in STARTUP; T3 dodge on the
## first ACTIVE frame; T4 dodge in RECOVERY. The script only reads the player's
## state to time each input. After each take a real ground click walks her
## back to the start (and drops her target lock); before the next take the
## fixture refills the charge to 3 and resets cooldowns and stamina: those
## are fixture writes, labelled in the film. No teleport.
## Every capture frame is printed: "FILM frame N take T state S wave_frame F waves W charge C".
##
## Run: godot --path . res://previews/film_wave_dodges.tscn --write-movie <abs>/frame.png --fixed-fps 30 --quit-after 600

const ENEMY_OFFSET := Vector3(-2.0, 0, 0)
## take -> [state to wait for, frames after entering it, dodge?]
const TAKES := [
	["", 0, false],
	["STARTUP", 3, true],
	["ACTIVE", 0, true],
	["RECOVERY", 3, true],
]
const GAP := 45

var game: GameManager
var enemy: Enemy
var origin := Vector3.ZERO
var frame := 0
var started := false
var take := -1
var phase := "wait"   # wait -> click -> watch -> rest
var phase_frame := 0
var entered := {}
var dodged := false

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
	origin = p.global_position
	var at := origin + ENEMY_OFFSET
	enemy = game._spawn_enemy(at, false, false)
	enemy.global_position = at
	enemy.max_health = 100000000
	enemy.health = 100000000
	enemy.set_physics_process(false)
	started = true
	print("FILM ready at frame %d" % frame)

func _process(_delta: float) -> void:
	if started:
		_drive()
		var p := game.player
		var waves := 0
		for node in game.get_children():
			if node is SwordWave: waves += 1
		print("FILM frame %d take %d phase %s state %s wave_frame %d waves %d charge %d sprite %s billboard %s" % [
			frame, take + 1, phase, Player.WaveState.keys()[p.wave_state], p.wave_frame, waves, p.sword_charge,
			p._sprite.visible, p._wave_billboard.visible])
	frame += 1

func _drive() -> void:
	var p := game.player
	phase_frame += 1
	match phase:
		"wait":
			if phase_frame >= 10:
				take += 1
				if take >= TAKES.size():
					phase = "done"
					return
				p.sword_charge = p.wave_hits_needed()
				p._attack_cooldown = 0.0
				p._dash_cooldown = 0.0
				p.stamina = 100.0
				entered = {}
				dodged = false
				phase = "click"
				phase_frame = 0
				print("FILM take %d starts at frame %d (fixture reset: charge 3, cooldowns, stamina; she walked back by a ground click)" % [take + 1, frame])
		"click":
			if phase_frame == 1: _click(enemy.global_position, true)
			elif phase_frame == 2:
				_click(enemy.global_position, false)
				phase = "watch"
				phase_frame = 0
		"watch":
			var s: String = Player.WaveState.keys()[p.wave_state]
			if not entered.has(s): entered[s] = phase_frame
			var spec: Array = TAKES[take]
			if spec[2] and not dodged and entered.has(spec[0]) and phase_frame - int(entered[spec[0]]) == int(spec[1]):
				_dash(true)
				dodged = true
				print("FILM take %d dodge pressed at frame %d in %s (wave_frame %d)" % [take + 1, frame, s, p.wave_frame])
			elif dodged and phase_frame - int(entered[spec[0]]) == int(spec[1]) + 1:
				_dash(false)
			if phase_frame > 30 and p.wave_state == Player.WaveState.READY:
				phase = "rest"
				phase_frame = 0
		"rest":
			# A real ground click at the start point: she walks back, and the
			# click clears her lock on the enemy (no auto-attack between takes).
			if phase_frame == 1: _click(origin, true)
			elif phase_frame == 2: _click(origin, false)
			if phase_frame >= GAP and not p._has_move_target:
				phase = "wait"
				phase_frame = 0

func _click(point: Vector3, pressed: bool) -> void:
	var screen := game.camera.unproject_position(point) * get_tree().root.get_visible_rect().size / game.get_viewport().get_visible_rect().size
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

func _dash(pressed: bool) -> void:
	var event := InputEventAction.new()
	event.action = &"dash"
	event.pressed = pressed
	Input.parse_input_event(event)

func _find_game(node: Node) -> GameManager:
	if node is GameManager: return node
	for child in node.get_children():
		var found := _find_game(child)
		if found != null: return found
	return null

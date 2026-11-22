extends Node
## Playable fixture (agent, 2026-11-22): try the wired wave_release in the real
## game. Seed-1729 mine floor, field cleared, Lappland, two still dummies with
## huge health, one left and one right of her (both facings). Click a dummy to
## swing; every 4th swing is a release (3 hits fill the charge). Space dodges:
## try it in the wind-up, on the sweep and in the settle. Close when done.
## Run windowed: godot --path . res://previews/wave_release_play.tscn

var game: GameManager

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
	var origin := p.global_position
	for side in [-1.0, 1.0]:
		var at := origin + Vector3(2.2 * side, 0, 0)
		var e := game._spawn_enemy(at, false, false)
		e.global_position = at
		e.max_health = 100000000
		e.health = 100000000
		e.set_physics_process(false)
	game.zoom_camera(-2)

func _find_game(node: Node) -> GameManager:
	if node is GameManager: return node
	for child in node.get_children():
		var found := _find_game(child)
		if found != null: return found
	return null

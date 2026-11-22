extends Node
## Preview (fixture, agent, 2026-11-22): the wired npc_idle clip in the real
## game. First the base store (可露希尔, 12 s), then the seed-1729 mine floor
## with the player placed beside the 罗德岛小队 set piece (three figures that
## should breathe out of step). Close the window when done.
## Run windowed: godot --path . res://previews/npc_idle_in_game.tscn

var game: GameManager

func _ready() -> void:
	var main: Node = load("res://game/main.tscn").instantiate()
	main.persist_sessions = false
	add_child(main)
	for i in range(10): await get_tree().process_frame
	game = _find_game(main)
	var store := game.base_map.get_node("store") as Node3D
	var closure := store.get_node("Closure") as Node3D
	var p := game.player
	var spot: Vector3 = store.to_global(closure.position + Vector3(BaseMap.EAST * 0.8, 0, 2.2))
	p.teleport(Vector3(spot.x, p.global_position.y, spot.z))
	game.zoom_camera(-3)
	await get_tree().create_timer(12.0).timeout
	game.fixed_map_seed = 1729
	game.seed_rng(1729)
	await game.start_contract("mine")
	for i in range(5): await get_tree().process_frame
	var piece := game.world_map.encounter_node as Node3D
	if piece != null:
		var at := piece.global_position + Vector3(0, 0, 2.5)
		game.player.teleport(Vector3(at.x, game.ground_y(at), at.z))
	game.zoom_camera(-3)

func _find_game(node: Node) -> GameManager:
	if node is GameManager: return node
	for child in node.get_children():
		var found := _find_game(child)
		if found != null: return found
	return null

extends Node
## Preview (fixture, agent, 2026-11-22): the new npc_idle clip beside today's
## 可露希尔 at the base store, before any wiring. Left: the old AnimatedSprite3D
## from FieldArt.npc_idle("closure"). Right: res://animations/npc_idle.tscn,
## placed the same way (world/base_map.gd:762-770), one cell out of step so the
## two are easy to tell apart. Nothing in the game is changed.
## Run windowed: godot --path . res://previews/npc_idle_side_by_side.tscn

const NPC_IDLE := preload("res://animations/npc_idle.tscn")
var game: GameManager

func _ready() -> void:
	var main: Node = load("res://game/main.tscn").instantiate()
	main.persist_sessions = false
	add_child(main)
	for i in range(10): await get_tree().process_frame
	game = _find_game(main)
	var store := game.base_map.get_node("store")
	var old := store.get_node("Closure") as Node3D
	var fresh := NPC_IDLE.instantiate() as Sprite3D
	fresh.name = "NpcIdlePreview"
	fresh.position = old.position + Vector3(BaseMap.EAST * 1.6, 0, 0)
	fresh.offset.y -= BaseMap.PIVOT_SCREEN_PX
	fresh.double_sided = true
	fresh.add_to_group("upright_sprites")
	store.add_child(fresh)
	(fresh.get_node("AnimationPlayer") as AnimationPlayer).seek(1.0 / 3.0, true)
	var p := game.player
	var spot: Vector3 = (store as Node3D).to_global(old.position + Vector3(BaseMap.EAST * 0.8, 0, 2.2))
	p.teleport(Vector3(spot.x, p.global_position.y, spot.z))
	game.zoom_camera(-3)

func _find_game(node: Node) -> GameManager:
	if node is GameManager: return node
	for child in node.get_children():
		var found := _find_game(child)
		if found != null: return found
	return null

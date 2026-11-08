extends Node
## FIXTURE for the user's in-play checks (A6 "Use It"): the real game on a real
## field floor with the simulation running, so both effects fire from normal
## play. Not gameplay code. Run from the editor (open this scene, F6) or:
##   Godot_v4.7.2-stable_win64.exe --path . res://previews/play_check.tscn [-- --city]
## Default Sami snow (lightest ground, fire pits); `-- --city` for the darkest;
## `-- --lit` lights every pit as the floor finishes loading.
## The pack gets 6 planks and 2 solid fuel so a pit can be fed with E.
## Extra keys (unused by the game and by the editor):
##   Y  pause / unpause the whole tree (get_tree().paused; menus don't do this)
##   H  hide / show every pit's FirePitFlames node
## Everything else is the game's own controls (left mouse, E, Esc, Z/X, wheel…).

@export var map_seed := 2026

var rig: Node
var game: GameManager
var _label: Label

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	rig = load("res://game/main.tscn").instantiate()
	rig.persist_sessions = false
	rig.process_mode = Node.PROCESS_MODE_PAUSABLE
	add_child(rig)
	game = _find_game(rig)
	var layer := CanvasLayer.new()
	layer.layer = 100
	add_child(layer)
	_label = Label.new()
	_label.position = Vector2(12, 40)
	_label.add_theme_font_size_override("font_size", 16)
	layer.add_child(_label)
	_load_level()

func _find_game(node: Node) -> GameManager:
	if node is GameManager: return node
	for child in node.get_children():
		var found := _find_game(child)
		if found != null: return found
	return null

func _load_level() -> void:
	var region := "city" if "--city" in OS.get_cmdline_user_args() else "snow"
	game.fixed_map_seed = map_seed
	game.seed_rng(map_seed)
	await game.start_contract(region)
	for i in range(6): game.inventory.add_stack(MaterialCatalog.create("木板", 1))
	for i in range(2): game.inventory.add_stack(MaterialCatalog.create("固体燃料", 1))
	# `-- --lit`: every pit full in the same frame the floor finishes loading,
	# the nearest the fixture gets to the camp fire that is lit at floor build.
	if "--lit" in OS.get_cmdline_user_args():
		for f in game.fires:
			if is_instance_valid(f): f.feed(FeatureCatalog.FIRE_MAX)
	print("PLAY_CHECK loaded %s, %d pits" % [region, game.fires.size()])

func _unhandled_input(event: InputEvent) -> void:
	if not (event is InputEventKey and event.pressed and not event.echo): return
	match event.keycode:
		KEY_Y:
			get_tree().paused = not get_tree().paused
		KEY_H:
			for f in game.fires:
				if not is_instance_valid(f): continue
				var fx := f.get_node_or_null("FirePitFlames") as Node3D
				if fx != null: fx.visible = not fx.visible
		_: return
	print("PLAY_CHECK paused %s" % get_tree().paused)

func _process(_delta: float) -> void:
	if not is_instance_valid(game): return
	var near := ""
	for f in game.fires:
		if is_instance_valid(f) and is_instance_valid(game.player) and f.global_position.distance_to(game.player.global_position) < 12.0:
			var fx := f.get_node_or_null("FirePitFlames") as Node3D
			near = "  pit: fuel %.0f s, ratio %.2f, %s" % [f.burn_left, (fx.get_child(0) as GPUParticles3D).amount_ratio if fx else 0.0, "hidden" if fx and not fx.visible else "shown"]
	_label.text = "FIXTURE play_check  Y pause tree: %s  H hide pits%s" % ["PAUSED" if get_tree().paused else "running", near]

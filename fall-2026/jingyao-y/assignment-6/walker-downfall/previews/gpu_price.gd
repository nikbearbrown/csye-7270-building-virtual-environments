extends Node
## FIXTURE, not gameplay: the windowed GPU-price rig for A6 (CHANGE-BRIEF.md,
## "Price predictions and budget"). Run it from the editor (open this scene, F6)
## with Debugger → Visual Profiler open, and read GPU time with each effect off
## and on at its heaviest.
##
## Boots the real game, Sami floor (seed 2026, every RNG stream seeded), freezes
## the simulation with the "capture" modal, camera on pit 1 at default size.
## Keys (none is used by the game; F7/F8 are the editor's pause/stop while a
## scene runs from the editor, so they are not used):
##   U   Effect A at its priced peak: a HitSpark every FREE_AFTER/8 s beside the
##       pit, so about 8 are alive at once (152 particles).
##   I   Effect B heaviest: every FirePit on the floor fuelled to 300 s
##       (amount_ratio 1.0); again to put them out.
##   O   vsync on/off (DisplayServer, this window only; no project setting).
## The label shows the state, FPS and the number of HitSparks alive.

const HIT_SPARK := preload("res://effects/hit_spark.tscn")
const PEAK := 8

@export var map_seed := 2026
@export var pit_index := 1

var rig: Node
var game: GameManager
var pit: FirePit
var loaded := false
var a_on := false
var b_on := false
var _spawn_clock := 0.0
var _label: Label

func _ready() -> void:
	process_priority = 1000
	rig = load("res://game/main.tscn").instantiate()
	rig.persist_sessions = false
	add_child(rig)
	game = _find_game(rig)
	var layer := CanvasLayer.new()
	layer.layer = 100
	add_child(layer)
	_label = Label.new()
	_label.position = Vector2(12, 12)
	_label.add_theme_font_size_override("font_size", 18)
	layer.add_child(_label)
	_load_level()

func _find_game(node: Node) -> GameManager:
	if node is GameManager: return node
	for child in node.get_children():
		var found := _find_game(child)
		if found != null: return found
	return null

func _load_level() -> void:
	game.fixed_map_seed = map_seed
	game.seed_rng(map_seed)
	await game.start_contract("snow")
	game.open_modal("capture")
	var valid := game.fires.filter(func(f): return is_instance_valid(f))
	if pit_index < valid.size(): pit = valid[pit_index]
	if pit == null:
		push_error("gpu_price: no FirePit %d on this floor" % pit_index)
		return
	game.player.teleport(game.world_map.nearest_walkable(pit.global_position + Vector3(2.5, 0.0, 0.0)))
	game.camera_size_goal = GameManager.CAMERA_SIZE
	game.camera.size = GameManager.CAMERA_SIZE
	loaded = true
	print("GPU_PRICE loaded: %d pits, pit %s" % [valid.size(), pit.global_position])

func _unhandled_input(event: InputEvent) -> void:
	if not (event is InputEventKey and event.pressed and not event.echo): return
	match event.keycode:
		KEY_U:
			a_on = not a_on
			_spawn_clock = 0.0
		KEY_I:
			b_on = not b_on
			for f in game.fires:
				if not is_instance_valid(f): continue
				if b_on: f.feed(FeatureCatalog.FIRE_MAX)
				else: f.burn(f.burn_left)
		KEY_O:
			var off := DisplayServer.window_get_vsync_mode() == DisplayServer.VSYNC_DISABLED
			DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_ENABLED if off else DisplayServer.VSYNC_DISABLED)
		_: return
	print("GPU_PRICE A %s B %s vsync %s" % [a_on, b_on, DisplayServer.window_get_vsync_mode() != DisplayServer.VSYNC_DISABLED])

func _process(delta: float) -> void:
	if not loaded: return
	game.camera.global_position = pit.global_position + game.camera_offset()
	if game._hud.visible: game._hud.hide()
	if a_on:
		_spawn_clock -= delta
		if _spawn_clock <= 0.0:
			_spawn_clock += 0.55 / PEAK
			var burst := HIT_SPARK.instantiate() as Node3D
			burst.position = game.to_local(pit.global_position + Vector3(-1.5, 0.65, 0.0))
			game.add_child(burst)
	var alive := 0
	for child in game.get_children():
		if child.get_script() == preload("res://effects/hit_spark.gd"): alive += 1
	_label.text = "FIXTURE gpu_price  U A:%s (alive %d)  I B:%s  O vsync:%s  FPS %d" % [
		"ON" if a_on else "off", alive, "ON" if b_on else "off",
		"on" if DisplayServer.window_get_vsync_mode() != DisplayServer.VSYNC_DISABLED else "OFF",
		Engine.get_frames_per_second()]

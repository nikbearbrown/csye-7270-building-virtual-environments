extends Node
## FIXTURE, not gameplay: the frame-strip preview for Effect A (CHANGE-BRIEF.md,
## "Frame strip (Effect A)"). Boots the real game (res://game/main.tscn) headed,
## starts a real city contract with a fixed map seed, freezes the simulation with
## the "capture" modal, spawns one real city enemy as the stand-in, centres the
## camera on it at the game's default size (24) and pitch, and instances
## res://effects/hit_spark.tscn at the stand-in's global_position under the
## GameManager at preview frame `fire_frame` and, with `retrigger` on, again at
## `retrigger_frame` (a second instance: the brief's overlap rule).
## The HitSpark instances made here are the only ones with use_fixed_seed on.
##
## Frame count: `frame` is 0 on this script's first _process and goes up by one
## per processed frame. The level is loaded from _ready (before the first
## frame) and must be ready before `fire_frame`; the log line PREVIEW_LOADED
## says on which frame it was, and PREVIEW_FIRE names the engine frame of each
## burst so the Movie Maker file numbers can be matched.
##
## Capture (windowed, Movie Maker):
##   godot --path . res://previews/hit_spark_preview.tscn
##     --write-movie <abs>/captures/hit_spark/r0/frame.png --fixed-fps 30 --quit-after 60

const HIT_SPARK := preload("res://effects/hit_spark.tscn")

@export var retrigger := true
@export var map_seed := 2026
@export var spark_seed := 7370
@export var fire_frame := 10
@export var retrigger_frame := 16
## Strip frames whose state is printed to the log.
@export var report_frames: PackedInt32Array = PackedInt32Array([10, 12, 15, 16, 20, 30, 50])

var rig: Node
var game: GameManager
var stand_in: Node3D
var loaded := false
var frame := -1
var fired := 0

func _ready() -> void:
	# Run after the GameManager's own _process, so the camera placed here is the one drawn.
	process_priority = 1000
	rig = load("res://game/main.tscn").instantiate()
	rig.persist_sessions = false
	add_child(rig)
	game = _find_game(rig)
	print("PREVIEW_BOOT engine_frame %d in_base %s" % [Engine.get_process_frames(), game.in_base])
	_load_level()

func _find_game(node: Node) -> GameManager:
	if node is GameManager: return node
	for child in node.get_children():
		var found := _find_game(child)
		if found != null: return found
	return null

func _load_level() -> void:
	game.fixed_map_seed = map_seed
	# `-- --snow`: the brief's lightest ground (萨米 snow) instead of the city street.
	var region := "snow" if "--snow" in OS.get_cmdline_user_args() else "city"
	await game.start_contract(region)
	game.open_modal("capture")
	var at: Vector2 = game.world_map.main_path[0] + Vector2(0, 8)
	game.player.teleport(game.world_map.nearest_walkable(Vector3(at.x, 0.7, at.y)))
	stand_in = game._spawn_enemy(game.player.global_position + Vector3(-1.5, 0.0, 0.0), false, false)
	game._hud.hide()
	game.camera_size_goal = GameManager.CAMERA_SIZE
	game.camera.size = GameManager.CAMERA_SIZE
	_place_camera()
	loaded = true
	print("PREVIEW_LOADED preview_frame %d engine_frame %d region %s seed %d player %s stand_in %s (%s) camera_size %.1f pitch %.4f" % [frame, Engine.get_process_frames(), game.region_id, map_seed, game.player.global_position, stand_in.global_position, stand_in.get("enemy_type"), game.camera.size, game.camera_pitch])

func _place_camera() -> void:
	if is_instance_valid(stand_in):
		game.camera.global_position = stand_in.global_position + game.camera_offset()

func _process(_delta: float) -> void:
	frame += 1
	if loaded:
		_place_camera()
		# Something re-shows the HUD after _load_level; keep it out of the fixture.
		if game._hud.visible: game._hud.hide()
	# `-- --loop` (human viewing only, not used for strips): replay the pair every 90 frames.
	var f := frame
	if "--loop" in OS.get_cmdline_user_args() and frame > retrigger_frame:
		f = fire_frame + (frame - fire_frame) % 90
	if f == fire_frame:
		_fire()
	if retrigger and f == retrigger_frame:
		_fire()
	if frame in report_frames:
		var alive := 0
		if is_instance_valid(game):
			for child in game.get_children():
				if child.name.begins_with("HitSpark"): alive += 1
		print("PREVIEW_FRAME %d engine_frame %d frames_drawn %d loaded %s hit_spark_alive %d" % [frame, Engine.get_process_frames(), Engine.get_frames_drawn(), loaded, alive])

func _fire() -> void:
	if not loaded or not is_instance_valid(stand_in):
		print("PREVIEW_ERROR level not loaded by preview frame %d; burst skipped" % frame)
		return
	var spark := HIT_SPARK.instantiate() as Node3D
	for child in spark.get_children():
		if child is GPUParticles3D:
			child.use_fixed_seed = true
			child.seed = spark_seed + fired
	spark.name = "HitSpark%d" % fired
	# GameManager is a Node3D at the origin, so this local position is the global one.
	spark.position = stand_in.global_position
	game.add_child(spark)
	fired += 1
	print("PREVIEW_FIRE %d preview_frame %d engine_frame %d at %s" % [fired, frame, Engine.get_process_frames(), spark.global_position])

extends Node
## FIXTURE, not gameplay: the frame-strip preview for Effect B (CHANGE-BRIEF.md,
## "Frame strip (Effect B)"). Boots the real game (res://game/main.tscn) headed,
## starts a real 萨米 (`snow`) contract with a fixed map seed, freezes the
## simulation with the "capture" modal, picks the floor's first real FirePit,
## puts the player a few units from it, centres the camera on the pit at the
## game's default size (24) and pitch, and instances
## res://effects/fire_pit_flames.tscn at the pit's global_position under the
## GameManager. The FirePitFlames instance made here is the only one with
## use_fixed_seed on.
##
## Gameplay is not wired yet (FirePit still makes its own CPU "Flames"/"Embers"),
## so this fixture plays the condition itself, by the brief's feedback mapping:
##   emitting     = burn_left > 0
##   amount_ratio = 0.3 + 0.7 * clamp(burn_left / 120.0, 0, 1)
## It changes the real pit's burn_left through FirePit.feed()/burn() (so the
## pit's Glow halo follows) and hides the pit's own CPU particle children so
## only the GPU effect is drawn. Frames: 10 feed 120 s (ratio 1.0), 55 burn to
## 24 s (ratio 0.44), 100 burn to 0 (out).
##
## Frame count: `frame` is 0 on this script's first _process and goes up by one
## per processed frame. PREVIEW_LOADED says on which frame the level was ready.
##
## Capture (windowed, Movie Maker):
##   godot --path . res://previews/fire_pit_flames_preview.tscn
##     --write-movie <abs>/captures/fire_pit_flames/r0/frame.png --fixed-fps 30 --quit-after 180

const FLAMES := preload("res://effects/fire_pit_flames.tscn")

@export var map_seed := 2026
@export var particle_seed := 7370
## preview frame -> burn_left the pit is set to on that frame.
## Index into the floor's FirePits (see _load_level).
@export var pit_index := 1
@export var light_frame := 10
@export var light_burn := 120.0
@export var dwindle_frame := 55
@export var dwindle_burn := 24.0
@export var out_frame := 100
## Strip frames whose state is printed to the log.
@export var report_frames: PackedInt32Array = PackedInt32Array([10, 12, 40, 54, 70, 99, 105, 130, 175])

var rig: Node
var game: GameManager
var pit: FirePit
var effect: Node3D
var loaded := false
var frame := -1

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
	# fixed_map_seed alone left the fire count and places varying run to run; fix every RNG stream too.
	game.seed_rng(map_seed)
	await game.start_contract("snow")
	game.open_modal("capture")
	# Which of the floor's pits (`-- --pit=N` overrides `pit_index`). With every RNG stream seeded,
	# seed 2026 gives 3 pits; 1 is in open snow (0 has the player on it, 2 a crowd).
	var index := pit_index
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--pit="): index = int(arg.trim_prefix("--pit="))
	var valid := game.fires.filter(func(f): return is_instance_valid(f))
	if index < valid.size(): pit = valid[index]
	if pit == null:
		print("PREVIEW_ERROR no FirePit on this floor (region %s seed %d)" % [game.region_id, map_seed])
		return
	# The pit's own CPU particles stay off screen; the GPU effect is what is captured.
	for child_name in ["Flames", "Embers"]:
		var cpu := pit.get_node_or_null(NodePath(child_name)) as Node3D
		if cpu != null: cpu.visible = false
	game.player.teleport(game.world_map.nearest_walkable(pit.global_position + Vector3(2.5, 0.0, 0.0)))
	effect = FLAMES.instantiate() as Node3D
	effect.name = "FirePitFlames"
	for child in effect.get_children():
		if child is GPUParticles3D:
			child.use_fixed_seed = true
			child.seed = particle_seed
	game.add_child(effect)
	effect.global_position = pit.global_position
	game._hud.hide()
	game.camera_size_goal = GameManager.CAMERA_SIZE
	game.camera.size = GameManager.CAMERA_SIZE
	_place_camera()
	loaded = true
	print("PREVIEW_LOADED preview_frame %d engine_frame %d region %s floor %d seed %d fires %d pit %s burn_left %.1f player %s camera_size %.1f pitch %.4f" % [frame, Engine.get_process_frames(), game.region_id, game.floor_number, map_seed, game.fires.size(), pit.global_position, pit.burn_left, game.player.global_position, game.camera.size, game.camera_pitch])

func _place_camera() -> void:
	if is_instance_valid(pit):
		game.camera.global_position = pit.global_position + game.camera_offset()

## The brief's feedback mapping, played by the fixture from the pit's real burn_left.
func _apply() -> void:
	var burn_left := pit.burn_left
	var ratio := 0.3 + 0.7 * clampf(burn_left / 120.0, 0.0, 1.0)
	for child in effect.get_children():
		if child is GPUParticles3D:
			child.amount_ratio = ratio
			child.emitting = burn_left > 0.0
	print("PREVIEW_SET preview_frame %d engine_frame %d burn_left %.1f emitting %s amount_ratio %.4f" % [frame, Engine.get_process_frames(), burn_left, burn_left > 0.0, ratio])

func _process(_delta: float) -> void:
	frame += 1
	if loaded:
		_place_camera()
		# Something re-shows the HUD after _load_level; keep it out of the fixture.
		if game._hud.visible: game._hud.hide()
		# `-- --loop` (human viewing only, not used for strips): a 600-frame cycle,
		# lit at 10, dwindling at 250, out at 400 (about 4 s / 2.5 s / 3.3 s at 60 fps).
		var f := frame
		var looping := "--loop" in OS.get_cmdline_user_args()
		if looping:
			f = 10 + (frame - 10) % 600 if frame >= 10 else frame
			if f == dwindle_frame or f == out_frame: f = -1
			elif f == 250: f = dwindle_frame
			elif f == 400: f = out_frame
		if f == light_frame:
			pit.feed(light_burn - pit.burn_left)
			_apply()
		elif f == dwindle_frame:
			pit.burn(pit.burn_left - dwindle_burn)
			_apply()
		elif f == out_frame:
			pit.burn(pit.burn_left)
			_apply()
	elif frame == light_frame:
		print("PREVIEW_ERROR level not loaded by preview frame %d" % frame)
	if frame in report_frames:
		var line := "PREVIEW_FRAME %d engine_frame %d frames_drawn %d loaded %s" % [frame, Engine.get_process_frames(), Engine.get_frames_drawn(), loaded]
		if loaded:
			var flames := effect.get_node("Flames") as GPUParticles3D
			line += " burn_left %.1f flames_emitting %s amount_ratio %.4f amount %d embers_emitting %s" % [pit.burn_left, flames.emitting, flames.amount_ratio, flames.amount, (effect.get_node("Embers") as GPUParticles3D).emitting]
		print(line)

extends SceneTree

## Film captures for the A3 reel, run in an isolated clone of ceada15 with
## window_width_override=3840 / window_height_override=2160.
##
##   godot --path CAP --script res://tests/capture_a3_film.gd -- stills
##       Mine floor, map seed 1729, through the game's own camera:
##       ramp foot and terrace top, the same views capture_terrain.gd uses,
##       then a cliff between terraces found as capture_terrain.gd finds one.
##       The player is placed by teleport (test shortcut), HUD left on.
##       Run under --write-movie too, so the film can take 4K frames by number.
##   godot --path CAP --write-movie orbit.avi --fixed-fps 30 --script res://tests/capture_a3_film.gd -- orbit
##       art/models/asset_preview.tscn: game camera for 2 s, then a perspective
##       camera orbiting all three assets once (including from behind), 16 s.
##   godot --path CAP --write-movie light.avi --fixed-fps 30 --script res://tests/capture_a3_film.gd -- light
##       TEST-REPORT loop 3, re-rendered: the rubble close-up lit by the sun basis
##       as first written (2 s), then by the corrected one in ceada15 (2 s).

var out_dir := ""

func _initialize() -> void: call_deferred("run")

func step(count: int = 8) -> void:
	for i in range(count): await process_frame

func find_game(node: Node) -> GameManager:
	if node is GameManager: return node
	for child in node.get_children():
		var found := find_game(child)
		if found != null: return found
	return null

func save(label: String) -> void:
	await step()
	await RenderingServer.frame_post_draw
	var image := root.get_texture().get_image()
	image.save_png(out_dir.path_join(label + ".png"))
	# Under --write-movie the window is capped at the screen size, but the
	# movie is written at the override size: the film takes this frame from
	# the 4K movie by its number.
	print("SAVED ", label, " ", image.get_size(), " frame ", Engine.get_frames_drawn())
	await step(15)

func run() -> void:
	out_dir = ProjectSettings.globalize_path("res://").path_join("capture_out")
	DirAccess.make_dir_recursive_absolute(out_dir)
	var mode: String = OS.get_cmdline_user_args()[0] if OS.get_cmdline_user_args().size() > 0 else "stills"
	if mode == "stills":
		await stills()
	elif mode == "light":
		await light()
	else:
		await orbit()
	quit()

func stills() -> void:
	var rig: Node = load("res://game/main.tscn").instantiate()
	rig.persist_sessions = false
	root.add_child(rig)
	await step()
	var game := find_game(rig)
	game.fixed_map_seed = 1729
	await game.start_contract("mine")
	game.open_modal("capture")
	var ramps: Array[Dictionary] = game.world_map.ramp_midpoints()
	print("RAMPS ", ramps.size())
	var ramp: Dictionary = ramps[0]
	var foot: Vector2 = ramp.point - ramp.up * 6.0
	game.player.teleport(game.world_map.nearest_walkable(Vector3(foot.x, 0.7, foot.y)))
	game.camera.global_position = game.player.global_position + GameManager.CAMERA_OFFSET
	await save("game-ramp")
	var top: Vector2 = ramp.point + ramp.up * 7.0
	game.player.teleport(game.world_map.nearest_walkable(Vector3(top.x, 0.7, top.y)))
	game.camera.global_position = game.player.global_position + GameManager.CAMERA_OFFSET
	await save("game-terrace")
	# A cliff between terraces, found the way capture_terrain.gd finds one:
	# mine floors on the seeds it tries, until a level spot 2.2 above another
	# lies 5 m away across open ground.
	for attempt in [0, 3, 6, 9, 12, 15]:
		game.close_modal()
		game.settle(true)
		game.fixed_map_seed = 1000 + attempt * 37
		await game.start_contract("mine")
		game.open_modal("capture")
		var pair := _cliff_pair(game.world_map)
		if pair.is_empty(): continue
		var middle: Vector2 = (pair[0] + pair[1]) * 0.5
		game.player.teleport(game.world_map.nearest_walkable(Vector3(pair[1].x, 0.7, pair[1].y)))
		game.camera.global_position = Vector3(middle.x, game.player.global_position.y, middle.y) + GameManager.CAMERA_OFFSET
		print("CLIFF seed ", game.fixed_map_seed, " high ", pair[0], " low ", pair[1])
		await save("game-cliff")
		break

## Copied from tests/capture_terrain.gd: two level spots across a cliff.
func _cliff_pair(map: ContinuousWorldMap) -> Array:
	for z in range(int(map.SPINE_MIN.y), int(map.SPINE_MAX.y), 2):
		for x in range(int(map.SPINE_MIN.x), int(map.SPINE_MAX.x), 2):
			var high := Vector2(x, z)
			if not map._has_clearance(high): continue
			var h := map.ground_height(high)
			if h < map.TIER - 0.1: continue
			for k in range(8):
				var direction := Vector2.from_angle(TAU * k / 8.0)
				var low := high + direction * 5.0
				if not map._has_clearance(low) or map.ground_height(low) > h - map.TIER + 0.1: continue
				var open := true
				for t in range(1, 10):
					if not map._is_open(high.x + direction.x * t * 0.5, high.y + direction.y * t * 0.5, 0.0): open = false
				if open: return [high, low]
	return []

func orbit() -> void:
	var scene: Node3D = load("res://art/models/asset_preview.tscn").instantiate()
	root.add_child(scene)
	var cam: Camera3D = scene.get_node("Camera3D")
	for i in range(60): await process_frame          # 2 s through the game camera
	cam.projection = Camera3D.PROJECTION_PERSPECTIVE
	cam.fov = 45.0
	var centre := Vector3(-0.25, 0.9, -2.0)
	var frames := 16 * 30
	for i in range(frames):
		# Starts in front (+Z, facing the cliff's face), goes all the way round.
		var a := TAU * float(i) / float(frames)
		cam.position = centre + Vector3(sin(a) * 15.0, 6.5, cos(a) * 15.0)
		cam.look_at(centre, Vector3.UP)
		await process_frame

## The sun's basis as the first preview scene wrote it. The .tscn lists
## Transform3D's basis by rows; it was typed by columns, so these are the rows
## Godot actually read, and -Z (the light direction) points upward.
const SUN_AS_FIRST_WRITTEN := Basis(Vector3(0.866025, 0, 0.5), Vector3(-0.353553, -0.707107, 0.612372), Vector3(0.353553, -0.707107, -0.612372))

func light() -> void:
	var scene: Node3D = load("res://art/models/asset_preview.tscn").instantiate()
	root.add_child(scene)
	var cam: Camera3D = scene.get_node("Camera3D")
	var sun: DirectionalLight3D = scene.get_node("Sun")
	var fixed := sun.basis
	cam.projection = Camera3D.PROJECTION_PERSPECTIVE
	cam.fov = 40.0
	cam.position = Vector3(6.5, 2.5, -3.5)
	cam.look_at(Vector3(6.5, 0.4, 0.0), Vector3.UP)
	sun.basis = SUN_AS_FIRST_WRITTEN
	print("LIGHT before: direction ", -sun.basis.z)
	for i in range(60): await process_frame
	sun.basis = fixed
	print("LIGHT after: direction ", -sun.basis.z)
	for i in range(60): await process_frame

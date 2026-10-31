extends SceneTree

const OUT := "res://evidence/a5/use-it/"
var game: GameManager
var seen := {}
var events: Array = []
var count := 0
var first_flame := false
var view: Viewport
var frame_directory := ""
var output_frame := 0

func save_frame() -> void:
	if frame_directory.is_empty(): return
	view.get_texture().get_image().save_jpg(frame_directory + "/%05d.jpg" % output_frame, 0.97)
	output_frame += 1

func _initialize() -> void:
	call_deferred("run")

func _process(_delta: float) -> bool:
	count += 1
	if not is_instance_valid(game): return false
	for hazard in get_nodes_in_group("ground_hazards"):
		var id: int = hazard.get_instance_id()
		if seen.has(id): continue
		seen[id] = true
		events.append({"frame": Engine.get_frames_drawn(), "id": id, "lasting": hazard.lasting, "fuse": hazard.fuse, "flame": hazard.has_node("Flame"), "decal": is_instance_valid(hazard._disc), "warning": hazard.has_node("Warning"), "source": hazard.source.enemy_type if is_instance_valid(hazard.source) else "none"})
	return false

func frames(n: int) -> void:
	for i in n: await process_frame

func shot(name: String) -> void:
	await RenderingServer.frame_post_draw
	view.get_texture().get_image().save_png(OUT + name + ".png")

func run() -> void:
	view = root
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--frames="):
			frame_directory = arg.trim_prefix("--frames=")
			DirAccess.make_dir_recursive_absolute(frame_directory)
			var viewport := SubViewport.new()
			viewport.size = Vector2i(3840, 2160)
			viewport.own_world_3d = true
			viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
			root.add_child(viewport)
			view = viewport
	game = GameManager.new()
	game.save_enabled = false
	game.fixed_map_seed = 1729
	view.add_child(game)
	await frames(8)
	await game.start_contract("city")
	var player := game.player
	player.invulnerable = true
	var target: Vector2 = game.world_map.main_path[0] + Vector2(0, 8)
	player.teleport(game.world_map.nearest_walkable(Vector3(target.x, 0.7, target.y)))
	game.camera.size = 15.0
	await frames(12)
	var started := Engine.get_frames_drawn()
	if not frame_directory.is_empty(): RenderingServer.frame_post_draw.connect(save_frame)
	var at := player.global_position
	var thrower: Enemy
	for offset in [Vector3(5, 0, 0), Vector3(-5, 0, 0), Vector3(0, 0, 5), Vector3(0, 0, -5)]:
		var spawn_at: Vector3 = game.world_map.nearest_walkable(at + offset)
		if at.distance_to(spawn_at) > 2 and game.line_of_sight(spawn_at, at):
			thrower = game._spawn_enemy(spawn_at, false, false, "thrower")
			thrower.begin_chase()
			break
	var pause_record := {}
	for i in 900:
		await process_frame
		var flames := get_nodes_in_group("ground_hazards").filter(func(h): return h.has_node("Flame"))
		if not flames.is_empty() and not first_flame:
			first_flame = true
			await shot("gameplay-fire")
			var hazard: GroundHazard = flames[0]
			var material := hazard.get_node("Flame").material_override as ShaderMaterial
			var before: float = material.get_shader_parameter("fire_remaining")
			game.open_modal("capture")
			await frames(60)
			pause_record = {"before": before, "after": material.get_shader_parameter("fire_remaining"), "lasting": hazard.lasting}
			await shot("gameplay-paused")
			game.close_modal()
		if i == 440: await shot("gameplay-repeat-fire")
	if is_instance_valid(thrower): thrower.queue_free()
	var slug := game._spawn_enemy(player.global_position + Vector3(1.5, 0, 0), false, false, "slug_volatile")
	slug.take_hit(99999.0, "true")
	await frames(6)
	await shot("gameplay-slug-warning")
	await frames(150)
	await shot("gameplay-after-slug")
	var result := {"engine": Engine.get_version_info().string, "renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name(), "movie_start_frame": started, "movie_end_frame": Engine.get_frames_drawn(), "events": events, "pause": pause_record, "fire_count": events.filter(func(e): return e.flame).size(), "blast_without_flame_count": events.filter(func(e): return e.fuse > 0 and not e.flame and e.warning).size(), "environment_tonemap": game.world_environment.environment.tonemap_mode}
	var f := FileAccess.open(OUT + "gameplay.json", FileAccess.WRITE)
	result["capture_size"] = str(view.get_texture().get_size())
	result["output_frames"] = output_frame
	f.store_string(JSON.stringify(result, "\t"))
	f.close()
	print("A5_GAMEPLAY_COMPLETE ", JSON.stringify(result))
	quit(0 if result.fire_count >= 3 and result.blast_without_flame_count >= 1 else 1)

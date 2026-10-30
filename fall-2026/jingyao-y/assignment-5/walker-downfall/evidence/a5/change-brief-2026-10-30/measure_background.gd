extends SceneTree
## Read-only scene measurements for CHANGE-BRIEF; no effect implementation.
var game: GameManager

func _initialize() -> void:
	call_deferred("run")

func step(count: int = 12) -> void:
	for i in range(count):
		await process_frame

func find_game(node: Node) -> GameManager:
	if node is GameManager:
		return node
	for child in node.get_children():
		var found := find_game(child)
		if found != null:
			return found
	return null

func run() -> void:
	var rig = load("res://game/main.tscn").instantiate()
	rig.persist_sessions = false
	root.add_child(rig)
	await step()
	game = find_game(rig)
	game.fixed_map_seed = 2026
	await game.start_contract("city")
	game.open_modal("capture")
	var at: Vector2 = game.world_map.main_path[0] + Vector2(0, 8)
	game.player.teleport(game.world_map.nearest_walkable(Vector3(at.x, 0.7, at.y)))
	game.camera.size = 24.0
	game.camera.global_position = game.player.global_position + GameManager.CAMERA_OFFSET
	game._hud.hide()
	game.player.hide()
	for hazard in get_nodes_in_group("ground_hazards"):
		hazard.hide()
	await step(30)
	var original := game.world_environment.environment
	var result := {
		"engine": Engine.get_version_info().string,
		"renderer": RenderingServer.get_current_rendering_method(),
		"driver": RenderingServer.get_current_rendering_driver_name(),
		"seed": 2026,
		"camera_size": game.camera.size,
		"camera_transform": str(game.camera.global_transform),
		"player_position": str(game.player.global_position),
		"original_environment": {
			"tonemap_mode": original.tonemap_mode,
			"tonemap_exposure": original.tonemap_exposure,
			"glow_enabled": original.glow_enabled,
			"fog_enabled": original.fog_enabled,
			"adjustment_enabled": original.adjustment_enabled,
			"ssao_enabled": original.ssao_enabled,
			"ssil_enabled": original.ssil_enabled,
		},
	}
	# Duplicate only in this disposable run. Production settings are unchanged.
	var controlled := original.duplicate() as Environment
	controlled.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	controlled.tonemap_exposure = 1.0
	controlled.glow_enabled = false
	controlled.fog_enabled = false
	controlled.volumetric_fog_enabled = false
	controlled.adjustment_enabled = false
	controlled.ssao_enabled = false
	controlled.ssil_enabled = false
	controlled.ssr_enabled = false
	game.world_environment.environment = controlled
	game.outline_pass.hide()
	result["controlled_environment"] = {
		"tonemap_mode": controlled.tonemap_mode,
		"tonemap_exposure": controlled.tonemap_exposure,
		"glow_enabled": controlled.glow_enabled,
		"fog_enabled": controlled.fog_enabled,
		"volumetric_fog_enabled": controlled.volumetric_fog_enabled,
		"adjustment_enabled": controlled.adjustment_enabled,
		"ssao_enabled": controlled.ssao_enabled,
		"ssil_enabled": controlled.ssil_enabled,
		"ssr_enabled": controlled.ssr_enabled,
	}
	await step(30)
	await RenderingServer.frame_post_draw
	var img := root.get_texture().get_image()
	var out := "D:/CSYE 7370/evidence/change-brief-2026-10-30/"
	img.save_png(out + "city-background.png")
	result["image_size"] = str(img.get_size())
	result["samples"] = []
	for pixel in [Vector2i(640, 420), Vector2i(704, 420)]:
		var c := img.get_pixelv(pixel)
		result.samples.append({"pixel": str(pixel), "rgb8": [roundi(c.r * 255), roundi(c.g * 255), roundi(c.b * 255)]})
	var output := FileAccess.open(out + "measurement.json", FileAccess.WRITE)
	output.store_string(JSON.stringify(result, "\t"))
	output.close()
	print("BRIEF_MEASUREMENT ", JSON.stringify(result))
	game.world_environment.environment = original
	rig.queue_free()
	await step(3)
	quit()

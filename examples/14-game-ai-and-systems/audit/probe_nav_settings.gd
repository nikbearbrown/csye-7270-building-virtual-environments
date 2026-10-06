extends SceneTree
func _initialize():
	for k in ["navigation/world/map_use_async_iterations", "navigation/2d/use_edge_connections", "navigation/world/region_use_async_iterations", "physics/common/max_physics_steps_per_frame", "physics/common/physics_ticks_per_second"]:
		print(k, " = ", ProjectSettings.get_setting(k, "<missing>"))
	quit()

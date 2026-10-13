extends SceneTree
# Records the machine and the renderer behind every number in this film's evidence (the Shader Lab uses the same window/renderer).
# Run (needs a window): godot --path <scratch project> --script res://verify_env.gd
func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	await process_frame
	await process_frame
	var info := Engine.get_version_info()
	print("RESULT " + JSON.stringify({"id": "env", "engine": info["string"], "adapter": RenderingServer.get_video_adapter_name(),
		"vendor": RenderingServer.get_video_adapter_vendor(), "renderer": RenderingServer.get_current_rendering_method(),
		"driver": RenderingServer.get_current_rendering_driver_name(), "os": OS.get_name(), "os_version": OS.get_version(), "cpu": OS.get_processor_name()}))
	quit(0)

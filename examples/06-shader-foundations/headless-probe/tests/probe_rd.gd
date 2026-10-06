extends SceneTree

func _initialize() -> void:
	print("DISPLAY=", DisplayServer.get_name())
	print("RENDERING_METHOD=", RenderingServer.get_current_rendering_method())
	print("RENDERING_DRIVER=", RenderingServer.get_current_rendering_driver_name())
	print("VIDEO_ADAPTER=", RenderingServer.get_video_adapter_name())
	print("RS.get_rendering_device=", RenderingServer.get_rendering_device())
	print("RS.create_local_rendering_device=", RenderingServer.create_local_rendering_device())
	quit(0)

extends SceneTree
# Reads the default roll-over limit from the running engine (a project that never set it), and the default time scale.
func _initialize() -> void:
	print("RESULT " + JSON.stringify({"id": "default-rollover", "rendering/limits/time/time_rollover_secs": ProjectSettings.get_setting("rendering/limits/time/time_rollover_secs"),
		"has_setting": ProjectSettings.has_setting("rendering/limits/time/time_rollover_secs"), "Engine.time_scale": Engine.time_scale}))
	quit(0)

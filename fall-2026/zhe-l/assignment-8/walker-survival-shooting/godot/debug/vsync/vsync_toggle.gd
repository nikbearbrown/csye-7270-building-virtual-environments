extends Node

const TOGGLE_KEY := KEY_V


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == TOGGLE_KEY:
		var off := DisplayServer.window_get_vsync_mode() == DisplayServer.VSYNC_DISABLED
		DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_ENABLED if off else DisplayServer.VSYNC_DISABLED)
		print("[vsync] %s" % ("on" if off else "off"))

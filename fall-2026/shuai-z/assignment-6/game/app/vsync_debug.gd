extends Node
## A debug key for the GPU price (CHANGE-BRIEF.md, sections 4 and 8): F9 turns
## vsync off and on again, so an FPS comparison in the editor is not held at
## the display's refresh rate. It changes no project setting, reads no game
## state, and no input action uses F9 (game/project.godot, input map). It
## works while the game is paused too. Each press prints the new mode to the
## Output panel.


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_F9:
		var was_off := DisplayServer.window_get_vsync_mode() == DisplayServer.VSYNC_DISABLED
		DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_ENABLED if was_off else DisplayServer.VSYNC_DISABLED)
		print("F9: vsync %s" % ("on" if was_off else "off"))

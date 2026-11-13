# ============================================================
# Class declaration: what it extends, what the whole script does
# ============================================================
extends Node  # A plain node in base.tscn; it only listens for one debug key
## A6 Use It: we press V in the running game to turn vsync off or back on, so an FPS comparison can rise above the
## display's refresh rate. It changes only the window's vsync mode, never game state, and no project setting.
## V is not used by the game. F10 was tried first and did nothing: on Windows F10 is the system menu key. F9 is taken by the A5 capture tool, and F7 / F8 pause and stop the run in the editor.

# ============================================================
# Constants: the debug key
# ============================================================
const TOGGLE_KEY := KEY_V  # The key we press to switch vsync


# ============================================================
# Engine callbacks: functions Godot calls automatically at set times
# ============================================================
## Called by Godot when an input event reaches this node and nothing else has handled it. Handles V only.
func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == TOGGLE_KEY:  # If this is a fresh press of V
		var off := DisplayServer.window_get_vsync_mode() == DisplayServer.VSYNC_DISABLED  # First we read whether vsync is off now
		DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_ENABLED if off else DisplayServer.VSYNC_DISABLED)  # Then we flip it
		print("[vsync] %s" % ("on" if off else "off"))  # And we say which way it went, so the profiler reading can be labelled

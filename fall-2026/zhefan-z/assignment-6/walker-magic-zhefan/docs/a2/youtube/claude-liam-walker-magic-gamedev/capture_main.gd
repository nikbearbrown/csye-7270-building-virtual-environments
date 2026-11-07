extends Node
## Capture harness entry point (lives only in the throwaway capture copy, at res://capture/).
## Instantiates the REAL main scene (game/main.tscn) untouched and adds the input-only
## driver beside it. Nothing in the game's own code is modified for capture.
##
## Environment:
##   WALKER_CAPTURE_MODE=probe|run-01|run-02|run-03|run-04
##   WALKER_CAPTURE_LOG=<path>   JSONL input/event log (appended across the run-02 reload)
##   WALKER_CAPTURE_MAX=<int>    hard frame cap per attempt (default 3000)
##   WALKER_CAPTURE_SCALE=<int>  integer scale of the 640x360 canvas (default 6 -> 3840x2160)
##
## Native 4K for a pixel-art game that uses stretch mode "viewport": the capture copy's
## project.godot sets a 3840x2160 root viewport (stretch mode "viewport" kept, so it stays
## 3840x2160 even when the OS clamps the window to a smaller screen), and the real main scene
## runs inside a 640x360 SubViewport drawn at x6 with nearest filtering. That is the same
## integer upscale the game's own window performs, rendered by the engine at 4K, not a
## low-resolution recording enlarged afterwards. Disclosed in CAPTURE.md.
##
## run-02 contains a real pit fall, and the game reloads its scene 1.2 s later. Here the
## reloaded scene is this harness, so an attempt counter kept on Engine metadata tells the
## driver it is the second attempt (music restarted from the top) instead of falling again.

const Driver := preload("res://capture/capture_driver.gd")

const LOGICAL := Vector2i(640, 360)

var main: Node
var driver: Node
var container: SubViewportContainer
var scale := 6
var frames := 0
var max_frames := 3000
var tail := -1


func _ready() -> void:
	# The harness keeps counting while the game is paused (run-04); the game itself stays
	# pausable exactly as when main.tscn is the root scene.
	process_mode = Node.PROCESS_MODE_ALWAYS
	var cap := OS.get_environment("WALKER_CAPTURE_MAX")
	if cap != "":
		max_frames = int(cap)
	var attempt: int = int(Engine.get_meta("walker_capture_attempt", 0)) + 1
	Engine.set_meta("walker_capture_attempt", attempt)
	var sc := OS.get_environment("WALKER_CAPTURE_SCALE")
	if sc != "":
		scale = int(sc)
	container = SubViewportContainer.new()
	container.stretch = true
	container.stretch_shrink = scale
	container.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	container.size = Vector2(LOGICAL * scale)
	add_child(container)
	var sub := SubViewport.new()
	sub.size = LOGICAL
	sub.canvas_item_default_texture_filter = Viewport.DEFAULT_CANVAS_ITEM_TEXTURE_FILTER_NEAREST
	sub.snap_2d_transforms_to_pixel = true
	sub.snap_2d_vertices_to_pixel = true
	container.add_child(sub)
	main = (load("res://game/main.tscn") as PackedScene).instantiate()
	main.process_mode = Node.PROCESS_MODE_PAUSABLE
	sub.add_child(main)
	driver = Driver.new()
	driver.main = main
	driver.to_window = world_to_window
	driver.to_root = world_to_root
	driver.mode = OS.get_environment("WALKER_CAPTURE_MODE")
	driver.attempt = attempt
	driver.log_path = OS.get_environment("WALKER_CAPTURE_LOG")
	add_child(driver)


## On Windows, Godot releases every held input when its window loses focus (seen in a 4K
## probe: the run key let go mid-take). Focus losses are logged and the window is asked back
## to the front; the driver re-asserts held actions before the player reads them. Whether the
## take is valid is decided by the headless reference gate (CAPTURE.md), not assumed.
func _notification(what: int) -> void:
	if what in [NOTIFICATION_APPLICATION_FOCUS_OUT, NOTIFICATION_WM_WINDOW_FOCUS_OUT] and driver and not driver.done:
		driver.note_focus_loss(frames)
		DisplayServer.window_move_to_foreground()


## A world point inside the game -> window pixels, so the driver's mouse events land
## where the game's own get_global_mouse_position() reads them back.
func world_to_window(world: Vector2) -> Vector2:
	# Root viewport pixels -> window pixels (the OS may have clamped the window).
	return get_tree().root.get_final_transform() * world_to_root(world)


## The same point in root-viewport pixels (what Input.warp_mouse expects).
func world_to_root(world: Vector2) -> Vector2:
	var canvas: Vector2 = main.get_viewport().get_canvas_transform() * world
	return container.global_position + canvas * float(scale)


func _physics_process(_delta: float) -> void:
	frames += 1
	if driver.done and tail < 0:
		tail = driver.tail_frames
	if tail > 0:
		tail -= 1
	if tail == 0 or frames >= max_frames:
		var code: int = driver.exit_code if tail == 0 else 2
		driver.finish("end" if tail == 0 else "frame cap reached before the take completed")
		print("CAPTURE END mode=%s attempt=%d frames=%d exit=%d events=%s" % [
			driver.mode, driver.attempt, frames, code, JSON.stringify(driver.events)])
		get_tree().quit(code)

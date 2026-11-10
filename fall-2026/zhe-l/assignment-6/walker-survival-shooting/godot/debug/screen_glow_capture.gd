# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
extends Node  # Root-node script of the debug scene screen_glow_capture.tscn
## A5 capture tool (for the human check, not an automated test): run in a real window, press F9,
## and it sets pad_light_data on the player's tablet screen to 0 / 0.39 / 1.0 / 2.0 in turn, captures each value with the engine (not an OS screenshot),
## and prints the RGB of three pixels — screen centre P1, a screen corner P2, the bezel P3 — beside the hand-computed predictions from CHANGE-BRIEF.
## Use: open debug/screen_glow_capture.tscn in the editor and press F6; long-press Tab to hold the tablet in both hands, wait until the screen lights, then press F9.
## Captures are saved to ../captures/ (beside the Godot project folder). It changes neither base.tscn nor any game code.

# ============================================================
# Constants: the values to capture, the pixel positions and the predictions, all from CHANGE-BRIEF
# ============================================================
const CAPTURE_KEY := KEY_F9  # Press this key to start capturing
const PARAM := &"pad_light_data"  # The shader parameter being set
const VALUES := [0.0, 0.39, 1.0, 2.0]  # Three controlled values + 2.0 for the hint_range experiment
# Predictions (the hand-computed table in CHANGE-BRIEF; 2.0 is my "hint_range does not clamp" prediction): RGB of P1 / P2
const PREDICTED := {0.0: Color8(0, 0, 0), 0.39: Color8(151, 162, 162), 1.0: Color8(230, 247, 247), 2.0: Color8(255, 255, 255)}
const SCREEN_SIZE := Vector2(0.18, 0.108)  # Size of the Screen quad (metres), the same as the QuadMesh in tablet_device.tscn
const CORNER_INSET := 0.01  # How far P2 is from the screen edges (metres), to stay clear of edge anti-aliasing
const BEZEL_POINT := Vector3(0.0, -0.066, 0.014)  # P3: in TabletDevice's own coordinates, on the casing 12 mm below the screen's lower edge
const MARK_RADIUS := 6  # Half-size (pixels) of the small box drawn around each sample point in the marked image
const OUT_DIR := "../captures"  # Where captures are saved: relative to the Godot project folder

# ============================================================
# Node references (@onready): nodes used in the scene
# ============================================================
@onready var _player: Humanoid = $Base/Player  # The player body in base.tscn
@onready var _brain: Node = $Base/Player/PlayerController  # The player brain: the driver runs in its _physics_process()
@onready var _tablet: TabletDevice = $Base/Player/Visual/TabletDevice  # The player's tablet
@onready var _screen: MeshInstance3D = $Base/Player/Visual/TabletDevice/Screen  # The player's tablet screen

var _busy := false  # true while capturing, so F9 cannot be pressed twice


# ============================================================
# Engine callbacks: functions Godot calls automatically at set times
# ============================================================
## Called by Godot when an input event arrives and no other node has handled it. Handles F9 only.
func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == CAPTURE_KEY and not _busy:
		_capture_all()


# ============================================================
# Feature functions
# ============================================================
## Captures the four values in turn and prints the pixels. The player brain's physics processing is paused while capturing; otherwise the driver would set the value back on the next frame.
func _capture_all() -> void:
	_busy = true
	var mat := _screen.get_surface_override_material(0) as ShaderMaterial
	var dir := ProjectSettings.globalize_path("res://").path_join(OUT_DIR)
	DirAccess.make_dir_recursive_absolute(dir)
	_brain.set_physics_process(false)  # Pause the driver (required by the assignment's Use It section)
	var camera := get_viewport().get_camera_3d()
	var points := {
		"P1 centre": _screen.global_transform * Vector3.ZERO,
		"P2 corner": _screen.global_transform * Vector3(SCREEN_SIZE.x / 2.0 - CORNER_INSET, SCREEN_SIZE.y / 2.0 - CORNER_INSET, 0.0),
		"P3 bezel": _tablet.global_transform * BEZEL_POINT,
	}
	var pixels := {}
	for name in points:
		pixels[name] = Vector2i(camera.unproject_position(points[name]).round())
	print("viewport %s, hold %s, pixels %s" % [get_viewport().get_visible_rect().size, _player.get_tablet_hold(), pixels])
	for value in VALUES:
		mat.set_shader_parameter(PARAM, value)
		await RenderingServer.frame_post_draw  # Wait until this frame has been drawn
		await RenderingServer.frame_post_draw  # Wait one more frame: makes sure the drawn frame already uses the new value
		var image := get_viewport().get_texture().get_image()
		var file := dir.path_join("screen_pad_%.2f.png" % value)
		image.save_png(file)
		var line := "pad_light_data %.2f:" % value
		for name in pixels:
			var c := image.get_pixelv(pixels[name])
			line += "  %s %s" % [name, _rgb(c)]
		print(line + "   predicted P1/P2 " + _rgb(PREDICTED[value]))
		_save_marked(image, pixels, dir.path_join("screen_pad_%.2f_marked.png" % value))
	_brain.set_physics_process(true)  # Resume the driver: on the next frame the screen goes back to its in-game value
	print("captures saved to ", dir)
	_busy = false


## Turns a colour into 0–255 integers, written as (R, G, B).
func _rgb(c: Color) -> String:
	return "(%d, %d, %d)" % [c.r8, c.g8, c.b8]


## Saves a second, marked image: draws a small red box around each sample point to confirm the sample positions (sampling uses the original image without boxes).
func _save_marked(image: Image, pixels: Dictionary, path: String) -> void:
	var marked := image.duplicate() as Image
	for name in pixels:
		var p: Vector2i = pixels[name]
		for i in range(-MARK_RADIUS, MARK_RADIUS + 1):
			for edge in [Vector2i(i, -MARK_RADIUS), Vector2i(i, MARK_RADIUS), Vector2i(-MARK_RADIUS, i), Vector2i(MARK_RADIUS, i)]:
				var q: Vector2i = p + edge
				if q.x >= 0 and q.y >= 0 and q.x < marked.get_width() and q.y < marked.get_height():
					marked.set_pixelv(q, Color.RED)
	marked.save_png(path)

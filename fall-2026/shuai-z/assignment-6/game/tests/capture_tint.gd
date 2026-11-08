extends Node
## Windowed capture of the hearts' tint for TEST-REPORT.md (CHANGE-BRIEF.md
## section 3; the assignment's Use It). After one hit at the first spikes, once
## that window has run out, it stops the driver and sets tint_amount from code
## to 0.0, 0.5, 1.0 and 2.0, saving each frame as the engine drew it, then once
## more with no material on the hearts. It prints the sampled pixels beside the
## brief's predictions. It opens a window; run from assignment-5/:
##   godot --path game --resolution 1920x1080 --always-on-top res://tests/capture_tint.tscn
## The PNGs go to evidence/use-it/. A frame is never resized, which would blend
## the pixels: the brief's 1920 x 1080 coordinates are scaled to the size drawn.

const MAIN := preload("res://app/main.tscn")
const LAYOUT := Vector2(1920, 1080)
## name, position in the 1920 x 1080 layout (CHANGE-BRIEF.md section 3)
const PIXELS := [["P1", Vector2(54, 58)], ["P2", Vector2(77, 56)], ["P3", Vector2(183, 49)], ["B", Vector2(222, 52)]]
## tint_amount, then P1's and P2's predicted colours (section 3)
const VALUES := [
	[0.0, "C84035", "992323"],
	[0.5, "BF605D", "99494F"],
	[1.0, "B58086", "996F7B"],
	[2.0, "A2C0D7", "99BBD3"], # if hint_range does not clamp
]
const CLAMPED := ["B58086", "996F7B"] ## P1 and P2 at 2.0 if hint_range does clamp
const HEARTS_RECT := Rect2(32, 24, 200, 56) ## Hud/Hearts in the layout (hud.tscn)
const STEPS := 2 ## "more than a step or two per channel is a finding"

var _main: Main
var _rudy: Rudy


func _ready() -> void:
	if DisplayServer.get_name() == "headless":
		printerr("STOP this needs a window: a headless run draws no frame to read")
		get_tree().quit(1)
		return
	var out_dir := ProjectSettings.globalize_path("res://").path_join("../evidence/use-it").simplify_path()
	DirAccess.make_dir_recursive_absolute(out_dir)
	Main.title_shown = true # straight to play
	_main = MAIN.instantiate()
	add_child(_main)
	_rudy = _main.get_node("Rudy")
	await _frames(30)
	# One hit at the first spikes, then wait for that window to run out with him standing still.
	Input.action_press(&"move_right")
	await _until(func() -> bool: return _rudy.hearts == 2)
	Input.action_release(&"move_right")
	print("HIT at x %.0f; hearts %d" % [_rudy.global_position.x, _rudy.hearts])
	await _until(func() -> bool: return not _rudy.is_invulnerable() and _rudy.is_on_floor() and _rudy.velocity.x == 0.0)
	await _frames(30)
	print("STILL at x %.0f, not invulnerable; hearts %d" % [_rudy.global_position.x, _rudy.hearts])

	var hud := _main.get_node("Hud")
	var hearts := hud.get_node("Hearts") as CanvasItem
	var material := hearts.material as ShaderMaterial
	hud.set_process(false) # the driver: it would overwrite the value before the frame draws
	var baseline: Image
	for v: Array in VALUES:
		material.set_shader_parameter(&"tint_amount", v[0])
		var image := await _capture(out_dir.path_join("hearts-tint-%.1f.png" % v[0]))
		if image == null:
			return
		print("SET tint_amount %.1f; the material reads back %s" % [v[0], material.get_shader_parameter(&"tint_amount")])
		if baseline == null:
			baseline = image
		_report(image, v, baseline)
	# Rule 7: at 0.0 the hearts are exactly as they are without the shader.
	material.set_shader_parameter(&"tint_amount", 0.0)
	hearts.material = null
	var without := await _capture(out_dir.path_join("hearts-no-material.png"))
	hearts.material = material
	if without == null:
		return
	_compare(baseline, without)
	hud.set_process(true)
	get_tree().quit()


func _capture(path: String) -> Image:
	await get_tree().process_frame # the new value is drawn from the next frame on
	await RenderingServer.frame_post_draw
	var image := get_viewport().get_texture().get_image()
	if image == null:
		printerr("STOP no frame to read: run this in a window, not with --headless")
		get_tree().quit(1)
		return null
	image.save_png(path)
	print("SAVED %s, %d x %d as drawn" % [path.get_file(), image.get_width(), image.get_height()])
	return image


func _report(image: Image, v: Array, baseline: Image) -> void:
	for p: Array in PIXELS:
		var at := _scaled(p[1], image)
		var shown := image.get_pixelv(at).to_html(false).to_upper()
		var line := "PIXEL tint %.1f %s at %s: #%s" % [v[0], p[0], at, shown]
		if p[0] == "P1" or p[0] == "P2":
			var i := 1 if p[0] == "P1" else 2
			line += ", predicted #%s, %s" % [v[i], _verdict(shown, v[i])]
			if v[0] == 2.0:
				line += "; clamped would be #%s, %s" % [CLAMPED[i - 1], _verdict(shown, CLAMPED[i - 1])]
		elif p[0] == "P3":
			var first := baseline.get_pixelv(at).to_html(false).to_upper()
			line += ", at 0.0 it was #%s, %s" % [first, _verdict(shown, first)]
		print(line)


func _compare(with_shader: Image, without: Image) -> void:
	var corner := _scaled(HEARTS_RECT.position, with_shader)
	var end := _scaled(HEARTS_RECT.end, with_shader)
	var differ := 0
	var worst := 0
	for y in range(corner.y, end.y):
		for x in range(corner.x, end.x):
			var d := _distance(with_shader.get_pixel(x, y), without.get_pixel(x, y))
			if d > 0:
				differ += 1
			worst = maxi(worst, d)
	print("RULE 7 tint 0.0 against no material, over the hearts (%s to %s): %d of %d pixels differ, by at most %d" % [
		corner, end, differ, (end.x - corner.x) * (end.y - corner.y), worst])


func _scaled(at: Vector2, image: Image) -> Vector2i:
	return Vector2i((at * Vector2(image.get_size()) / LAYOUT).floor())


func _verdict(shown: String, want: String) -> String:
	var d := _distance(Color.html(shown), Color.html(want))
	return "off by %d (%s)" % [d, "within %d" % STEPS if d <= STEPS else "a finding"]


## The largest difference in one channel, in 8-bit steps.
func _distance(a: Color, b: Color) -> int:
	return maxi(maxi(absi(a.r8 - b.r8), absi(a.g8 - b.g8)), absi(a.b8 - b.b8))


func _until(condition: Callable) -> void:
	for i in 600:
		if condition.call():
			return
		await get_tree().physics_frame
	push_error("capture_tint: a condition never came true")


func _frames(n: int) -> void:
	for i in n:
		await get_tree().physics_frame

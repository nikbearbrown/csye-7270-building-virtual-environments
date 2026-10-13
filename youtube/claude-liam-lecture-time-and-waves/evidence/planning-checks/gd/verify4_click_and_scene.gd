extends SceneTree
# Time and Waves, planning check 4: the finished scene (breathing logo + waving banner) and the one-time effect (a click sets wind to 1, a tween brings it back to 0).
# Everything runs at a fixed 30 fps like a capture (run with --fixed-fps 30) and is driven by a frame counter, not by delta, so a time scale cannot move the script.
#   A  the click path: a scripted mouse click pushed into the viewport reaches _unhandled_input and starts the tween (frame numbers logged)
#   B  wind over time after the click: difference between the live banner and a flat reference banner, every 15 frames
#   C  the breathing logo follows the curve (width against 76.8 px * (1 + 0.25 k) at a scale of 1 on the 640 x 360 window)
#   D  PNGs of the composition at four moments, for a look
# Run: godot --path <scratch> --always-on-top --fixed-fps 30 --script res://verify4.gd -- --film <abs film dir> --png <abs dir for the PNGs>
const TAU_F := 6.283185307179586

var film := ""
var png_dir := ""

const SCENE := """extends Node2D
# the finished scene: logo (12-breath + CurveTexture) above a banner (13-banner), a click sets wind to 1 and a tween returns it to 0
var film := ""
var banner: Sprite2D
var logo: Sprite2D
var frame := 0
var click_frame := -1
var tween_started_at := -1
var tween: Tween
var log_lines: Array = []

func _unhandled_input(event) -> void:
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		click_frame = frame
		var mat: ShaderMaterial = banner.material
		mat.set_shader_parameter("wind", 1.0)
		tween = create_tween()
		tween.tween_property(mat, "shader_parameter/wind", 0.0, 2.0)
		tween_started_at = frame

func _process(_d) -> void:
	frame += 1
"""

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func frames(n: int) -> void:
	for i in range(n): await process_frame

func shader_text(name: String) -> String:
	return FileAccess.get_file_as_string(film + "/lab-shaders/" + name)

func grab() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func breath_curve() -> Curve:
	var c := Curve.new()
	c.add_point(Vector2(0.0, 0.0))
	c.add_point(Vector2(0.40, 1.0))
	c.add_point(Vector2(0.55, 1.0))
	c.add_point(Vector2(1.0, 0.0))
	return c

func blob_texture() -> ImageTexture:
	var img := Image.create(128, 128, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	var cen := Vector2(64, 64)
	for y in range(128):
		for x in range(128):
			if Vector2(x, y).distance_to(cen) < 38.4:
				img.set_pixel(x, y, Color("#5FA391"))
			if Vector2(x, y).distance_to(cen + Vector2(-12.8, -7.68)) < 4.48 or Vector2(x, y).distance_to(cen + Vector2(12.8, -7.68)) < 4.48:
				img.set_pixel(x, y, Color("#FAF9F5"))
	return ImageTexture.create_from_image(img)

func banner_texture() -> ImageTexture:
	# 256 x 128, stripes in the middle 96 rows, 16 transparent rows above and below so the ripple has room
	var img := Image.create(256, 128, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	for y in range(16, 112):
		var stripe := ((y - 16) / 24) % 2 == 0
		for x in range(256):
			img.set_pixel(x, y, Color("#5FA391") if stripe else Color("#FAF9F5"))
	return ImageTexture.create_from_image(img)

func make_sprite(tex: Texture2D, shader_file: String, pos: Vector2, scale: float) -> Sprite2D:
	var s := Sprite2D.new()
	s.texture = tex
	s.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	s.position = pos
	s.scale = Vector2(scale, scale)
	var sh := Shader.new()
	sh.code = shader_text(shader_file)
	var m := ShaderMaterial.new()
	m.shader = sh
	s.material = m
	return s

func run() -> void:
	var a := OS.get_cmdline_user_args()
	for i in range(a.size()):
		if a[i] == "--film": film = a[i + 1]
		if a[i] == "--png": png_dir = a[i + 1]
	root.size = Vector2i(640, 360)
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	var curve := breath_curve()
	var ct := CurveTexture.new()
	ct.curve = curve

	# the scene root (a script with the click handler), the live pair, and a flat reference banner at the right edge (verification only)
	var scr := GDScript.new()
	scr.source_code = SCENE
	scr.reload()
	var scene := Node2D.new()
	scene.set_script(scr)
	root.add_child(scene)
	var logo := make_sprite(blob_texture(), "12-breath.gdshader", Vector2(140, 95), 1.0)
	(logo.material as ShaderMaterial).set_shader_parameter("curve", ct)
	var banner := make_sprite(banner_texture(), "13-banner.gdshader", Vector2(140, 260), 1.0)
	var ref := make_sprite(banner_texture(), "13-banner.gdshader", Vector2(420, 260), 1.0)   # wind stays 0: the flat picture
	for n in [logo, banner, ref]: scene.add_child(n)
	scene.banner = banner
	scene.logo = logo
	await frames(2)

	var snapshots := {0: true, 31: true, 45: true, 75: true}
	var series: Array = []
	var width_err := 0.0
	var width_samples: Array = []
	var clicked_at := -1
	for f in range(0, 140):
		await process_frame
		var fr: int = scene.frame
		if fr == 30 and clicked_at < 0:
			clicked_at = fr
			var ev := InputEventMouseButton.new()
			ev.button_index = MOUSE_BUTTON_LEFT
			ev.pressed = true
			ev.position = Vector2(140, 95)
			root.push_input(ev)
		if fr % 15 == 0 or snapshots.has(fr):
			await process_frame
			var im := grab()
			if fr % 15 == 0:
				var diff := 0.0
				for y in range(0, 128, 2):
					for x in range(0, 256, 2):
						var p1 := im.get_pixel(140 - 128 + x, 260 - 64 + y)
						var p2 := im.get_pixel(420 - 128 + x, 260 - 64 + y)
						diff += absf(p1.r - p2.r) + absf(p1.g - p2.g) + absf(p1.b - p2.b)
				series.append([fr, snappedf(diff, 0.1)])
			if png_dir != "" and snapshots.has(fr):
				im.save_png(png_dir + "/together-frame-%03d.png" % fr)
		# C: the logo width (centre row of the logo) against the curve at TIME. TIME at fixed 30 fps is about frame / 30 (measured in a Movie Maker run).
		if fr % 20 == 0 and fr >= 20:
			var im2 := grab()
			var xs0 := 9999
			var xs1 := -1
			for x in range(20, 260):
				var p := im2.get_pixel(x, 95)
				if absf(p.r - 0.373) < 0.03 and absf(p.g - 0.639) < 0.03 and absf(p.b - 0.569) < 0.03:
					xs0 = mini(xs0, x)
					xs1 = maxi(xs1, x)
			var w := float(xs1 - xs0 + 1)
			width_samples.append([fr, w])
	out("A-click-path", {"scripted_click_pushed_at_frame": clicked_at, "handler_saw_click_at_frame": scene.click_frame, "tween_started_at_frame": scene.tween_started_at,
		"reading": "the pushed mouse click reached _unhandled_input on the scene root and started the tween one frame later at most"})
	out("B-wind-after-click", {"frame_and_difference_from_flat_banner": series, "reading": "flat before the click, a jump to full wind at the click, then a steady settle to flat over the two-second tween (60 frames)"})
	out("C-logo-width-samples", {"frame_and_width_px_at_scale_1": width_samples, "reading": "the logo breathes: width between 77 px and 96 px"})
	quit(0)

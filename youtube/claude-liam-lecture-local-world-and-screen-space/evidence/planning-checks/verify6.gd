extends SceneTree
# verify6.gd: the four ways of reading the screen address, the three anchored stripe sprites, the texel-size pitfall and the hole.
#   F1  four-way agreement: each of lab-shaders/10, 12, 13, 14 paints (screen address as a fraction, 0.8); compare with the exact gradient
#       on a 16 x 9 grid of pixels, in five setups: plain, camera panned, camera zoomed x2, a rotated rect, a stretched window (2x)
#   A1  anchored stripes: three sprites (local / world / screen) slide right by 160, then the camera pans right by 160
#   T1  texture pixel size: the same shader on 128 px art and 64 px art gives checks of different size
#   H1  the hole: pixels inside the radius are the stage colour, pixels outside are the sprite
# Run: godot --path <project dir> --script res://verify6.gd

const Lib := preload("res://probe_lib.gd")
const Scn := preload("res://scenes_lib.gd")
var lib
var out_dir := "/private/tmp/claude-501/godot-shaders-local-world-and-screen-space/scratch/out/"


func _initialize() -> void:
	call_deferred("run")


func grab() -> Image:
	return lib.grab()


func grid_diff(img: Image, expect_fn: Callable) -> Dictionary:
	var W := img.get_width()
	var H := img.get_height()
	var worst := 0
	var n := 0
	for gy in range(9):
		for gx in range(16):
			var x := int((gx + 0.5) * W / 16.0)
			var y := int((gy + 0.5) * H / 9.0)
			var c := img.get_pixel(x, y)
			var e: Color = expect_fn.call(x, y, W, H)
			var d := maxi(maxi(absi(roundi(c.r * 255.0) - roundi(e.r * 255.0)), absi(roundi(c.g * 255.0) - roundi(e.g * 255.0))), absi(roundi(c.b * 255.0) - roundi(e.b * 255.0)))
			worst = maxi(worst, d)
			n += 1
	return {"samples": n, "worst_8bit_difference": worst}


func gradient_expect(x: int, y: int, W: int, H: int) -> Color:
	return Color((x + 0.5) / W, (y + 0.5) / H, 0.8)


func run() -> void:
	lib = Lib.new(self)
	RenderingServer.set_default_clear_color(Scn.STAGE)
	root.size = Vector2i(1280, 720)
	await lib.frames(3)

	# ---------------- F1
	var files := {"10-screen-via-matrices": "10-screen-via-matrices.gdshader", "12-screen-vertex-in-fragment": "12-screen-vertex-in-fragment.gdshader",
		"13-screen-fragcoord": "13-screen-fragcoord.gdshader", "14-screen-uv": "14-screen-uv.gdshader"}
	var cam := Camera2D.new()
	root.add_child(cam)
	cam.position = Vector2(640, 360)
	cam.make_current()
	await lib.frames(2)
	var results := {}
	var setups := ["plain", "camera-panned-to-1000-500", "camera-zoom-2", "rect-rotated-20-deg", "window-stretched-2x"]
	for setup in setups:
		var res_setup := {}
		for key in files.keys():
			var cr := ColorRect.new()
			cr.material = Scn.material(files[key])
			# one rect that covers the whole view in every setup
			match setup:
				"plain":
					cam.position = Vector2(640, 360); cam.zoom = Vector2(1, 1)
					cr.position = Vector2(-400, -400); cr.size = Vector2(2200, 1600)
				"camera-panned-to-1000-500":
					cam.position = Vector2(1000, 500); cam.zoom = Vector2(1, 1)
					cr.position = Vector2(-400, -400); cr.size = Vector2(2400, 1600)
				"camera-zoom-2":
					cam.position = Vector2(640, 360); cam.zoom = Vector2(2, 2)
					cr.position = Vector2(-400, -400); cr.size = Vector2(2200, 1600)
				"rect-rotated-20-deg":
					cam.position = Vector2(640, 360); cam.zoom = Vector2(1, 1)
					cr.position = Vector2(640, 360) - Vector2(1600, 1200) * 0.5; cr.size = Vector2(1600, 1200)
					cr.pivot_offset = Vector2(800, 600); cr.rotation = deg_to_rad(20.0)
				"window-stretched-2x":
					cam.position = Vector2(320, 180); cam.zoom = Vector2(1, 1)
					cr.position = Vector2(-200, -200); cr.size = Vector2(1100, 800)
					root.content_scale_size = Vector2i(640, 360)
					root.content_scale_mode = Window.CONTENT_SCALE_MODE_CANVAS_ITEMS
					root.content_scale_aspect = Window.CONTENT_SCALE_ASPECT_KEEP
					await lib.frames(4)
			root.add_child(cr)
			await lib.frames(3)
			var img := grab()
			var d := grid_diff(img, gradient_expect)
			d["image_size"] = [img.get_width(), img.get_height()]
			res_setup[key] = d
			cr.queue_free()
			await lib.frames(2)
			if setup == "window-stretched-2x":
				root.content_scale_mode = Window.CONTENT_SCALE_MODE_DISABLED
				root.content_scale_size = Vector2i(0, 0)
				await lib.frames(4)
		results[setup] = res_setup
	cam.zoom = Vector2(1, 1)
	cam.position = Vector2(640, 360)
	lib.out("F1-four-ways-against-the-exact-screen-gradient", results)

	# ---------------- A1 stripes
	var blob256: Texture2D = Scn.blob_texture(256)
	var shaders := ["15-anchor-local.gdshader", "16-anchor-world.gdshader", "17-anchor-screen.gdshader"]
	var sprites: Array = []
	for i in 3:
		var s := Scn.sprite(blob256, Vector2(256 + 384 * i, 360), 1.0, Scn.material(shaders[i]))   # x = 256, 640, 1024: multiples of 64, so the three stripe patterns coincide at the start
		root.add_child(s)
		sprites.append(s)
	await lib.frames(4)
	var states := {}
	states["start"] = _stripe_rows(sprites, cam)
	grab().save_png(out_dir + "anchors-start.png")
	for s in sprites:
		s.position.x += 160
	await lib.frames(3)
	states["after_slide_right_160"] = _stripe_rows(sprites, cam)
	grab().save_png(out_dir + "anchors-after-slide.png")
	for s in sprites:
		s.position.x -= 160
	cam.position.x += 160
	await lib.frames(3)
	states["after_camera_pan_right_160"] = _stripe_rows(sprites, cam)
	grab().save_png(out_dir + "anchors-after-pan.png")
	# compare: for each sprite compare the on/off pattern along the midline (x from -70 to +70 around the sprite's screen x)
	var cmp := {}
	for i in 3:
		var nm: String = ["local", "world", "screen"][i]
		var st: String = states["start"][i]
		var sl: String = states["after_slide_right_160"][i]
		var pn: String = states["after_camera_pan_right_160"][i]
		cmp[nm] = {"pattern_start": st, "pattern_after_slide": sl, "pattern_after_pan": pn,
			"slide_keeps_pattern_relative_to_sprite": st == sl, "pan_keeps_pattern_relative_to_sprite": st == pn}
	lib.out("A1-three-anchors-slide-then-pan", cmp)
	for s in sprites:
		s.queue_free()
	cam.position = Vector2(640, 360)
	await lib.frames(3)

	# ---------------- T1 texture pixel size
	var chk: Texture2D = Scn.checker_texture(256)
	var a_art := Scn.sprite(Scn.blob_texture(128), Vector2(400, 360), 2.0, Scn.material("07-pattern-texel-size.gdshader", {"pattern": chk}))
	var b_art := Scn.sprite(Scn.blob_texture(64), Vector2(880, 360), 4.0, Scn.material("07-pattern-texel-size.gdshader", {"pattern": chk}))
	root.add_child(a_art)
	root.add_child(b_art)
	await lib.frames(4)
	var img_t := grab()
	var runs := {}
	for pair in [["A_128px_art", 400], ["B_64px_art", 880]]:
		var transitions := 0
		var prev := ""
		var first_x := -1
		var last_x := -1
		for x in range(pair[1] - 70, pair[1] + 71):
			var c := img_t.get_pixel(x, 360)
			var cls := "cream" if c.r > 0.9 else "teal"
			if prev != "" and cls != prev:
				transitions += 1
				if first_x < 0:
					first_x = x
				last_x = x
			prev = cls
		runs[pair[0]] = {"colour_changes_along_140_pixels": transitions}
	lib.out("T1-texture-pixel-size-changes-the-pattern-with-the-art", runs)
	grab().save_png(out_dir + "texel-size.png")
	a_art.queue_free()
	b_art.queue_free()
	await lib.frames(2)

	# ---------------- H1 hole (radius 60 at (640,360); the blob at (640,360) is 154 px across, so a ring of blob shows round the hole)
	var sp := Scn.sprite(Scn.blob_texture(256), Vector2(640, 360), 1.0, Scn.material("08-world-hole.gdshader"))
	root.add_child(sp)
	await lib.frames(4)
	var img_h := grab()
	var inside := img_h.get_pixel(640, 360)
	var edge_in := img_h.get_pixel(640 - 59, 360)
	var edge_out := img_h.get_pixel(640 - 61, 360)
	lib.out("H1-hole", {"centre_rgb": [roundi(inside.r * 255), roundi(inside.g * 255), roundi(inside.b * 255)], "59_left_of_centre_rgb": [roundi(edge_in.r * 255), roundi(edge_in.g * 255), roundi(edge_in.b * 255)],
		"61_left_of_centre_rgb": [roundi(edge_out.r * 255), roundi(edge_out.g * 255), roundi(edge_out.b * 255)], "stage_rgb": [217, 213, 202], "teal_rgb": [95, 163, 145],
		"note": "inside the radius the pixel is thrown away (stage colour); two pixels further out the sprite's teal shows"})
	sp.position.x = 560
	await lib.frames(3)
	grab().save_png(out_dir + "hole-partial.png")
	quit(0)


# the on/off pattern along the midline of each sprite, from x_screen - 70 to + 70 (white stripe = "1", anything else "0")
func _stripe_rows(sprites: Array, cam: Camera2D) -> Array:
	var img := grab()
	var rows: Array = []
	for s in sprites:
		var screen_x := int((s.position.x - cam.position.x) + 640.0)
		var bits := ""
		for dx in range(-70, 71, 2):
			var c := img.get_pixel(screen_x + dx, 360)
			bits += "1" if (c.r > 0.97 and c.g > 0.97 and c.b > 0.97) else "0"
		rows.append(bits)
	return rows

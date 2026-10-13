extends SceneTree
# verify13.gd: the four window-pixel shaders of C10 (10, 12, 13, 14) through the OTHER capture route, for the record.
# The series rule (GLOSSARY.md "Series conventions", COMPONENT-SPECS.md "Capture harness", 2026-10-13) says shaders that read window pixels are captured
# at the size they are shown, 1920 x 1080 at scale 1, because the 3x SubViewport route changes the numbers they read. C10 therefore uses the 1920 x 1080
# route (verify12.gd). This script measures what the 3x route (a 3840 x 2160 SubViewport over a 1280 x 720 canvas) would have given for the same four
# shaders, so the film can say what it did and why, with numbers:
#   A  the four shaders read through the 3x route: raw pixel readings (x3) and the gradient they paint (a fraction, so unchanged)
#   B  the same four-tile arrangement at 1920 x 1080 scale 1 (a SubViewport of 1920 x 1080, no override): the raw pixel readings are the window's own
# Run: godot --path <project dir> --script res://verify13.gd

const Lib := preload("res://probe_lib.gd")
const Scn := preload("res://scenes_lib.gd")
var lib


func _initialize() -> void:
	call_deferred("run")


func worst_vs_gradient(img: Image, skip_seams: bool) -> Array:
	var w := img.get_width()
	var h := img.get_height()
	var worst := 0
	var n := 0
	for gy in range(9):
		for gx in range(16):
			var x := int((gx + 0.5) * w / 16.0)
			var y := int((gy + 0.5) * h / 9.0)
			if skip_seams and (absi(y - h / 2) < 6 or absi(x - w / 2) < 6):
				continue
			var c: Color = img.get_pixel(x, y)
			var e := Color((x + 0.5) / float(w), (y + 0.5) / float(h), 0.8)
			var d := maxi(maxi(absi(roundi(c.r * 255.0) - roundi(e.r * 255.0)), absi(roundi(c.g * 255.0) - roundi(e.g * 255.0))), absi(roundi(c.b * 255.0) - roundi(e.b * 255.0)))
			worst = maxi(worst, d)
			n += 1
	return [worst, n]


func four_tiles(host: Node, canvas: Vector2) -> void:
	var files := ["10-screen-via-matrices.gdshader", "12-screen-vertex-in-fragment.gdshader", "13-screen-fragcoord.gdshader", "14-screen-uv.gdshader"]
	var hw := canvas.x / 2.0
	var hh := canvas.y / 2.0
	var rects := [Rect2(0, 0, hw, hh), Rect2(hw, 0, hw, hh), Rect2(0, hh, hw, hh), Rect2(hw, hh, hw, hh)]
	for i in 4:
		var cr := ColorRect.new()
		cr.position = rects[i].position
		cr.size = rects[i].size
		cr.color = Color("#BDB8AA")
		cr.material = Scn.material(files[i])
		host.add_child(cr)


func run() -> void:
	lib = Lib.new(self)
	RenderingServer.set_default_clear_color(Scn.STAGE)
	root.size = Vector2i(1280, 720)
	await lib.frames(3)

	# ---- A: the 3x route
	var sub := SubViewport.new()
	sub.size = Vector2i(3840, 2160)
	sub.size_2d_override = Vector2i(1280, 720)
	sub.size_2d_override_stretch = true
	sub.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(sub)
	four_tiles(sub, Vector2(1280, 720))
	await lib.frames(5)
	var imgA: Image = sub.get_texture().get_image()
	var wa := worst_vs_gradient(imgA, false)
	# the raw pixel numbers the three window-pixel shaders read at the logical pixel (286, 236) are in verify8.gd R1 (858, 708: three times); here only the painting
	lib.out("A-3x-route-four-tiles-final-frame-against-the-exact-gradient", {"image_size": [imgA.get_width(), imgA.get_height()], "samples": wa[1], "worst_8bit_difference": wa[0],
		"note": "the shaders multiply a pixel count by SCREEN_PIXEL_SIZE, so both scale by 3 and the painted fraction is unchanged; the raw counts are verify8.gd R1 (858, 708 for the logical pixel 286, 236)"})
	sub.queue_free()
	await lib.frames(3)

	# ---- B: 1920 x 1080 at scale 1
	var sub2 := SubViewport.new()
	sub2.size = Vector2i(1920, 1080)
	sub2.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(sub2)
	four_tiles(sub2, Vector2(1920, 1080))
	await lib.frames(5)
	var imgB: Image = sub2.get_texture().get_image()
	var wb := worst_vs_gradient(imgB, false)
	lib.out("B-1920x1080-scale-1-four-tiles-final-frame-against-the-exact-gradient", {"image_size": [imgB.get_width(), imgB.get_height()], "samples": wb[1], "worst_8bit_difference": wb[0]})

	# the raw readings of the window-pixel built-ins at the corner pixel of a 128 px sprite, the 1920 x 1080 route (the window's own pixels): use the encoder probe
	var mat: ShaderMaterial = lib.make_enc_material()
	var spr := Sprite2D.new()
	spr.texture = lib.white_texture(128)
	spr.position = Vector2(900, 600)
	spr.material = mat
	sub2.add_child(spr)
	await lib.frames(5)
	var px := 900 - 64 + 2
	var py := 600 - 64 + 2
	var rr := {"pixel_probed_in_the_1920_by_1080_image": [px, py]}
	for item in [[6, "VERTEX_in_fragment.x", 1.0], [8, "FRAGCOORD.x", 1.0], [10, "SCREEN_UV.x_x50000", 50000.0], [12, "SCREEN_PIXEL_SIZE.x_x1e6", 1000000.0]]:
		mat.set_shader_parameter("which", item[0])
		mat.set_shader_parameter("scale", item[2])
		await lib.frames(3)
		var img: Image = sub2.get_texture().get_image()
		rr[item[1]] = lib.decode(img.get_pixel(px, py), item[2])
	lib.out("B2-1920x1080-scale-1-raw-readings-at-one-pixel", rr)
	quit(0)

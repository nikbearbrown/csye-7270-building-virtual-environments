extends SceneTree
# verify8.gd: the capture route and two capture scenes.
#   R1  the 4K capture route (a 3840 x 2160 SubViewport over a 1280 x 720 logical canvas): world and local numbers stay logical,
#       screen-pixel built-ins count 4K pixels (3x), screen U V and the screen-fraction shaders do not change
#   S6  the four-tile scene (C10): four 640 x 360 ColorRects with shaders 10, 12, 13, 14 switched on in turn; the final frame equals the exact gradient
#   S5  the hole scene (C08) with its thin grey ring: a frame to look at
# Run: godot --path <project dir> --script res://verify8.gd

const Lib := preload("res://probe_lib.gd")
const Scn := preload("res://scenes_lib.gd")
var lib
var out_dir := "/private/tmp/claude-501/godot-shaders-local-world-and-screen-space/scratch/out/"


func _initialize() -> void:
	call_deferred("run")


func run() -> void:
	lib = Lib.new(self)
	RenderingServer.set_default_clear_color(Scn.STAGE)
	root.size = Vector2i(1280, 720)
	await lib.frames(3)

	# ---------------- R1: the 4K route
	var sub := SubViewport.new()
	sub.size = Vector2i(3840, 2160)
	sub.size_2d_override = Vector2i(1280, 720)
	sub.size_2d_override_stretch = true
	sub.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(sub)
	var mat: ShaderMaterial = lib.make_enc_material()
	var spr := Sprite2D.new()
	spr.texture = lib.white_texture(128)
	spr.position = Vector2(600, 400)
	spr.material = mat
	sub.add_child(spr)
	var cam := Camera2D.new()
	cam.position = Vector2(890, 460)
	sub.add_child(cam)
	cam.make_current()
	await lib.frames(5)
	var px := 858   # logical (286, 236) * 3
	var py := 708
	var r := {"subviewport": [sub.size.x, sub.size.y], "logical_canvas": [1280, 720], "canvas_transform_origin": [sub.get_canvas_transform().origin.x, sub.get_canvas_transform().origin.y],
		"final_transform_scale": sub.get_final_transform().x.x}
	for item in [[0, "local.x", 1.0], [1, "local.y", 1.0], [2, "world.x", 1.0], [3, "world.y", 1.0], [4, "screen_by_matrices.x", 1.0], [5, "screen_by_matrices.y", 1.0],
			[6, "VERTEX_in_fragment.x", 1.0], [8, "FRAGCOORD.x", 1.0], [10, "SCREEN_UV.x_x50000", 50000.0], [12, "SCREEN_PIXEL_SIZE.x_x1e6", 1000000.0]]:
		mat.set_shader_parameter("which", item[0])
		mat.set_shader_parameter("scale", item[2])
		await lib.frames(3)
		var img: Image = sub.get_texture().get_image()
		r[item[1]] = lib.decode(img.get_pixel(px, py), item[2])
	lib.out("R1-4K-route-subviewport-over-a-1280x720-canvas", r)
	sub.queue_free()
	await lib.frames(3)

	# ---------------- S6: four tiles
	var tiles: Array = []
	var files := ["10-screen-via-matrices.gdshader", "12-screen-vertex-in-fragment.gdshader", "13-screen-fragcoord.gdshader", "14-screen-uv.gdshader"]
	var rects := [Rect2(0, 0, 640, 360), Rect2(640, 0, 640, 360), Rect2(0, 360, 640, 360), Rect2(640, 360, 640, 360)]
	for i in 4:
		var cr := ColorRect.new()
		cr.position = rects[i].position
		cr.size = rects[i].size
		cr.color = Color("#BDB8AA")
		root.add_child(cr)
		tiles.append(cr)
	await lib.frames(3)
	lib.grab().save_png(out_dir + "four-tiles-0-flat.png")
	for i in 4:
		tiles[i].material = Scn.material(files[i])
		await lib.frames(3)
		if i == 1:
			lib.grab().save_png(out_dir + "four-tiles-2-of-4.png")
	var img_f: Image = lib.grab()
	img_f.save_png(out_dir + "four-tiles-4-of-4.png")
	var worst := 0
	var n := 0
	for gy in range(9):
		for gx in range(16):
			var x := int((gx + 0.5) * 1280 / 16.0)
			var y := int((gy + 0.5) * 720 / 9.0)
			var c: Color = img_f.get_pixel(x, y)
			var e := Color((x + 0.5) / 1280.0, (y + 0.5) / 720.0, 0.8)
			var d := maxi(maxi(absi(roundi(c.r * 255.0) - roundi(e.r * 255.0)), absi(roundi(c.g * 255.0) - roundi(e.g * 255.0))), absi(roundi(c.b * 255.0) - roundi(e.b * 255.0)))
			worst = maxi(worst, d)
			n += 1
	# the pixels either side of the two seams
	var seams := {}
	for sp in [[639, 100], [640, 100], [300, 359], [300, 360], [900, 359], [900, 360]]:
		var c2: Color = img_f.get_pixel(sp[0], sp[1])
		seams["%d,%d" % [sp[0], sp[1]]] = [roundi(c2.r * 255), roundi(c2.g * 255), roundi(c2.b * 255)]
	lib.out("S6-four-tiles-final-frame-against-the-exact-gradient", {"samples": n, "worst_8bit_difference": worst, "pixels_either_side_of_the_seams": seams})
	for t in tiles:
		t.queue_free()
	await lib.frames(2)

	# ---------------- S5: hole with a ring
	var ring := Node2D.new()
	root.add_child(ring)
	ring.draw.connect(func(): ring.draw_arc(Vector2(640, 360), 60.0, 0.0, TAU, 96, Color("#8F8A7B"), 3.0, true))
	ring.queue_redraw()
	var sp5 := Scn.sprite(Scn.blob_texture(256), Vector2(600, 360), 1.0, Scn.material("08-world-hole.gdshader"))
	root.add_child(sp5)
	await lib.frames(4)
	lib.grab().save_png(out_dir + "hole-with-ring.png")
	quit(0)

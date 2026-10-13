extends SceneTree
# Claim checked: the same shader file draws a different picture on a different mesh, because UV comes from the mesh.
#   The pad shader (lab-shaders/12-signal-pad.gdshader) is drawn on (a) a flat QuadMesh and (b) the thin BoxMesh the pad uses in its game.
#   Counted: how many stripe bands cross each surface. Also saves the angled "game camera" picture of both, side by side.
# Run:  godot --path <project dir> --script res://verify2-pad-on-quad-and-box.gd          (Forward+)
const SHADER_PATH := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shaders-in-3d/lab-shaders/12-signal-pad.gdshader"
const PNG_DIR := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shaders-in-3d/evidence/planning-checks/png/"

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func make_mat(activation: float) -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = FileAccess.get_file_as_string(SHADER_PATH)
	var m := ShaderMaterial.new()
	m.shader = sh
	m.set_shader_parameter("activation", activation)
	return m

# Count how many bands a horizontal scan line crosses between x0 and x1: a band edge is a jump in the red channel bigger than half
# the dark/light gap (at activation 0 the gap is about 0.075).
func count_bands(img: Image, y: int, x0: int, x1: int) -> int:
	var bands := 1
	var prev := img.get_pixel(x0, y).r
	var level := 0   # 0 = near the first value
	var first := prev
	for x in range(x0 + 1, x1):
		var v := img.get_pixel(x, y).r
		if absf(v - prev) > 0.03:
			bands += 1
		prev = v
	return bands

func run() -> void:
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	root.size = Vector2i(1280, 720)
	var stage := Node3D.new()
	root.add_child(stage)
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	stage.add_child(cam)
	cam.current = true
	var mi := MeshInstance3D.new()
	stage.add_child(mi)
	mi.material_override = make_mat(0.0)

	# (a) flat quad, seen from the front, 2.4 x 2.4 world units, camera size 3.0 (full height)
	var q := QuadMesh.new()
	q.size = Vector2(2.4, 2.4)
	mi.mesh = q
	cam.size = 3.0
	cam.position = Vector3(0, 0, 4)
	cam.rotation_degrees = Vector3.ZERO
	for i in range(4): await process_frame
	RenderingServer.force_draw(false)
	var img := root.get_texture().get_image()
	var ppu := img.get_height() / 3.0
	var cx := img.get_width() / 2
	var cy := img.get_height() / 2
	var half := int(1.2 * ppu)
	var bands_quad := count_bands(img, cy, cx - half + 4, cx + half - 4)
	img.save_png(PNG_DIR + "pad-quad-front-activation0.png")

	# (b) thin box (the pad's size in its game), seen from straight above
	var b := BoxMesh.new()
	b.size = Vector3(1.55, 0.10, 1.55)
	mi.mesh = b
	cam.position = Vector3(0, 4, 0)
	cam.rotation_degrees = Vector3(-90, 0, 0)
	cam.size = 2.0
	for i in range(4): await process_frame
	RenderingServer.force_draw(false)
	img = root.get_texture().get_image()
	var ppu2 := img.get_height() / 2.0
	var half2 := int(1.55 / 2.0 * ppu2)
	# scan across the TOP face only: stay clear of the box edges by a few pixels
	var bands_box := count_bands(img, cy, cx - half2 + 4, cx + half2 - 4)
	img.save_png(PNG_DIR + "pad-box-top-activation0.png")
	out("A-stripe-bands", {"renderer": RenderingServer.get_current_rendering_method(), "activation": 0.0, "bands_across_flat_quad": bands_quad, "bands_across_box_top": bands_box,
		"expected": "quad: 16 bands (8 dark + 8 light). box top: UV x covers 1/3 of the map, 8/3 = 2.67 periods, so about 6 bands"})

	# (c) the angled picture used in the film: both meshes, game camera direction, three activations
	mi.queue_free()
	var box := MeshInstance3D.new()
	box.mesh = b
	box.position = Vector3(-1.1, 0, 0)
	stage.add_child(box)
	var quad := MeshInstance3D.new()
	var q2 := QuadMesh.new()
	q2.size = Vector2(1.55, 1.55)
	quad.mesh = q2
	quad.position = Vector3(1.1, 0, 0)
	quad.rotation_degrees = Vector3(-90, 0, 0)    # lay it flat, like the pad's top face (a QuadMesh stands up by default)
	stage.add_child(quad)
	cam.size = 4.2
	cam.position = Vector3(5.8, 9, 11).normalized() * 12.0
	cam.rotation_degrees = Vector3.ZERO
	cam.look_at(Vector3.ZERO)
	for a in [0.0, 0.5, 1.0]:
		var m := make_mat(a)
		box.material_override = m
		quad.material_override = m
		for i in range(4): await process_frame
		RenderingServer.force_draw(false)
		root.get_texture().get_image().save_png(PNG_DIR + "pad-box-and-quad-angled-activation%s.png" % str(a))
	out("B-angled-pictures", {"saved": ["pad-box-and-quad-angled-activation0.0.png", "pad-box-and-quad-angled-activation0.5.png", "pad-box-and-quad-angled-activation1.0.png"], "camera": "orthographic, size 4.2, from (5.8, 9, 11) looking at the origin (the direction the game's own camera uses)"})
	quit(0)

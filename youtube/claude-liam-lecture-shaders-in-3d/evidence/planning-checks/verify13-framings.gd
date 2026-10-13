extends SceneTree
# Claim checked (CAPTURE-PLAN.md, camera sizes): the capture framings the plan names keep every object in frame and fill a useful part of it.
# For each capture the same objects, spacing and orthographic camera size as the plan are built at 1280 x 720, and the bounding box of every
# non-stage pixel is printed as fractions of the frame (x0, x1, y0, y1). The captures themselves (30 fps, 3840 x 2160) are not made here.
#   C03 one sphere, size 1.8       C04 two spheres, 2.4       C05 three spheres, 2.8       C06 two squares at yaw 35, 2.4
#   C02 square, box, sphere swinging to -50, 0 and +50 degrees, size 2.6       C18 two squares (one red), 2.6
#   C07 / S5 one face-on square 1.8, size 2.0       C14 the thin box and the flat square under the pad shader, size 4.2 (the first plan) against 3.2 (the plan now)
# A contact sheet of the first six is saved as png/framing-sheet.png. Scripted placement; a planning check, not a shot in the film.
# Run:  ./run-script.sh verify13-framings.gd run-13-framings.log
const LAB := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shaders-in-3d/lab-shaders/"
const PNG_DIR := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-shaders-in-3d/evidence/planning-checks/png/"
const STAGE := Color("#D9D5CA")

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func mat(file: String) -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = FileAccess.get_file_as_string(LAB + file)
	var m := ShaderMaterial.new()
	m.shader = sh
	return m

func sphere(file: String, x: float) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	mi.mesh = SphereMesh.new()
	mi.material_override = mat(file)
	mi.position = Vector3(x, 0, 0)
	return mi

func quad(file: String, x: float, size: float) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	var q := QuadMesh.new()
	q.size = Vector2(size, size)
	mi.mesh = q
	mi.material_override = mat(file)
	mi.position = Vector3(x, 0, 0)
	return mi

func setup(size: float, with_light: bool) -> Node3D:
	var stage := Node3D.new()
	root.add_child(stage)
	if with_light:
		var env := Environment.new()
		env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
		env.ambient_light_color = Color.WHITE
		env.ambient_light_energy = 0.25
		var we := WorldEnvironment.new()
		we.environment = env
		stage.add_child(we)
		var lamp := DirectionalLight3D.new()
		lamp.rotation_degrees = Vector3(-30, -65, 0)
		stage.add_child(lamp)
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = size
	cam.position = Vector3(0, 0, 5)
	stage.add_child(cam)
	cam.current = true
	return stage

func shot() -> Image:
	for i in range(4): await process_frame
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func bbox(img: Image) -> Dictionary:
	var minx := 9999; var maxx := -1; var miny := 9999; var maxy := -1
	for y in range(0, img.get_height(), 2):
		for x in range(0, img.get_width(), 2):
			var c := img.get_pixel(x, y)
			if absf(c.r - STAGE.r) + absf(c.g - STAGE.g) + absf(c.b - STAGE.b) > 0.05:
				minx = mini(minx, x); maxx = maxi(maxx, x); miny = mini(miny, y); maxy = maxi(maxy, y)
	var w := float(img.get_width()); var h := float(img.get_height())
	return {"x": [snappedf(minx / w, 0.01), snappedf(maxx / w, 0.01)], "y": [snappedf(miny / h, 0.01), snappedf(maxy / h, 0.01)]}

func run() -> void:
	RenderingServer.set_default_clear_color(STAGE)
	root.size = Vector2i(1280, 720)
	var imgs := []
	var rows := []
	var s := setup(1.8, true); s.add_child(sphere("02-flat-teal-3d.gdshader", 0.0))
	var img := await shot(); imgs.append(img); rows.append({"capture": "C03 one sphere, size 1.8", "fill": bbox(img)}); s.queue_free(); await process_frame
	s = setup(2.4, true); s.add_child(sphere("02-flat-teal-3d.gdshader", -0.7)); s.add_child(sphere("07-flat-teal-3d-unshaded.gdshader", 0.7))
	img = await shot(); imgs.append(img); rows.append({"capture": "C04 two spheres at -0.7 and +0.7, size 2.4", "fill": bbox(img)}); s.queue_free(); await process_frame
	s = setup(2.8, true); s.add_child(sphere("02-flat-teal-3d.gdshader", -1.15)); s.add_child(sphere("07-flat-teal-3d-unshaded.gdshader", 0.0)); s.add_child(sphere("08-flat-teal-3d-empty-light.gdshader", 1.15))
	img = await shot(); imgs.append(img); rows.append({"capture": "C05 three spheres at -1.15, 0, +1.15, size 2.8", "fill": bbox(img)}); s.queue_free(); await process_frame
	s = setup(2.4, false)
	var a := quad("07-flat-teal-3d-unshaded.gdshader", -0.85, 1.2); var b := quad("09-two-sided.gdshader", 0.85, 1.2)
	s.add_child(a); s.add_child(b); a.rotation_degrees = Vector3(0, 35, 0); b.rotation_degrees = Vector3(0, 35, 0)
	img = await shot(); imgs.append(img); rows.append({"capture": "C06 two squares at -0.85 and +0.85, yaw 35, size 2.4", "fill": bbox(img)}); s.queue_free(); await process_frame
	for yaw in [-50.0, 0.0, 50.0]:
		s = setup(2.6, false)
		var q := quad("06-uv-colors-3d.gdshader", -1.35, 1.0)
		var bx := MeshInstance3D.new(); bx.mesh = BoxMesh.new(); bx.material_override = mat("06-uv-colors-3d.gdshader"); bx.position = Vector3(0, 0, 0)
		var sp := sphere("06-uv-colors-3d.gdshader", 1.35)
		s.add_child(q); s.add_child(bx); s.add_child(sp)
		for n in [q, bx, sp]: n.rotation_degrees = Vector3(-20, yaw, 0)
		img = await shot()
		if yaw == 50.0: imgs.append(img)
		rows.append({"capture": "C02 square at -1.35, box at 0, sphere at +1.35, tilt -20, yaw %d, size 2.6" % int(yaw), "fill": bbox(img)}); s.queue_free(); await process_frame
	s = setup(2.6, false); s.add_child(quad("07-flat-teal-3d-unshaded.gdshader", -0.95, 1.4)); s.add_child(quad("19-three-d-shader-on-a-mesh.gdshader", 0.95, 1.4))
	img = await shot(); imgs.append(img); rows.append({"capture": "C18 two squares at -0.95 and +0.95 (right one red), size 2.6", "fill": bbox(img)}); s.queue_free(); await process_frame
	# C07 and the S5 clips: one face-on square 1.8 x 1.8
	s = setup(2.0, false); s.add_child(quad("06-uv-colors-3d.gdshader", 0.0, 1.8))
	img = await shot(); rows.append({"capture": "C07 / S5 one face-on square 1.8, size 2.0", "fill": bbox(img)}); s.queue_free(); await process_frame
	# C14: the thin box and the flat square under the pad shader, seen from the game's direction
	for sz in [4.2, 3.2]:
		var stage := Node3D.new(); root.add_child(stage)
		var pm := mat("12-signal-pad.gdshader"); pm.set_shader_parameter("activation", 0.3)
		var bm := MeshInstance3D.new(); var boxm := BoxMesh.new(); boxm.size = Vector3(1.55, 0.10, 1.55); bm.mesh = boxm; bm.material_override = pm; bm.position = Vector3(-1.1, 0, 0); stage.add_child(bm)
		var qm := MeshInstance3D.new(); var quadm := QuadMesh.new(); quadm.size = Vector2(1.55, 1.55); qm.mesh = quadm; qm.rotation_degrees = Vector3(-90, 0, 0); qm.material_override = pm; qm.position = Vector3(1.1, 0, 0); stage.add_child(qm)
		var cam := Camera3D.new(); cam.projection = Camera3D.PROJECTION_ORTHOGONAL; cam.size = sz
		cam.position = Vector3(5.8, 9, 11).normalized() * 12.0; stage.add_child(cam); cam.look_at(Vector3.ZERO); cam.current = true
		img = await shot()
		rows.append({"capture": "C14 thin box at -1.1 and flat square at +1.1 under the pad shader (activation 0.3), size %.1f" % sz, "fill": bbox(img)})
		stage.queue_free(); await process_frame
	var sheet := Image.create(1280, 480, false, Image.FORMAT_RGB8)
	for i in range(imgs.size()):
		var small: Image = imgs[i].duplicate(); small.resize(427, 240)
		sheet.blit_rect(small, Rect2i(0, 0, 427, 240), Vector2i((i % 3) * 427, (i / 3) * 240))
	sheet.save_png(PNG_DIR + "framing-sheet.png")
	out("framings", {"renderer": RenderingServer.get_current_rendering_method(), "frame": "1280 x 720", "rows": rows})
	quit(0)

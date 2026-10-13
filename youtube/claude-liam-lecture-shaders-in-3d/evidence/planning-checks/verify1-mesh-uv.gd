extends SceneTree
# Claims checked (Shaders in 3D):
#   - a QuadMesh has four vertices; each vertex carries a UV address; the four addresses are the corners of the 0..1 square
#   - a BoxMesh lays its UV map out as 3 x 2 cells, one per face (docs: "arranged in a 3×2 layout")
#   - a SphereMesh wraps U around itself
#   - what the shader sees on screen matches the mesh data: the QuadMesh corners seen from the front (top-left = 0,0),
#     the top face of the pad-sized box, and U at the front of a turning sphere
# Run:  godot --path <project dir> --script res://verify1-mesh-uv.gd          (Forward+, the default renderer)
# In Forward+ an unshaded ALBEDO is encoded for the screen, so rendered values are decoded with Color.srgb_to_linear()
# before they are read as UV. The mesh-array part needs no renderer at all.

const UVSHADER := "shader_type spatial;\nrender_mode unshaded;\nvoid fragment() { ALBEDO = vec3(UV.x, UV.y, 0.0); }\n"

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func r3(v: float) -> float:
	return snappedf(v, 0.001)

func uv_stats(mesh: Mesh) -> Dictionary:
	var arrays := mesh.surface_get_arrays(0)
	var verts: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
	var uvs: PackedVector2Array = arrays[Mesh.ARRAY_TEX_UV]
	var umin := 9.0
	var umax := -9.0
	var vmin := 9.0
	var vmax := -9.0
	for u in uvs:
		umin = minf(umin, u.x); umax = maxf(umax, u.x); vmin = minf(vmin, u.y); vmax = maxf(vmax, u.y)
	return {"vertices": verts.size(), "uv_count": uvs.size(), "u_range": [r3(umin), r3(umax)], "v_range": [r3(vmin), r3(vmax)]}

func decode(c: Color) -> Array:
	var l := c
	if RenderingServer.get_current_rendering_method() != "gl_compatibility":
		l = c.srgb_to_linear()
	return [r3(l.r), r3(l.g)]

func mat() -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = UVSHADER
	var m := ShaderMaterial.new()
	m.shader = sh
	return m

func run() -> void:
	# ---- 1. mesh data: no renderer involved
	var quad := QuadMesh.new()
	var qa := quad.surface_get_arrays(0)
	var quad_pairs := []
	for i in range((qa[Mesh.ARRAY_VERTEX] as PackedVector3Array).size()):
		var p: Vector3 = qa[Mesh.ARRAY_VERTEX][i]
		var u: Vector2 = qa[Mesh.ARRAY_TEX_UV][i]
		quad_pairs.append({"vertex": [r3(p.x), r3(p.y)], "uv": [r3(u.x), r3(u.y)]})
	out("1a-quad-vertices-carry-uv", {"stats": uv_stats(quad), "vertex_and_uv": quad_pairs, "reading": "four vertices; the corner at the top-left of the face (x -0.5, y +0.5 seen from the front) carries UV (0,0)"})

	var box := BoxMesh.new()
	box.size = Vector3(1, 1, 1)
	var ba := box.surface_get_arrays(0)
	var faces := {}
	for i in range((ba[Mesh.ARRAY_VERTEX] as PackedVector3Array).size()):
		var n: Vector3 = ba[Mesh.ARRAY_NORMAL][i]
		var key := "%d,%d,%d" % [int(round(n.x)), int(round(n.y)), int(round(n.z))]
		var u: Vector2 = ba[Mesh.ARRAY_TEX_UV][i]
		if not faces.has(key):
			faces[key] = {"umin": 9.0, "umax": -9.0, "vmin": 9.0, "vmax": -9.0, "n": 0}
		var f: Dictionary = faces[key]
		f["umin"] = minf(f["umin"], u.x); f["umax"] = maxf(f["umax"], u.x); f["vmin"] = minf(f["vmin"], u.y); f["vmax"] = maxf(f["vmax"], u.y); f["n"] += 1
	var face_rows := {}
	for k in faces:
		var f2: Dictionary = faces[k]
		face_rows[k] = {"vertices": f2["n"], "u": [r3(f2["umin"]), r3(f2["umax"])], "v": [r3(f2["vmin"]), r3(f2["vmax"])]}
	out("1b-box-uv-layout", {"stats": uv_stats(box), "faces_by_normal(x,y,z)": face_rows, "reading": "six faces of four vertices; every face owns one cell of a 3 x 2 grid (u in thirds, v in halves)"})

	var sphere := SphereMesh.new()
	out("1c-sphere", {"stats": uv_stats(sphere), "reading": "U runs 0..1 once around the equator"})

	# ---- 2. what the screen shows
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	root.size = Vector2i(640, 360)
	var stage := Node3D.new()
	root.add_child(stage)
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = 2.0
	cam.position = Vector3(0, 0, 3)
	stage.add_child(cam)
	cam.current = true

	# quad seen from the front (a 2 x 2 quad fills the 2-unit-high view; probes near its corners)
	var mi := MeshInstance3D.new()
	var q2 := QuadMesh.new()
	q2.size = Vector2(1.8, 1.8)
	mi.mesh = q2
	mi.material_override = mat()
	stage.add_child(mi)
	for i in range(4): await process_frame
	RenderingServer.force_draw(false)
	var img := root.get_texture().get_image()
	var ppu := img.get_height() / 2.0
	var cx := img.get_width() / 2.0
	var cy := img.get_height() / 2.0
	var half := 0.9 * ppu
	var corners := {}
	for name in ["top-left", "top-right", "bottom-left", "bottom-right"]:
		var sx := -1.0 if name.ends_with("left") else 1.0
		var sy := -1.0 if name.begins_with("top") else 1.0
		var c := img.get_pixel(int(cx + sx * (half - 3)), int(cy + sy * (half - 3)))
		corners[name] = decode(c)
	out("2a-quad-corners-on-screen", {"renderer": RenderingServer.get_current_rendering_method(), "decoded_uv": corners, "reading": "seen from the front: UV x grows to the right, UV y grows downward, top-left is (0,0), as in 2D"})

	# the box (pad-sized) seen from above: where does the TOP face sit in the map?
	mi.mesh = null
	var bx := BoxMesh.new()
	bx.size = Vector3(1.55, 0.10, 1.55)
	mi.mesh = bx
	cam.position = Vector3(0, 3, 0)
	cam.rotation_degrees = Vector3(-90, 0, 0)
	for i in range(4): await process_frame
	RenderingServer.force_draw(false)
	img = root.get_texture().get_image()
	var half_box := 1.55 / 2.0 * ppu
	var top := {}
	for name in ["screen-top-left", "screen-top-right", "screen-bottom-left", "screen-bottom-right", "centre"]:
		var sx2 := 0.0
		var sy2 := 0.0
		if name != "centre":
			sx2 = -1.0 if name.ends_with("left") else 1.0
			sy2 = -1.0 if name.begins_with("screen-top") else 1.0
		var c2 := img.get_pixel(int(cx + sx2 * (half_box - 3)), int(cy + sy2 * (half_box - 3)))
		top[name] = decode(c2)
	out("2b-box-top-face-on-screen", {"decoded_uv": top, "reading": "the top face spans about u 0.33..0.67 and v 0.5..1.0: one cell of the 3 x 2 layout, so UV x * 8.0 covers only about 2.7 stripe periods"})

	# sphere: U at the middle of the visible face as the sphere turns about the vertical axis
	cam.position = Vector3(0, 0, 3)
	cam.rotation_degrees = Vector3.ZERO
	mi.rotation_degrees = Vector3.ZERO
	mi.mesh = SphereMesh.new()
	var turn := {}
	for yaw in [0, 90, 180, 270]:
		mi.rotation_degrees = Vector3(0, yaw, 0)
		for i in range(3): await process_frame
		RenderingServer.force_draw(false)
		img = root.get_texture().get_image()
		turn[str(yaw)] = decode(img.get_pixel(int(cx), int(cy)))
	out("2c-sphere-u-as-it-turns", {"decoded_uv_at_screen_centre_by_yaw_deg": turn, "reading": "U at the centre changes by a quarter for every quarter turn: the map wraps once around the sphere"})
	quit(0)

extends SceneTree
# Claim checked (Shaders in 3D, beat B06, the one CORRECTED row): a spatial fragment() does have a COLOR, and it is a read-only input: the vertex
# color (white when a mesh has none). The brief said "there is no COLOR here".
#   A  ALBEDO = COLOR.rgb;                         on a QuadMesh (no vertex colors)        -> white
#   A2 ALBEDO = COLOR.rgb * vec3(1.0, 0.5, 0.0);   on the same QuadMesh                    -> albedo (1.0, 0.5, 0.0); Forward+ draws 0.5 as 0.737
#   B  ALBEDO = COLOR.rgb;                         on a quad whose four vertices carry the color (0.25, 0.5, 1.0) -> that color, encoded for the screen
# Writing COLOR instead fails to compile ("Constants cannot be modified."): Lab check 04 in lab-results.jsonl.
# Unshaded, so no lamp matters. Centre pixel of the render. Forward+ by default.
# Run:  ./run-script.sh verify14-color-in-spatial.gd run-14-color-in-spatial.log
const HEAD := "shader_type spatial;\nrender_mode unshaded;\nvoid fragment() {\n"

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func px(img: Image) -> Array:
	var c := img.get_pixel(img.get_width() / 2, img.get_height() / 2)
	return [snappedf(c.r, 0.001), snappedf(c.g, 0.001), snappedf(c.b, 0.001)]

func shot() -> Image:
	for i in range(4): await process_frame
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func mat(body: String) -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = HEAD + "\t" + body + "\n}\n"
	var m := ShaderMaterial.new()
	m.shader = sh
	return m

func colored_quad(c: Color) -> ArrayMesh:
	var arrays := []
	arrays.resize(Mesh.ARRAY_MAX)
	arrays[Mesh.ARRAY_VERTEX] = PackedVector3Array([Vector3(-0.6, -0.6, 0), Vector3(0.6, -0.6, 0), Vector3(0.6, 0.6, 0), Vector3(-0.6, 0.6, 0)])
	arrays[Mesh.ARRAY_COLOR] = PackedColorArray([c, c, c, c])
	arrays[Mesh.ARRAY_INDEX] = PackedInt32Array([0, 2, 1, 0, 3, 2])
	var m := ArrayMesh.new()
	m.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arrays)
	return m

func run() -> void:
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	root.size = Vector2i(320, 180)
	var stage := Node3D.new()
	root.add_child(stage)
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = 2.0
	cam.position = Vector3(0, 0, 3)
	stage.add_child(cam)
	cam.current = true
	var mi := MeshInstance3D.new()
	stage.add_child(mi)
	var q := QuadMesh.new()
	q.size = Vector2(1.2, 1.2)
	var rows := []
	mi.mesh = q
	mi.material_override = mat("ALBEDO = COLOR.rgb;")
	rows.append({"case": "A: ALBEDO = COLOR.rgb on a QuadMesh with no vertex colors", "centre": px(await shot())})
	mi.material_override = mat("ALBEDO = COLOR.rgb * vec3(1.0, 0.5, 0.0);")
	rows.append({"case": "A2: ALBEDO = COLOR.rgb * vec3(1.0, 0.5, 0.0) on the same quad", "centre": px(await shot())})
	mi.mesh = colored_quad(Color(0.25, 0.5, 1.0))
	mi.material_override = mat("ALBEDO = COLOR.rgb;")
	rows.append({"case": "B: ALBEDO = COLOR.rgb on a quad whose vertices carry the color (0.25, 0.5, 1.0)", "centre": px(await shot())})
	out("color-in-spatial", {"renderer": RenderingServer.get_current_rendering_method(), "rows": rows})
	quit(0)

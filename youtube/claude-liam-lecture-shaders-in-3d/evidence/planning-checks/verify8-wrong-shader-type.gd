extends SceneTree
# Evidence for beat B07 (first run as a side finding): what happens when a canvas_item (two-D) shader is given to a
# three-D mesh as its material override. Compared with a mesh that has no material at all and with a spatial shader that paints red.
# Result to read: does Godot print an error, and is the red drawn?
# Run:  ./run-script.sh verify8-wrong-shader-type.gd run-8-wrong-shader-type.log
const TWOD := "shader_type canvas_item;\nvoid fragment() { COLOR = vec4(1.0, 0.0, 0.0, 1.0); }\n"
const THREED := "shader_type spatial;\nrender_mode unshaded;\nvoid fragment() { ALBEDO = vec3(1.0, 0.0, 0.0); }\n"

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func frames(n: int) -> void:
	for i in range(n): await process_frame

func centre() -> Array:
	RenderingServer.force_draw(false)
	var img := root.get_texture().get_image()
	var c := img.get_pixel(img.get_width() / 2, img.get_height() / 2)
	return [snappedf(c.r, 0.001), snappedf(c.g, 0.001), snappedf(c.b, 0.001)]

func mat_of(code: String) -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = code
	var m := ShaderMaterial.new()
	m.shader = sh
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
	var q := QuadMesh.new()
	q.size = Vector2(1.6, 1.6)
	mi.mesh = q
	stage.add_child(mi)
	await frames(3)
	var none := centre()
	mi.material_override = mat_of(TWOD)
	await frames(3)
	var wrong := centre()
	mi.material_override = mat_of(THREED)
	await frames(3)
	var right := centre()
	out("wrong-type", {"renderer": RenderingServer.get_current_rendering_method(), "no_material": none, "canvas_item_shader_as_override": wrong, "spatial_shader_as_override": right,
		"reading": "if the first two are equal the two-D shader was ignored; any engine error line appears above this RESULT in the log"})
	quit(0)

extends SceneTree
# R9b follow-up probe, written for the film (checks whether the R9 "no_hint colour uniform behaves like source_color in Forward+" result is an artefact of passing a Color).
# R9 probe, written for the film. Renders flat patches of an unshaded spatial shader and reads RGB8 back.
# Four rows (same fixed ortho camera, Linear tonemap, exposure 1.0, no lights needed because unshaded):
#   const    : ALBEDO = vec3(<literal>) written into the shader source          (no uniform, no mix)
#   uniform  : uniform float v;           ALBEDO = vec3(v)                       (float uniform, no hint)
#   src_col  : uniform vec4 q : source_color;  ALBEDO = q.rgb                    (colour uniform with the hint)
#   no_hint  : uniform vec4 q;                 ALBEDO = q.rgb                    (colour uniform without the hint)
# Run: godot --path godot --rendering-method <forward_plus|gl_compatibility> --script res://course-series/tests/ev-constant-albedo-b.gd -- <outdir> <tag>  (rows here: no_hint_color, no_hint_vec4, vec3_vec3, vec3_color)
var viewport: SubViewport
var camera: Camera3D
var world: Node3D
const VALUES := [0.0585, 0.09, 0.104, 0.12, 0.16, 0.19, 0.26, 0.40, 0.52, 0.72]
const ROWS := ["no_hint_color", "no_hint_vec4", "vec3_vec3", "vec3_color"]
func _initialize() -> void: call_deferred("run")
func make_shader(row: String, v: float) -> Shader:
	var s := Shader.new()
	match row:
		"no_hint_color": s.code = "shader_type spatial;\nrender_mode unshaded;\nuniform vec4 q = vec4(0.0);\nvoid fragment() { ALBEDO = q.rgb; }"
		"no_hint_vec4": s.code = "shader_type spatial;\nrender_mode unshaded;\nuniform vec4 q = vec4(0.0);\nvoid fragment() { ALBEDO = q.rgb; }"
		"vec3_vec3": s.code = "shader_type spatial;\nrender_mode unshaded;\nuniform vec3 q = vec3(0.0);\nvoid fragment() { ALBEDO = q; }"
		"vec3_color": s.code = "shader_type spatial;\nrender_mode unshaded;\nuniform vec3 q = vec3(0.0);\nvoid fragment() { ALBEDO = q; }"
	return s
func run() -> void:
	var args := OS.get_cmdline_user_args()
	var output: String = args[0]
	var tag: String = args[1]
	viewport = SubViewport.new(); viewport.size = Vector2i(3840, 2160)
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(viewport); world = Node3D.new(); viewport.add_child(world)
	camera = Camera3D.new(); camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	camera.size = 4.0; camera.position = Vector3(0, 0, 5); world.add_child(camera); camera.make_current()
	var environment := Environment.new(); environment.background_mode = Environment.BG_COLOR
	environment.background_color = Color("14262d"); environment.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	environment.tonemap_exposure = 1.0
	environment.glow_enabled = false; environment.fog_enabled = false; environment.adjustment_enabled = false
	var sky := WorldEnvironment.new(); sky.environment = environment; world.add_child(sky)
	var points := {}
	for r in range(ROWS.size()):
		for c in range(VALUES.size()):
			var node := MeshInstance3D.new(); var mesh := QuadMesh.new(); mesh.size = Vector2(0.6, 0.8); node.mesh = mesh
			var x := (float(c) - float(VALUES.size() - 1) / 2.0) * 0.68
			var y := 1.5 - float(r) * 1.0
			node.position = Vector3(x, y, 0)
			var m := ShaderMaterial.new(); m.shader = make_shader(ROWS[r], VALUES[c])
			var v: float = VALUES[c]
			if ROWS[r] == "no_hint_color": m.set_shader_parameter("q", Color(v, v, v, 1.0))
			if ROWS[r] == "no_hint_vec4": m.set_shader_parameter("q", Vector4(v, v, v, 1.0))
			if ROWS[r] == "vec3_vec3": m.set_shader_parameter("q", Vector3(v, v, v))
			if ROWS[r] == "vec3_color": m.set_shader_parameter("q", Color(v, v, v, 1.0))
			node.material_override = m; world.add_child(node)
			points[ROWS[r] + "_" + str(c)] = Vector3(x, y, 0)
	for i in range(8): await process_frame
	await RenderingServer.frame_post_draw
	var image := viewport.get_texture().get_image()
	image.save_png(output + "/constant_albedo_b_" + tag + ".png")
	var table := []
	for r in range(ROWS.size()):
		for c in range(VALUES.size()):
			var pos := camera.unproject_position(points[ROWS[r] + "_" + str(c)])
			var col := image.get_pixel(int(pos.x), int(pos.y))
			table.append({"row": ROWS[r], "value": VALUES[c], "pixel": [int(pos.x), int(pos.y)], "rgb8": [roundi(col.r * 255), roundi(col.g * 255), roundi(col.b * 255)], "float": [col.r, col.g, col.b]})
	var report := {
		"engine": Engine.get_version_info().string,
		"rendering_method": RenderingServer.get_current_rendering_method(),
		"adapter": RenderingServer.get_video_adapter_name(),
		"rendering_driver": RenderingServer.get_current_rendering_driver_name(),
		"tag": tag, "rows": table,
	}
	var file := FileAccess.open(output + "/constant_albedo_b_" + tag + ".json", FileAccess.WRITE)
	file.store_string(JSON.stringify(report, "\t")); file.close()
	print("RENDERER ", report.rendering_method, " / ", report.adapter, " / driver ", report.rendering_driver)
	for e in table:
		print("PATCH %-8s %.4f -> %s" % [e.row, e.value, JSON.stringify(e.rgb8)])
	viewport.queue_free(); await process_frame; quit()

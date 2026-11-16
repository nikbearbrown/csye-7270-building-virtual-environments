extends SceneTree
# R9d follow-up probe, written for the film. Same constant-ALBEDO patches as ev-constant-albedo.gd (the "const" row only),
# read back from three kinds of render target, to see whether the Compatibility deviation depends on where the pixels are read:
#   root   : the main window's own viewport, read with root.get_texture().get_image()  (what the assignment's capture() snippet does)
#   sub1280: a 1280x720 SubViewport
#   sub3840: a 3840x2160 SubViewport (what the other evidence scripts use)
# Patch centres are computed from the image size (camera.size = 4 is the vertical extent), not with unproject_position.
# Run: godot --path godot --rendering-method <forward_plus|gl_compatibility> --script res://course-series/tests/ev-constant-albedo-d.gd -- <outdir> <tag> <root|sub1280|sub3840>
const VALUES := [0.0585, 0.09, 0.104, 0.12, 0.16, 0.19, 0.26, 0.40, 0.52, 0.72]
func _initialize() -> void: call_deferred("run")
func run() -> void:
	var args := OS.get_cmdline_user_args()
	var output: String = args[0]
	var tag: String = args[1]
	var mode: String = args[2]
	var holder: Node = root
	var viewport_for_image: Viewport = root
	if mode != "root":
		var sub := SubViewport.new()
		sub.size = Vector2i(1280, 720) if mode == "sub1280" else Vector2i(3840, 2160)
		sub.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		root.add_child(sub)
		holder = sub
		viewport_for_image = sub
	var world := Node3D.new(); holder.add_child(world)
	var camera := Camera3D.new(); camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	camera.size = 4.0; camera.position = Vector3(0, 0, 5); world.add_child(camera); camera.make_current()
	var environment := Environment.new(); environment.background_mode = Environment.BG_COLOR
	environment.background_color = Color("14262d"); environment.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	environment.tonemap_exposure = 1.0
	environment.glow_enabled = false; environment.fog_enabled = false; environment.adjustment_enabled = false
	var sky := WorldEnvironment.new(); sky.environment = environment; world.add_child(sky)
	var xs := []
	for c in range(VALUES.size()):
		var node := MeshInstance3D.new(); var mesh := QuadMesh.new(); mesh.size = Vector2(0.6, 0.8); node.mesh = mesh
		var x := (float(c) - float(VALUES.size() - 1) / 2.0) * 0.68
		node.position = Vector3(x, 0, 0)
		var m := ShaderMaterial.new(); var s := Shader.new()
		s.code = "shader_type spatial;\nrender_mode unshaded;\nvoid fragment() { ALBEDO = vec3(%s); }" % String.num(VALUES[c], 6)
		m.shader = s; node.material_override = m; world.add_child(node); xs.append(x)
	for i in range(8): await process_frame
	await RenderingServer.frame_post_draw
	var image := viewport_for_image.get_texture().get_image()
	image.save_png(output + "/constant_albedo_d_" + tag + "_" + mode + ".png")
	var w := image.get_width(); var h := image.get_height()
	var table := []
	for c in range(VALUES.size()):
		var px := int(float(w) / 2.0 + xs[c] * float(h) / 4.0); var py := int(float(h) / 2.0)
		var col := image.get_pixel(px, py)
		table.append({"value": VALUES[c], "pixel": [px, py], "rgb8": [roundi(col.r * 255), roundi(col.g * 255), roundi(col.b * 255)]})
	var report := {"engine": Engine.get_version_info().string, "rendering_method": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name(), "mode": mode, "image_size": [w, h], "image_format": image.get_format(), "rows": table}
	var file := FileAccess.open(output + "/constant_albedo_d_" + tag + "_" + mode + ".json", FileAccess.WRITE)
	file.store_string(JSON.stringify(report, "\t")); file.close()
	print("RENDERER ", report.rendering_method, " / ", report.adapter, " mode=", mode, " image=", w, "x", h, " format=", image.get_format())
	print("CONST_ROW ", JSON.stringify(table.map(func(e): return e.rgb8[0])))
	quit()

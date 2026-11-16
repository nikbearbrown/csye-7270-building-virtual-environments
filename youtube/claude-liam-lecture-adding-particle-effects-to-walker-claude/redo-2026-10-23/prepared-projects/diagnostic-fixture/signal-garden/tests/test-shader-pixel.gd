extends SceneTree
# Renders the pad shader at activation=0.5 and samples a lit stripe pixel.
# Catches wrong-shader-input defects invisible to headless state checks.
# Invoked non-headless by scripts/check-garden.py alongside test-garden.
func _initialize() -> void: call_deferred("run")
func run() -> void:
	root.size = Vector2i(1280, 720)
	root.content_scale_size = Vector2i(1280, 720)
	var stage := Node3D.new()
	root.add_child(stage)
	var cam := Camera3D.new()
	cam.position = Vector3(0.0, 0.0, 6.0)
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = 5.5
	stage.add_child(cam)
	cam.current = true
	var mat := ShaderMaterial.new()
	mat.shader = load("res://signal-garden/signal.gdshader")
	mat.set_shader_parameter("activation", 0.5)
	var mesh := MeshInstance3D.new()
	var quad := QuadMesh.new()
	quad.size = Vector2(4.0, 3.0)
	mesh.mesh = quad
	mesh.material_override = mat
	stage.add_child(mesh)
	for _i in range(5): await process_frame
	RenderingServer.force_draw(false)
	var image := root.get_texture().get_image()
	# UV.x = 0.21875: fract(0.21875 × 8) = 0.75 ≥ 0.5, so stripe = 1 (lit, shade = 1.0).
	# Quad spans x = -2.0..2.0; world x for this UV: 0.21875 × 4 - 2 = -1.125.
	var sp := cam.unproject_position(Vector3(-1.125, 0.0, 0.0))
	var sx := clampi(int(sp.x), 0, 1279)
	var sy := clampi(int(sp.y), 0, 719)
	var col := image.get_pixel(sx, sy)
	# Oracle model (Compatibility OUTPUT_IS_SRGB): sRGB linear-mix of sRGB inputs.
	# activation = 0.5, stripe = 1, shade = 1.0:
	# 0.5 × [0.40, 0.16, 0.09] + 0.5 × [0.12, 0.72, 0.52] = [0.26, 0.44, 0.305]
	const EXP := [0.26, 0.44, 0.305]
	const TOL := 0.05
	var obs := [col.r, col.g, col.b]
	var ok := absf(col.r - EXP[0]) < TOL and absf(col.g - EXP[1]) < TOL and absf(col.b - EXP[2]) < TOL
	print(JSON.stringify({"id": "shader-pixel-midpoint", "observation": obs, "pass": ok}))
	stage.queue_free()
	await process_frame
	quit(0 if ok else 1)

extends SceneTree
# The code the film shows for driving the dissolve from the game:
#   $Sprite.material.set_shader_parameter("progress", 0.0)
#   var tween := create_tween()
#   tween.tween_property($Sprite.material, "shader_parameter/progress", 1.0, 2.0)
# T1 (without the first line) a tween on a uniform never set from code: error? does progress move?  T2 (with it): does progress move (start, mid, end)?
# Uses the film's dissolve shader (lab-shaders/16-dissolve.gdshader text inlined below) on a Sprite2D. Run: godot --path <dir> --script res://verify-tween-progress.gd
const SHADER := "shader_type canvas_item;\nuniform sampler2D noise_tex;\nuniform sampler2D ramp_tex : source_color;\nuniform float progress : hint_range(0.0, 1.0) = 0.0;\nuniform float edge = 0.1;\nvoid fragment() {\n\tfloat n = texture(noise_tex, UV).r;\n\tfloat cut = mix(-edge, 1.0, progress);\n\tif (n <= cut) discard;\n\tfloat heat = 1.0 - (n - cut) / edge;\n\tif (heat > 0.0) COLOR.rgb = texture(ramp_tex, vec2(heat, 0.5)).rgb;\n}\n"

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func frames(n: int) -> void:
	for i in range(n): await process_frame

func make_sprite() -> Sprite2D:
	var im := Image.create(128, 128, false, Image.FORMAT_RGBA8)
	im.fill(Color("#5FA391"))
	var sp := Sprite2D.new()
	sp.texture = ImageTexture.create_from_image(im)
	sp.position = Vector2(160, 90)
	var fn := FastNoiseLite.new()
	fn.seed = 7
	fn.frequency = 0.02
	var nt := ImageTexture.create_from_image(fn.get_image(256, 256))
	var g := Gradient.new()
	g.offsets = PackedFloat32Array([0.0, 0.5, 1.0])
	g.colors = PackedColorArray([Color("#8A2A12"), Color("#E8742F"), Color("#F7D46B")])
	var gt := GradientTexture1D.new()
	gt.gradient = g
	var sh := Shader.new()
	sh.code = SHADER
	var mat := ShaderMaterial.new()
	mat.shader = sh
	mat.set_shader_parameter("noise_tex", nt)
	mat.set_shader_parameter("ramp_tex", gt)
	sp.material = mat
	return sp

func remaining(img: Image) -> int:
	# count sprite-teal pixels (the sprite is a flat teal square, 128 px)
	var n := 0
	for y in range(26, 154, 2):
		for x in range(96, 224, 2):
			var c := img.get_pixel(x, y)
			if absf(c.r - 0.3725) < 0.02 and absf(c.g - 0.6392) < 0.02 and absf(c.b - 0.5686) < 0.02: n += 1
	return n

func run() -> void:
	root.size = Vector2i(320, 180)
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	for with_initial_set in [false, true]:
		var sp := make_sprite()
		root.add_child(sp)
		await frames(3)
		var mat: ShaderMaterial = sp.material
		var before = mat.get_shader_parameter("progress")
		if with_initial_set:
			mat.set_shader_parameter("progress", 0.0)
		var tw := create_tween()
		tw.tween_property(mat, "shader_parameter/progress", 1.0, 1.0)
		await create_timer(0.5).timeout
		RenderingServer.force_draw(false)
		var mid := remaining(root.get_texture().get_image())
		var mid_val = mat.get_shader_parameter("progress")
		await create_timer(0.7).timeout
		RenderingServer.force_draw(false)
		var end := remaining(root.get_texture().get_image())
		out("T%d-tween-%s-initial-set" % [2 if with_initial_set else 1, "WITH" if with_initial_set else "WITHOUT"],
			{"progress_before_tween_via_get_shader_parameter": str(before), "progress_value_at_half_second": str(mid_val), "teal_samples_left_at_0.5s": mid, "teal_samples_left_at_1.2s": end, "samples_total": 64 * 64})
		sp.queue_free()
		await frames(2)
	quit(0)

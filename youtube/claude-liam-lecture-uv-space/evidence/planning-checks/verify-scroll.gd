extends SceneTree
# UV Space planning check C: does UV.x += TIME * 0.1 scroll at a tenth of the picture per second, and which way?
# The "picture" is the 256x256 address picture (red = x/255), repeat enabled. At a fixed output pixel (the middle) the red value is
# the picture position being read, so how fast red climbs is how fast the picture slides past: red rising = the picture moves LEFT.
# Run: godot --path <project dir> --script res://verify-scroll.gd

const CODE := "shader_type canvas_item;\nuniform sampler2D pic : repeat_enable;\nvoid fragment() {\n\tvec2 uv = UV;\n\tuv.x += TIME * 0.1;\n\tCOLOR = texture(pic, uv);\n}\n"

func _initialize() -> void: call_deferred("run")

func frames(n: int) -> void:
	for i in range(n): await process_frame

func grab() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func addr_picture() -> ImageTexture:
	var im := Image.create(256, 256, false, Image.FORMAT_RGBA8)
	for y in 256:
		for x in 256:
			im.set_pixel(x, y, Color(x / 255.0, y / 255.0, 0.0, 1.0))
	return ImageTexture.create_from_image(im)

func run() -> void:
	root.size = Vector2i(256, 256)
	var cr := ColorRect.new()
	cr.size = Vector2(256, 256)
	var sh := Shader.new()
	sh.code = CODE
	var m := ShaderMaterial.new()
	m.shader = sh
	m.set_shader_parameter("pic", addr_picture())
	cr.material = m
	root.add_child(cr)
	await frames(3)
	var reads: Array = []
	var ticks: Array = []
	for i in range(4):
		var img := grab()
		reads.append(img.get_pixel(128, 128).r)
		ticks.append(Time.get_ticks_msec() / 1000.0)
		var t0 := Time.get_ticks_msec()
		while Time.get_ticks_msec() - t0 < 700:
			await process_frame
	var steps: Array = []
	for i in range(1, reads.size()):
		var d_red := fposmod(reads[i] - reads[i - 1], 1.0)
		var d_t: float = ticks[i] - ticks[i - 1]
		steps.append({"red_step": snappedf(d_red, 0.001), "seconds_by_clock": snappedf(d_t, 0.001), "pictures_per_second": snappedf(d_red / d_t, 0.001)})
	out("C-scroll-speed-and-direction", {"red_at_middle": reads.map(func(v): return snappedf(v, 0.001)), "steps": steps,
		"reading": "red at a fixed pixel rises by about 0.1 per second: the picture position under that pixel increases, so the picture slides LEFT at a tenth of its width per second"})
	quit(0)

extends SceneTree
# Time and Waves, planning check 2: the shown shaders, with their real TIME, against the TIME decoded from the same frame.
#   A  02-pulse: the pixel against 0.5 + 0.5 sin(TAU TIME)
#   B  03-dials with a shared material (speed) and a per-node instance uniform (offset): five squares, offsets 0, 0.2 .. 0.8
#   C  04-three-shapes: where each bar ends against the sine, triangle and sawtooth values
#   D  07-travel: where a crest is against speed * TIME + 0.25 / frequency
# TIME is decoded from a pixel (ENCODER) in the same draw. Run: godot --path <scratch> --always-on-top --script res://verify2.gd -- --film <abs film dir>
const ENCODER := "shader_type canvas_item;\nvoid fragment() {\n\tfloat whole = floor(TIME);\n\tfloat part = (TIME - whole) * 255.0;\n\tfloat p1 = floor(part);\n\tCOLOR = vec4(whole / 255.0, p1 / 255.0, part - p1, 1.0);\n}\n"
const TAU_F := 6.283185307179586
const TEAL := Vector3(0.37, 0.64, 0.57)
const CREAM := Vector3(0.98, 0.97, 0.96)

var film := ""
var enc: ColorRect

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func frames(n: int) -> void:
	for i in range(n): await process_frame

func shader_text(name: String) -> String:
	return FileAccess.get_file_as_string(film + "/lab-shaders/" + name)

func make_rect(code: String, pos: Vector2, size: Vector2) -> ColorRect:
	var rect := ColorRect.new()
	rect.position = pos
	rect.size = size
	var sh := Shader.new()
	sh.code = code
	var mat := ShaderMaterial.new()
	mat.shader = sh
	rect.material = mat
	return rect

func grab() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func decode_time(img: Image) -> float:
	var c := img.get_pixel(int(enc.position.x + 10), int(enc.position.y + 10))
	return roundf(c.r * 255.0) + (roundf(c.g * 255.0) + c.b) / 255.0

func mixv(a: Vector3, b: Vector3, t: float) -> Vector3:
	return a * (1.0 - t) + b * t

func steps(c: Color, v: Vector3) -> float:
	return maxf(maxf(absf(c.r - v.x), absf(c.g - v.y)), absf(c.b - v.z)) * 255.0

func run() -> void:
	var a := OS.get_cmdline_user_args()
	for i in range(a.size()):
		if a[i] == "--film": film = a[i + 1]
	root.size = Vector2i(640, 360)
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	enc = make_rect(ENCODER, Vector2(0, 0), Vector2(20, 20))
	root.add_child(enc)

	# A: 02-pulse
	var pulse := make_rect(shader_text("02-pulse.gdshader"), Vector2(40, 0), Vector2(100, 100))
	root.add_child(pulse)
	# B: 03-dials, one shared material, five nodes with instance offsets
	var dial_shader := Shader.new()
	dial_shader.code = shader_text("03-dials.gdshader")
	var dial_mat := ShaderMaterial.new()
	dial_mat.shader = dial_shader
	var squares: Array = []
	for i in range(5):
		var r := ColorRect.new()
		r.position = Vector2(40 + i * 60, 120)
		r.size = Vector2(50, 50)
		r.material = dial_mat
		root.add_child(r)
		r.set_instance_shader_parameter("offset", i / 5.0)
		squares.append(r)
	# C: 04-three-shapes
	var shapes := make_rect(shader_text("04-three-shapes.gdshader"), Vector2(350, 0), Vector2(240, 120))
	root.add_child(shapes)
	# D: 07-travel
	var travel := make_rect(shader_text("07-travel.gdshader"), Vector2(350, 200), Vector2(240, 60))
	root.add_child(travel)
	(travel.material as ShaderMaterial).set_shader_parameter("frequency", 3.0)
	(travel.material as ShaderMaterial).set_shader_parameter("speed", 0.5)
	await frames(5)

	var maxA := 0.0
	var maxB := 0.0
	var maxC := 0.0
	var maxD := 0.0
	var n := 0
	var first_row_distinct := false
	var sample_B: Array = []
	for f in range(90):
		await process_frame
		var img := grab()
		var t := decode_time(img)
		n += 1
		# A
		var p := 0.5 + 0.5 * sin(TAU_F * t)
		maxA = maxf(maxA, steps(img.get_pixel(90, 50), mixv(TEAL, CREAM, p)))
		# B
		var vals: Array = []
		for i in range(5):
			var pb := 0.5 + 0.5 * sin(TAU_F * (t * 0.5 + i / 5.0))
			var px := img.get_pixel(int(65 + i * 60), 145)
			maxB = maxf(maxB, steps(px, mixv(TEAL, CREAM, pb)))
			vals.append(snappedf(px.g, 0.001))
		if f == 40:
			sample_B = vals
		# C: bar edges in the three rows of the 240 x 120 rect at (350, 0): rows are y 0..40, 40..80, 80..120
		var cyc := t * 0.5
		var saw := cyc - floorf(cyc)
		var tri := 1.0 - absf(saw * 2.0 - 1.0)
		var sine := 0.5 + 0.5 * sin(TAU_F * (cyc - 0.25))
		var want := [sine, tri, saw]
		for row in range(3):
			var y := int(20 + row * 40)
			var edge := 0
			for x in range(240):
				var px2 := img.get_pixel(350 + x, y)
				if absf(px2.r - 0.3686) < 0.02 and absf(px2.g - 0.6392) < 0.02:
					edge = x + 1
				else:
					break
			# the bar is solid from the left to the edge; compare with value * 240 (one pixel of slack each way)
			var got := float(edge) / 240.0
			maxC = maxf(maxC, absf(got - float(want[row])) * 240.0)
		# D: crest of the stripes: find the brightest x (in the first 80 px, frequency 3 -> crest spacing 80 px)
		var best_x := 0
		var best_v := -1.0
		for x in range(240):
			var px3 := img.get_pixel(350 + x, 230)
			if px3.r > best_v:
				best_v = px3.r
				best_x = x
		var crest := fmod(0.5 * t + 0.25 / 3.0, 1.0 / 3.0) * 240.0         # first crest from the left, in pixels
		var d := absf(float(best_x) - crest)
		d = minf(d, absf(d - 80.0))
		maxD = maxf(maxD, d)
	out("A-pulse-vs-TIME", {"frames": n, "max_error_8bit_steps": snappedf(maxA, 0.01), "reading": "02-pulse pixel against 0.5 + 0.5 sin(TAU TIME), TIME decoded from the same frame"})
	out("B-dials-instance-offsets", {"frames": n, "max_error_8bit_steps": snappedf(maxB, 0.01), "green_channel_of_the_five_squares_at_one_frame": sample_B,
		"reading": "five squares share one ShaderMaterial (speed 0.5); each has its own instance uniform offset = 0, 0.2, 0.4, 0.6, 0.8. If the instance uniforms did not work all five would match."})
	out("C-three-shapes-edges", {"frames": n, "max_error_pixels_of_240": snappedf(maxC, 0.01), "reading": "bar edge position against sine, triangle, sawtooth values (rect 240 px wide)"})
	out("D-travel-crest", {"frames": n, "max_error_pixels": snappedf(maxD, 0.01), "reading": "first bright crest position (px) against speed * TIME + 0.25 / frequency; crest spacing is 80 px"})
	quit(0)

extends SceneTree
# Time and Waves, planning check 5: what the TIME roll-over does to a pulse.
# The roll-over limit is set to 2.0 s at run time (the default is 3600 s; nobody waits an hour). Two copies of the 03-dials pulse:
#   "fits":  speed 1.0 -> 2 whole cycles in the 2 s limit  -> the pulse should carry on smoothly through the wrap
#   "jumps": speed 0.7 -> 1.4 cycles in the 2 s limit       -> the pulse should jump at the wrap
# For every frame where TIME fell (a wrap) the colour change from the frame before is compared with the largest change between ordinary frames.
# Run: godot --path <scratch> --always-on-top --script res://verify5_rollover.gd -- --film <abs film dir>
const ENCODER := "shader_type canvas_item;\nvoid fragment() {\n\tfloat whole = floor(TIME);\n\tfloat part = (TIME - whole) * 255.0;\n\tfloat p1 = floor(part);\n\tCOLOR = vec4(whole / 255.0, p1 / 255.0, part - p1, 1.0);\n}\n"
var film := ""
var enc: ColorRect

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func grab() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func make_rect(code: String, pos: Vector2, size := Vector2(20, 20)) -> ColorRect:
	var rect := ColorRect.new()
	rect.position = pos
	rect.size = size
	var sh := Shader.new()
	sh.code = code
	var mat := ShaderMaterial.new()
	mat.shader = sh
	rect.material = mat
	return rect

func decode(img: Image) -> float:
	var c := img.get_pixel(int(enc.position.x + 10), int(enc.position.y + 10))
	return roundf(c.r * 255.0) + (roundf(c.g * 255.0) + c.b) / 255.0

func run() -> void:
	var a := OS.get_cmdline_user_args()
	for i in range(a.size()):
		if a[i] == "--film": film = a[i + 1]
	root.size = Vector2i(320, 180)
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	enc = make_rect(ENCODER, Vector2(0, 0))
	root.add_child(enc)
	var dials := FileAccess.get_file_as_string(film + "/lab-shaders/03-dials.gdshader").replace("instance uniform", "uniform")
	var fits := make_rect(dials, Vector2(60, 20), Vector2(60, 60))
	var jumps := make_rect(dials, Vector2(160, 20), Vector2(60, 60))
	(fits.material as ShaderMaterial).set_shader_parameter("speed", 1.0)
	(jumps.material as ShaderMaterial).set_shader_parameter("speed", 0.7)
	root.add_child(fits)
	root.add_child(jumps)
	for i in range(5): await process_frame
	ProjectSettings.set_setting("rendering/limits/time/time_rollover_secs", 2.0)
	var prev_t := -1.0
	var prev_f := 0.0
	var prev_j := 0.0
	var ordinary_f := 0.0
	var ordinary_j := 0.0
	var wraps_f: Array = []
	var wraps_j: Array = []
	var times_at_wrap: Array = []
	for f in range(600):
		await process_frame
		var im := grab()
		var t := decode(im)
		var cf := im.get_pixel(90, 50).r
		var cj := im.get_pixel(190, 50).r
		if prev_t >= 0.0:
			if t < prev_t - 0.5:
				wraps_f.append(snappedf(absf(cf - prev_f) * 255.0, 0.1))
				wraps_j.append(snappedf(absf(cj - prev_j) * 255.0, 0.1))
				times_at_wrap.append([snappedf(prev_t, 0.001), snappedf(t, 0.001)])
			else:
				ordinary_f = maxf(ordinary_f, absf(cf - prev_f) * 255.0)
				ordinary_j = maxf(ordinary_j, absf(cj - prev_j) * 255.0)
		prev_t = t
		prev_f = cf
		prev_j = cj
	out("H-rollover-jump", {"limit_s": 2.0, "wraps_seen": wraps_f.size(), "TIME_before_and_after_each_wrap": times_at_wrap,
		"fits_speed_1.0_change_at_each_wrap_8bit_steps": wraps_f, "largest_ordinary_frame_change_fits_steps": snappedf(ordinary_f, 0.1),
		"jumps_speed_0.7_change_at_each_wrap_8bit_steps": wraps_j, "largest_ordinary_frame_change_jumps_steps": snappedf(ordinary_j, 0.1),
		"reading": "a pulse that repeats a whole number of times in the limit changes no more at the wrap than between any two frames; any other pulse jumps."})
	quit(0)

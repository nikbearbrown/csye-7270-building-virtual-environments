extends SceneTree
# glow_check.gd: renders the film's glow bubble (lab-shaders/14-glow-bubble.gdshader, or another shader given with --shader) in a REAL window
# of Godot 4.7.2 under chosen settings, and prints one RESULT line of pixel readings.
# The Lab (lab/runner.gd) cannot add a WorldEnvironment or switch HDR 2D, so this is the scratch route the common brief allows.
#
#   godot --path <scratch project> [--rendering-method gl_compatibility] --script res://glow_check.gd -- <options>
#   --shader <abs path>     shader file (default: the film's 14-glow-bubble.gdshader)
#   --label <text>          name echoed in the RESULT line
#   --glow 1.0              the shader's `glow` uniform (if the shader has one)
#   --hdr2d                 set Viewport.use_hdr_2d = true on the root viewport before the first frame (the runtime form of the project setting)
#   --env                   add a WorldEnvironment with an Environment whose glow is enabled
#   --threshold 1.0         Environment.glow_hdr_threshold
#   --intensity 0.8         Environment.glow_intensity (engine default 0.3 when omitted)
#   --bloom 0.0             Environment.glow_bloom
#   --bgcanvas              Environment.background_mode = BG_CANVAS
#   --set name=value        extra float/color uniform (floats only; use #hex for colors)
#   --sub                   ALSO render the shader into a 256x256 SubViewport (use_hdr_2d follows the root viewport) and read its texture back as an image
#   --frames 12             how many process frames to run before the frame is read (post effects may need a few)
#   --clear "#D9D5CA"       the stage (clear) colour; the Lab default is a LIGHT warm grey, on which glow is hard to see
#   --blend N               Environment.glow_blend_mode (0 additive, 1 screen, 2 softlight, 3 replace, 4 mix); engine default is screen
#   --png <abs path>        save the window frame
#
# The bubble is a 256 x 256 ColorRect centred in a 640 x 360 window: UV (u, v) is window pixel (192 + 256 u, 52 + 256 v).
# The disc is fully opaque inside radius 64 px of (320, 180), fades to nothing at radius 102.4 px.

var A := {"shader": "", "label": "", "glow": 1.0, "hdr2d": false, "env": false, "threshold": 1.0, "intensity": -1.0, "bloom": 0.0,
	"bgcanvas": false, "sets": [], "sub": false, "png": "", "frames": 12, "clear": "#D9D5CA", "blend": -1}

func _initialize() -> void:
	call_deferred("run")

func parse() -> void:
	var a := OS.get_cmdline_user_args()
	var i := 0
	while i < a.size():
		var k: String = a[i]
		if k == "--shader": A["shader"] = a[i + 1]; i += 2
		elif k == "--label": A["label"] = a[i + 1]; i += 2
		elif k == "--glow": A["glow"] = float(a[i + 1]); i += 2
		elif k == "--hdr2d": A["hdr2d"] = true; i += 1
		elif k == "--env": A["env"] = true; i += 1
		elif k == "--threshold": A["threshold"] = float(a[i + 1]); i += 2
		elif k == "--intensity": A["intensity"] = float(a[i + 1]); i += 2
		elif k == "--bloom": A["bloom"] = float(a[i + 1]); i += 2
		elif k == "--bgcanvas": A["bgcanvas"] = true; i += 1
		elif k == "--set": A["sets"].append(a[i + 1]); i += 2
		elif k == "--sub": A["sub"] = true; i += 1
		elif k == "--png": A["png"] = a[i + 1]; i += 2
		elif k == "--frames": A["frames"] = int(a[i + 1]); i += 2
		elif k == "--clear": A["clear"] = a[i + 1]; i += 2
		elif k == "--blend": A["blend"] = int(a[i + 1]); i += 2
		else: i += 1

func frames(n: int) -> void:
	for i in range(n):
		await process_frame

func rgba(c: Color) -> Array:
	return [snappedf(c.r, 0.0001), snappedf(c.g, 0.0001), snappedf(c.b, 0.0001), snappedf(c.a, 0.0001)]

# With HDR 2D on, the window image holds LINEAR floats (the engine encodes them to sRGB only when it blits to the screen). "display" is what
# the screen would show: clamp to 0..1 then encode. Without HDR 2D the image already holds the display values.
func to_display(c: Color) -> Color:
	if not root.use_hdr_2d or RenderingServer.get_current_rendering_method() == "gl_compatibility":
		return c   # SDR already holds display values; the Compatibility renderer does not render HDR 2D in linear light
	var k := Color(clampf(c.r, 0.0, 1.0), clampf(c.g, 0.0, 1.0), clampf(c.b, 0.0, 1.0), 1.0)
	return k.linear_to_srgb()

func make_material(code: String) -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = code
	var mat := ShaderMaterial.new()
	mat.shader = sh
	var names: Array = []
	for u in sh.get_shader_uniform_list():
		names.append(String(u["name"]))
	if names.has("glow"):
		mat.set_shader_parameter("glow", float(A["glow"]))
	for s in A["sets"]:
		var kv := String(s).split("=", true, 1)
		if kv[1].begins_with("#"):
			mat.set_shader_parameter(kv[0], Color(kv[1]))
		else:
			mat.set_shader_parameter(kv[0], float(kv[1]))
	return mat

func run() -> void:
	parse()
	var code := FileAccess.get_file_as_string(String(A["shader"]) if String(A["shader"]) != "" else "res://14-glow-bubble.gdshader")
	if code == "":
		print("RESULT " + JSON.stringify({"ok": false, "error": "cannot read the shader"}))
		quit(2)
		return
	DisplayServer.window_move_to_foreground()   # a covered window is not drawn
	RenderingServer.set_default_clear_color(Color(String(A["clear"])))
	root.size = Vector2i(640, 360)
	if bool(A["hdr2d"]):
		root.use_hdr_2d = true
	var rect := ColorRect.new()
	rect.size = Vector2(256, 256)
	rect.position = Vector2(192, 52)
	rect.material = make_material(code)
	root.add_child(rect)
	if bool(A["env"]):
		var e := Environment.new()
		e.glow_enabled = true
		e.glow_hdr_threshold = float(A["threshold"])
		e.glow_bloom = float(A["bloom"])
		if float(A["intensity"]) >= 0.0:
			e.glow_intensity = float(A["intensity"])
		if int(A["blend"]) >= 0:
			e.glow_blend_mode = int(A["blend"]) as Environment.GlowBlendMode
		if bool(A["bgcanvas"]):
			e.background_mode = Environment.BG_CANVAS
		var we := WorldEnvironment.new()
		we.environment = e
		root.add_child(we)
	var sub: SubViewport = null
	if bool(A["sub"]):
		sub = SubViewport.new()
		sub.size = Vector2i(256, 256)
		sub.use_hdr_2d = root.use_hdr_2d
		sub.transparent_bg = true
		sub.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		var r2 := ColorRect.new()
		r2.size = Vector2(256, 256)
		r2.material = make_material(code)
		sub.add_child(r2)
		root.add_child(sub)
	await frames(int(A["frames"]))
	RenderingServer.force_draw(false)
	var img := root.get_texture().get_image()
	var pts := {
		"spot_center": Vector2i(282, 142),          # UV (0.35, 0.35)
		"disc_center": Vector2i(320, 180),
		"body_far_from_spot": Vector2i(346, 206),   # UV (0.6, 0.6)
		"edge_band_mid": Vector2i(320 + 83, 180),   # radius 83 px: the middle of the soft band
		"halo_r108": Vector2i(320 + 108, 180),
		"halo_r118": Vector2i(320 + 118, 180),
		"halo_r130": Vector2i(320 + 130, 180),      # outside the 256 px rect (it ends at radius 128)
		"halo_r160": Vector2i(320 + 160, 180),
		"halo_r200": Vector2i(320 + 200, 180),
		"far_corner": Vector2i(30, 30)}
	var probes := {}
	var display := {}
	for k in pts:
		probes[k] = rgba(img.get_pixel(pts[k].x, pts[k].y))
		display[k] = rgba(to_display(img.get_pixel(pts[k].x, pts[k].y)))
	var out := {"ok": true, "label": A["label"], "engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(),
		"adapter": RenderingServer.get_video_adapter_name(), "hdr2d_flag": A["hdr2d"], "root_use_hdr_2d": root.use_hdr_2d, "env_glow": A["env"], "threshold": A["threshold"], "intensity": A["intensity"], "clear": A["clear"], "blend": A["blend"], "bgcanvas": A["bgcanvas"],
		"glow_uniform": A["glow"], "window_image_format": img.get_format(), "frames_run": A["frames"], "frames_drawn": Engine.get_frames_drawn(), "probes": probes, "display": display}
	if sub != null:
		var simg := sub.get_texture().get_image()
		out["sub_format"] = simg.get_format()   # 5 = RGBA8, 15 = RGBAH (Image.Format enum)
		out["sub_probes"] = {"body_far_from_spot": rgba(simg.get_pixel(154, 154)), "spot_center": rgba(simg.get_pixel(90, 90)), "far_corner": rgba(simg.get_pixel(4, 4))}
	if String(A["png"]) != "":
		DirAccess.make_dir_recursive_absolute(String(A["png"]).get_base_dir())
		var shot := img.duplicate() as Image
		if root.use_hdr_2d and RenderingServer.get_current_rendering_method() != "gl_compatibility":
			shot.convert(Image.FORMAT_RGBA8)   # clamps to 0..1 (linear)
			shot.linear_to_srgb()              # what the screen shows
		shot.save_png(A["png"])
	print("RESULT " + JSON.stringify(out))
	quit(0)

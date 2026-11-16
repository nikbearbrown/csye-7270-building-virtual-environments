extends SceneTree
# Shared plumbing for the verification scripts (run with:  godot --path <project> [--rendering-method gl_compatibility] --script res://tools/<script>.gd -- <args>).
# A real, windowed Godot; the render loop is switched off and every picture is one process_frame + RenderingServer.force_draw(false, step),
# so shader TIME advances only by the step we give it (the same technique as the series Lab's capture.gd). Offline: says nothing about real-time speed.

var out: Array = []          # every line printed, also written to the log file given by --log
var log_path := ""
var args := {}
var xfer := PackedFloat32Array()   # calibrated: the SCREEN value (0..1) that ALBEDO = k/255 produces, for k = 0..255 (see calibrate())
var is_compat := false

func _initialize() -> void:
	call_deferred("_main")

func _main() -> void:
	var a := OS.get_cmdline_user_args()
	var i := 0
	while i < a.size():
		if a[i].begins_with("--") and i + 1 < a.size() and not String(a[i + 1]).begins_with("--"):
			args[String(a[i]).substr(2)] = a[i + 1]
			i += 2
		else:
			args[String(a[i]).substr(2)] = "1"
			i += 1
	log_path = String(args.get("log", ""))
	RenderingServer.set_default_clear_color(Rig.CLEAR)
	root.size = Vector2i(1280, 720)
	DisplayServer.window_set_flag(DisplayServer.WINDOW_FLAG_ALWAYS_ON_TOP, true)
	RenderingServer.render_loop_enabled = false
	is_compat = RenderingServer.get_current_rendering_method() == "gl_compatibility"
	say("HEADER godot %s | renderer %s | adapter %s | window %s" % [Engine.get_version_info()["string"], RenderingServer.get_current_rendering_method(),
		RenderingServer.get_video_adapter_name(), str(root.size)])
	await run()
	if log_path != "":
		var f := FileAccess.open(log_path, FileAccess.WRITE)
		f.store_string("\n".join(out) + "\n")
		f.close()
	quit(0)

func run() -> void:
	pass

func say(s: String) -> void:
	print(s)
	out.append(s)

# one picture: wait a frame, draw with the given clock step, return the root viewport's pixels
func shoot(step := 0.0) -> Image:
	await process_frame
	RenderingServer.force_draw(false, step)
	return root.get_texture().get_image()

func warm(n := 3) -> void:
	for k in range(n):
		await process_frame
		RenderingServer.force_draw(false, 0.0)

# a Node3D scene root with the rig camera only; returns the root
func scene_with_camera() -> Dictionary:
	var s := Node3D.new()
	root.add_child(s)
	var cam := Camera3D.new()
	cam.fov = Rig.FOV_DEG
	cam.position = Rig.CAM_POS
	s.add_child(cam)
	cam.current = true
	return {"scene": s, "camera": cam}

# a big quad covering the whole view, wearing a ShaderMaterial built from `code`
func flat(code: String, params := {}) -> Dictionary:
	var d := scene_with_camera()
	var q := QuadMesh.new()
	q.size = Vector2(20, 20)
	var mi := MeshInstance3D.new()
	mi.mesh = q
	var sh := Shader.new()
	sh.code = code
	var m := ShaderMaterial.new()
	m.shader = sh
	for k in params:
		m.set_shader_parameter(k, params[k])
	mi.material_override = m
	d["scene"].add_child(mi)
	d["mesh"] = mi
	d["material"] = m
	return d

func drop(d: Dictionary) -> void:
	d["scene"].queue_free()
	await process_frame

func px(img: Image, x: int, y: int) -> Color:
	return img.get_pixel(x, y)

func b255(c: Color) -> String:
	return "(%d,%d,%d)" % [int(round(c.r * 255.0)), int(round(c.g * 255.0)), int(round(c.b * 255.0))]

# ---------------------------------------------------------------- the ALBEDO -> screen transfer curve, MEASURED (it differs between renderers)
func calibrate() -> void:
	var code := "shader_type spatial; render_mode unshaded;\nvoid fragment() { float k = floor(FRAGCOORD.x / 5.0); ALBEDO = vec3(k / 255.0); }\n"
	var d := flat(code)
	await warm(2)
	var img := await shoot()
	xfer.resize(256)
	var worst_gray := 0.0
	for k in range(256):
		var c := img.get_pixel(k * 5 + 2, 360)
		xfer[k] = c.r
		worst_gray = maxf(worst_gray, maxf(absf(c.r - c.g), absf(c.r - c.b)))
	await drop(d)
	var mono := true
	for k in range(1, 256):
		if xfer[k] < xfer[k - 1] - 1e-6:
			mono = false
	say("NOTE transfer curve measured (ALBEDO k/255 -> screen byte): 16:%d 32:%d 64:%d 128:%d 188:%d 255:%d | monotone %s | grey (r=g=b) %s" % [
		int(round(xfer[16] * 255)), int(round(xfer[32] * 255)), int(round(xfer[64] * 255)), int(round(xfer[128] * 255)), int(round(xfer[188] * 255)), int(round(xfer[255] * 255)), str(mono), str(worst_gray < 0.005)])

# screen value (0..1) for a shader output x (0..1), by the measured curve
func scr(x: float) -> float:
	var t := clampf(x, 0.0, 1.0) * 255.0
	var k := mini(int(floor(t)), 254)
	return lerpf(xfer[k], xfer[k + 1], t - k)

# shader output (0..1) that produced a screen value s: the inverse of scr()
func inv(s: float) -> float:
	if s <= xfer[0]:
		return 0.0
	if s >= xfer[255]:
		return 1.0
	var lo := 0
	var hi := 255
	while hi - lo > 1:
		var mid := (lo + hi) >> 1
		if xfer[mid] <= s:
			lo = mid
		else:
			hi = mid
	var span := xfer[hi] - xfer[lo]
	return (lo + (s - xfer[lo]) / span if span > 1e-9 else float(lo)) / 255.0

func scr3(v: Vector3) -> Vector3:
	return Vector3(scr(v.x), scr(v.y), scr(v.z))

func inv3(c: Color) -> Vector3:
	return Vector3(inv(c.r), inv(c.g), inv(c.b))

# what a shader receives for an sRGB-authored colour or texel: Forward+ converts to linear light, Compatibility passes the number through (measured, TRAP-2 / TRAP-5)
func dec(c: Color) -> Vector3:
	if is_compat:
		return Vector3(c.r, c.g, c.b)
	return Vector3(Rig.srgb_to_lin(c.r), Rig.srgb_to_lin(c.g), Rig.srgb_to_lin(c.b))

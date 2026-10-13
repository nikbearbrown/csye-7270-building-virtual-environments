extends SceneTree
# verify1: how a 2D lit pixel is made. A sprite (colour 0.6, 0.3, 0.9), an optional CanvasModulate (ambient), optional white light(s), and optional light() code.
# Cases A-F use Godot's DEFAULT lighting (no light() written). Cases G-M write a light() and read what the pixel becomes.
# Run: godot --path <project dir> --script res://verify1.gd
const LL := preload("res://lightlab.gd")
const SPR := Color(0.6, 0.3, 0.9, 1.0)

func _initialize() -> void: call_deferred("run")
func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))
func frames(n: int) -> void:
	for i in range(n): await process_frame
func grab() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()
func clear() -> void:
	for c in root.get_children(): c.queue_free()
	await frames(2)

func build(ambient: Variant, lights: Array, code: String) -> void:
	if ambient != null: root.add_child(LL.canvas_mod(ambient))
	var mat: ShaderMaterial = LL.shader_mat(code) if code != "" else null
	root.add_child(LL.sprite(LL.solid_tex(SPR, 64), Vector2(160, 90), Vector2(1.5, 1.5), mat))
	for l in lights: root.add_child(l)
	await frames(4)

func case_(id: String, ambient: Variant, lights: Array, code: String, note: String) -> void:
	await clear()
	await build(ambient, lights, code)
	var im := grab()
	out(id, {"centre_rgb": LL.px(im, 160, 90), "note": note})

func run() -> void:
	root.size = Vector2i(320, 180)
	var white := LL.solid_tex(Color.WHITE, 128)
	var env := {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(),
		"adapter": RenderingServer.get_video_adapter_name(), "image": [grab().get_width(), grab().get_height()]}
	out("env", env)
	# --- default lighting (no light() written) ---
	await case_("A-no-canvasmodulate-no-light", null, [], "", "sprite colour 0.6,0.3,0.9; nothing else: the 2D default is unshaded")
	await case_("B-no-canvasmodulate-one-white-light", null, [LL.point_light(Vector2(160, 90), white, 4.0, 1.0)], "", "no CanvasModulate + one white light, energy 1")
	await case_("C-ambient0.2-no-light", Color(0.2, 0.2, 0.2), [], "", "CanvasModulate 0.2 grey, no light: sprite x 0.2?")
	await case_("D-ambient0.2-one-white-light-e1", Color(0.2, 0.2, 0.2), [LL.point_light(Vector2(160, 90), white, 4.0, 1.0)], "", "ambient 0.2 + white light energy 1")
	await case_("E-ambient0.2-one-white-light-e0.5", Color(0.2, 0.2, 0.2), [LL.point_light(Vector2(160, 90), white, 4.0, 0.5)], "", "ambient 0.2 + white light energy 0.5")
	await case_("F-ambient0-one-orange-light-e1", Color(0, 0, 0), [LL.point_light(Vector2(160, 90), white, 4.0, 1.0, Color(1.0, 0.5, 0.0))], "", "ambient black + orange light (1,0.5,0)")
	await case_("F2-ambient0-one-white-light-e2", Color(0, 0, 0), [LL.point_light(Vector2(160, 90), white, 4.0, 2.0)], "", "ambient black + white light energy 2")
	# --- light() written ---
	var L := func(body: String) -> String: return "shader_type canvas_item;\nvoid light() {\n\t" + body + "\n}\n"
	await case_("G-light-empty-ambient0.2-one-light", Color(0.2, 0.2, 0.2), [LL.point_light(Vector2(160, 90), white, 4.0, 1.0)], L.call(""), "empty light(), ambient 0.2, one white light")
	await case_("G0-light-empty-ambient0.2-no-light", Color(0.2, 0.2, 0.2), [], L.call(""), "empty light(), ambient 0.2, NO light")
	await case_("H-light-const0.2-ambient0.2-one-light", Color(0.2, 0.2, 0.2), [LL.point_light(Vector2(160, 90), white, 4.0, 1.0)], L.call("LIGHT = vec4(0.2, 0.2, 0.2, 1.0);"), "light() = 0.2 grey constant, ambient 0.2, one light")
	await case_("I-light-const-white-ambient0-one-light", Color(0, 0, 0), [LL.point_light(Vector2(160, 90), white, 4.0, 1.0)], L.call("LIGHT = vec4(1.0, 1.0, 1.0, 1.0);"), "light() = white, ambient black, one light: is the sprite colour multiplied in?")
	await case_("I2-light-const-0.5-ambient0-one-light", Color(0, 0, 0), [LL.point_light(Vector2(160, 90), white, 4.0, 1.0)], L.call("LIGHT = vec4(0.5, 0.5, 0.5, 1.0);"), "light() = 0.5 grey, ambient black, one light")
	await case_("J-light-alpha0.5-ambient0-one-light", Color(0, 0, 0), [LL.point_light(Vector2(160, 90), white, 4.0, 1.0)], L.call("LIGHT = vec4(1.0, 1.0, 1.0, 0.5);"), "light() white with alpha 0.5, ambient black: does alpha scale the add?")
	await case_("K-light-COLOR-only-ambient0-one-light", Color(0, 0, 0), [LL.point_light(Vector2(160, 90), white, 4.0, 1.0)], L.call("LIGHT = vec4(COLOR.rgb, 1.0);"), "light() = COLOR.rgb")
	await case_("L-light-LIGHTCOLOR-x-COLOR-e2", Color(0, 0, 0), [LL.point_light(Vector2(160, 90), white, 4.0, 2.0, Color(1.0, 0.5, 0.0))], L.call("LIGHT = vec4(COLOR.rgb * LIGHT_COLOR.rgb * LIGHT_ENERGY, LIGHT_COLOR.a);"), "rebuilt default, energy 2, orange light")
	await case_("L0-DEFAULT-same-scene-as-L", Color(0, 0, 0), [LL.point_light(Vector2(160, 90), white, 4.0, 2.0, Color(1.0, 0.5, 0.0))], "", "default lighting in the very same scene as L")
	await case_("M-light-LIGHTCOLOR-rgb-over-4", Color(0, 0, 0), [LL.point_light(Vector2(160, 90), white, 4.0, 2.0, Color(1.0, 0.5, 0.0))], L.call("LIGHT = vec4(LIGHT_COLOR.rgb * 0.25, 1.0);"), "read LIGHT_COLOR.rgb/4 (energy 2, colour 1,0.5,0): is energy already inside LIGHT_COLOR?")
	await case_("M2-light-ENERGY-over-4", Color(0, 0, 0), [LL.point_light(Vector2(160, 90), white, 4.0, 2.0, Color(1.0, 0.5, 0.0))], L.call("LIGHT = vec4(vec3(LIGHT_ENERGY * 0.25), 1.0);"), "read LIGHT_ENERGY/4 (energy 2)")
	await case_("M3-light-LIGHTCOLOR-a", Color(0, 0, 0), [LL.point_light(Vector2(160, 90), white, 4.0, 2.0, Color(1.0, 0.5, 0.0, 0.5))], L.call("LIGHT = vec4(vec3(LIGHT_COLOR.a), 1.0);"), "read LIGHT_COLOR.a (light colour alpha 0.5, opaque texture)")
	quit(0)

extends Node2D
# Captures C35 (beat B35, the finished scene) and C38 / C39 (the logo alone, the banner alone): the logo breathes (12-breath + the CurveTexture), the banner waves (13-banner, wind 1).
# Run with user args: --part together | logo | banner  (default together). 30 fps; together 12 s (360 frames), logo 10 s (300), banner 10 s (300).
# Layout, together: logo centred (0.50, 0.30) at 0.50 of the height; banner centred (0.50, 0.72) at 0.55 of the width. Alone: centred (0.50, 0.50) at the same sizes.
const C = preload("res://scenes/scene_common.gd")

func part() -> String:
	var a := OS.get_cmdline_user_args()
	var i := a.find("--part")
	return a[i + 1] if i >= 0 and i + 1 < a.size() else "together"

func _ready() -> void:
	C.stage()
	var vp := get_viewport_rect().size
	var p := part()
	if p == "together" or p == "logo":
		var logo := C.shaded_sprite(C.blob_texture(), "12-breath.gdshader", Vector2(vp.x * 0.5, vp.y * (0.30 if p == "together" else 0.5)), vp.y * 0.5 / 128.0)
		(logo.material as ShaderMaterial).set_shader_parameter("curve", C.breath_curve_texture())
		add_child(logo)
	if p == "together" or p == "banner":
		var banner := C.shaded_sprite(C.banner_texture(), "13-banner.gdshader", Vector2(vp.x * 0.5, vp.y * (0.72 if p == "together" else 0.5)), vp.x * 0.55 / 256.0)
		(banner.material as ShaderMaterial).set_shader_parameter("wind", 1.0)
		add_child(banner)
	if C.wants_verify():
		add_child(C.shaded_rect(C.ENCODER, Vector2(0, 0), Vector2(20, 20)))

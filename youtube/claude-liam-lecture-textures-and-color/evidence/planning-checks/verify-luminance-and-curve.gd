extends SceneTree
# L1: Color.get_luminance() of the pure primaries = the grey weights the film uses (should read 0.2126, 0.7152, 0.0722).
# L2: the sRGB curve in numbers: srgb_to_linear / linear_to_srgb at the values the film says aloud.
# L3: the two midpoints of two greys (0.2 and 0.8): average the typed numbers, or average the light and convert back.
# L4: the film's grey weights applied to the four swatches' typed numbers (what the 2D shader computes) against the true luminance converted back to typed numbers.
func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func r4(x: float) -> float: return snappedf(x, 0.0001)

func run() -> void:
	out("L1-weights-from-get_luminance", {"red": r4(Color(1, 0, 0).get_luminance()), "green": r4(Color(0, 1, 0).get_luminance()), "blue": r4(Color(0, 0, 1).get_luminance()), "white": r4(Color(1, 1, 1).get_luminance())})
	var pts := [0.0, 0.0331, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7354, 0.8, 0.9, 1.0]
	var rows := []
	for v in pts:
		var c := Color(v, v, v)
		rows.append({"typed": v, "to_linear": r4(c.srgb_to_linear().r), "typed_again_from_linear": r4(Color(v, v, v).linear_to_srgb().r)})
	out("L2-curve", {"rows": rows, "half_the_light_as_typed": r4(Color(0.5, 0.5, 0.5).linear_to_srgb().r), "typed_half_as_light": r4(Color(0.5, 0.5, 0.5).srgb_to_linear().r)})
	var a := Color(0.2, 0.2, 0.2)
	var b := Color(0.8, 0.8, 0.8)
	var typed_mid := a.lerp(b, 0.5)
	var light_mid := a.srgb_to_linear().lerp(b.srgb_to_linear(), 0.5).linear_to_srgb()
	out("L3-midpoints", {"typed_midpoint": r4(typed_mid.r), "light_midpoint_shown_as_typed": r4(light_mid.r), "light_midpoint_in_light": r4(a.srgb_to_linear().lerp(b.srgb_to_linear(), 0.5).r)})
	var sw := {"rose": Color("#E6598C"), "leaf": Color("#66A659"), "sky": Color("#6680D9"), "sand": Color("#E0B04A")}
	var rows4 := {}
	for k in sw.keys():
		var c: Color = sw[k]
		var typed_luma := 0.2126 * c.r + 0.7152 * c.g + 0.0722 * c.b
		var lin := c.srgb_to_linear()
		var true_lum := 0.2126 * lin.r + 0.7152 * lin.g + 0.0722 * lin.b
		rows4[k] = {"typed": [r4(c.r), r4(c.g), r4(c.b)], "red_channel_only": r4(c.r), "weighted_on_typed_numbers": r4(typed_luma), "true_luminance_in_light": r4(true_lum),
			"true_luminance_shown_as_typed": r4(Color(true_lum, true_lum, true_lum).linear_to_srgb().r), "get_luminance_of_linear": r4(lin.get_luminance())}
	out("L4-grey-weights-on-the-swatches", rows4)
	quit(0)

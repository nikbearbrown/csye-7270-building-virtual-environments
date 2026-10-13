extends SceneTree
# CPU-side (GDScript) checks for the Trigonometry for Shaders layout. Nothing here renders; it backs the docs quotes about
# Vector2.from_angle(), Vector2.angle(), rotation direction, and the arithmetic of the numbers shown on screen.
# Run: godot --headless --path <scratch project> --script <absolute path to this file>
# Each check prints one RESULT line (JSON).

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func _initialize() -> void:
	out("env", {"engine": Engine.get_version_info()["string"]})

	# A. Vector2.from_angle(a) equals Vector2(cos(a), sin(a))  (docs: "This is equivalent to doing Vector2(cos(angle), sin(angle))")
	var worst := 0.0
	for a in [0.0, 0.5236, 1.0, 1.5708, 2.0, 3.1416, 4.0, 4.7124, 6.0, -1.0, -2.5, 30.0]:
		var d: Vector2 = Vector2.from_angle(a) - Vector2(cos(a), sin(a))
		worst = maxf(worst, d.length())
	out("A-from-angle-equals-cos-sin", {"largest_difference": worst})

	# B. Vector2.angle() for the compass vectors (docs: DOWN.angle() will return PI / 2)
	out("B-angle-of-compass-vectors", {"RIGHT": Vector2.RIGHT.angle(), "DOWN": Vector2.DOWN.angle(), "LEFT": Vector2.LEFT.angle(), "UP": Vector2.UP.angle(),
		"(1,-1)": Vector2(1, -1).angle(), "PI/2": PI / 2.0, "-PI/4": -PI / 4.0, "DOWN_is_plus_y": Vector2.DOWN.y})

	# C. A positive rotation of RIGHT lands on DOWN: clockwise on a screen where y counts downward
	var r: Vector2 = Vector2.RIGHT.rotated(PI / 2.0)
	out("C-positive-rotation-goes-down", {"RIGHT_rotated_PI_over_2": [snappedf(r.x, 0.000001), snappedf(r.y, 0.000001)]})

	# D. Vector2.angle() equals atan2(y, x)  (docs: "equivalent to calling @GlobalScope.atan2() with y and x")
	var worst_d := 0.0
	for v in [Vector2(1, 0), Vector2(0, 1), Vector2(-1, 0.001), Vector2(-1, -0.001), Vector2(0.3, -0.7), Vector2(-0.6, 0.2)]:
		worst_d = maxf(worst_d, absf(v.angle() - atan2(v.y, v.x)))
	out("D-angle-equals-atan2", {"largest_difference": worst_d})

	# E. The by-hand example shown on screen: distance 0.6, angle 30 degrees
	var a30 := deg_to_rad(30.0)
	out("E-worked-example", {"angle_radians": a30, "PI/6": PI / 6.0, "across_0.6cos": 0.6 * cos(a30), "second_0.6sin": 0.6 * sin(a30),
		"uv_x": (0.6 * cos(a30) + 1.0) / 2.0, "uv_y": (0.6 * sin(a30) + 1.0) / 2.0})

	# F. The degrees/radians trap: 30 read as radians
	out("F-thirty-radians", {"turns": 30.0 / TAU, "fraction_of_last_turn": fposmod(30.0, TAU) / TAU, "angle_in_degrees_mod_360": fposmod(rad_to_deg(30.0), 360.0),
		"sin_30_as_radians": sin(30.0), "cos_30_as_radians": cos(30.0), "sin_30_degrees": sin(deg_to_rad(30.0)), "cos_30_degrees": cos(deg_to_rad(30.0))})

	# G. Right-triangle ratios depend only on the angle: sizes from 1 to 1000 at 30 and 50 degrees
	var spread30 := 0.0
	var spread50 := 0.0
	for hyp in [1.0, 2.0, 7.5, 20.0, 100.0, 1000.0]:
		spread30 = maxf(spread30, absf(hyp * sin(deg_to_rad(30.0)) / hyp - 0.5))
		spread50 = maxf(spread50, absf(hyp * sin(deg_to_rad(50.0)) / hyp - sin(deg_to_rad(50.0))))
	out("G-ratio-does-not-depend-on-size", {"opposite_over_hypotenuse_at_30": 0.5, "largest_error_30": spread30, "sin_50_degrees": sin(deg_to_rad(50.0)),
		"largest_error_50": spread50, "cos_30": cos(deg_to_rad(30.0)), "tan_30": tan(deg_to_rad(30.0))})

	# H. Cosine is sine a quarter turn earlier: cos(x) == sin(x + PI/2)
	var worst_h := 0.0
	for x in [0.0, 0.4, 1.0, 2.2, 3.5, 5.0, -1.3]:
		worst_h = maxf(worst_h, absf(cos(x) - sin(x + PI / 2.0)))
	out("H-cosine-is-shifted-sine", {"largest_difference": worst_h})

	# I. Radian: the arc equal to the radius; a full turn is a little over six radii
	out("I-radian", {"TAU": TAU, "radii_in_a_full_turn": TAU, "whole_radii": int(TAU), "leftover": TAU - int(TAU), "PI": PI, "radians_of_45": deg_to_rad(45.0), "PI/4": PI / 4.0})

	# J. Sine wave landmarks: sin at 0, quarter turn, half turn, three-quarter turn, full turn
	out("J-sine-landmarks", {"sin_0": sin(0.0), "sin_PI/2": sin(PI / 2.0), "sin_PI": snappedf(sin(PI), 0.0000001), "sin_3PI/2": sin(3.0 * PI / 2.0), "sin_TAU": snappedf(sin(TAU), 0.0000001),
		"cos_0": cos(0.0), "cos_PI/2": snappedf(cos(PI / 2.0), 0.0000001), "cos_PI": cos(PI)})

	# K. The three-moon spacing: a third of a turn
	out("K-third-of-a-turn", {"TAU/3": TAU / 3.0, "degrees": rad_to_deg(TAU / 3.0)})

	# L. atan2 landmarks used on screen (y first, then x), screen orientation (y down)
	out("L-atan2-landmarks", {"right(0,1)": atan2(0.0, 1.0), "down(1,0)": atan2(1.0, 0.0), "left_below(+0.001,-1)": atan2(0.001, -1.0), "left_above(-0.001,-1)": atan2(-0.001, -1.0),
		"up(-1,0)": atan2(-1.0, 0.0), "one_arg_atan(1/1)": atan(1.0), "one_arg_atan(-1/-1)": atan((-1.0) / (-1.0)), "two_arg(1,1)": atan2(1.0, 1.0), "two_arg(-1,-1)": atan2(-1.0, -1.0)})
	quit(0)

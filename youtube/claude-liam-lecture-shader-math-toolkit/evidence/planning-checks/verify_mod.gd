extends SceneTree
# GDScript side of the "mod" trap: the film says a shader's mod(-0.25, 1.0) is 0.75 (it follows floor), while GDScript's fmod keeps the
# sign of the first number (-0.25) and fposmod matches the shader (0.75). Prints one RESULT line per check.
# Run (non-GPU, no window): godot --headless --path <scratch project> --script res://verify_mod.gd
func _initialize() -> void:
	call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func run() -> void:
	var xs := [-0.25, 0.25, 1.25, -1.25, 2.75]
	var rows := []
	for x in xs:
		rows.append({"x": x, "fmod_x_1": fmod(x, 1.0), "fposmod_x_1": fposmod(x, 1.0), "x_minus_floor_x": x - floor(x)})
	out("M-gdscript-fmod-vs-fposmod", {"engine": Engine.get_version_info()["string"], "rows": rows,
		"reading": "fmod keeps the sign of x; fposmod and x - floor(x) give the shader's mod(x, 1.0) (0.75 for -0.25)"})
	# lerp does not clamp its weight either (docs: values outside 0..1 extrapolate), same as the shader mix()
	out("L-lerp-extrapolates", {"lerp_0.2_0.4_w2": lerp(0.2, 0.4, 2.0), "lerp_0.2_0.4_w-1": lerp(0.2, 0.4, -1.0),
		"reading": "same numbers as the shader mix(0.2, 0.4, w): 0.6 and 0.0"})
	quit(0)

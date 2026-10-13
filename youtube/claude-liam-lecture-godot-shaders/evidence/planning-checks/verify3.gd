extends SceneTree
# Claims about uniforms, checked in a real window of Godot 4.7.2:
#  F: a hint_range does not clamp a value set from code (stored value comes back unchanged)
#  G: a misspelled uniform name is a silent no-op (no error, picture unchanged)
#  H: a Tween on "shader_parameter/<name>" animates the uniform (picture changes over time)
# Run: godot --path <project dir> --script res://verify3.gd

const DIAL := "shader_type canvas_item;\nuniform float red : hint_range(0.0, 1.0) = 0.2;\nvoid fragment() { COLOR = vec4(red, 0.0, 0.0, 1.0); }\n"

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func frames(n: int) -> void:
	for i in range(n): await process_frame

func red_at_center() -> float:
	RenderingServer.force_draw(false)
	var img := root.get_texture().get_image()
	return img.get_pixel(img.get_width() / 2, img.get_height() / 2).r

func run() -> void:
	root.size = Vector2i(320, 180)
	var rect := ColorRect.new()
	rect.size = Vector2(320, 180)
	var sh := Shader.new()
	sh.code = DIAL
	var mat := ShaderMaterial.new()
	mat.shader = sh
	rect.material = mat
	root.add_child(rect)
	await frames(3)
	var base := red_at_center()

	# F: hint does not clamp
	mat.set_shader_parameter("red", 7.0)
	out("F-hint-does-not-clamp", {"stored_after_set_7": mat.get_shader_parameter("red"), "hint": "hint_range(0.0, 1.0)"})

	# G: typo is silent
	mat.set_shader_parameter("red", 0.2)
	await frames(2)
	var before := red_at_center()
	mat.set_shader_parameter("rd", 0.9)           # misspelled
	await frames(2)
	var after_typo := red_at_center()
	mat.set_shader_parameter("red", 0.9)          # correct
	await frames(2)
	var after_ok := red_at_center()
	out("G-typo-is-silent", {"red_before": before, "red_after_typo_rd_0.9": after_typo, "red_after_correct_red_0.9": after_ok,
		"rd_stored_as_unused_param": mat.get_shader_parameter("rd"), "baseline_first_frame": base})

	# H: tween the uniform through its property path
	mat.set_shader_parameter("red", 0.0)
	await frames(2)
	var t0 := red_at_center()
	var tw := create_tween()
	tw.tween_property(mat, "shader_parameter/red", 1.0, 0.5)
	await create_timer(0.25).timeout
	var mid := red_at_center()
	await tw.finished
	await frames(2)
	var end := red_at_center()
	out("H-tween-shader-parameter", {"start": t0, "mid": mid, "end": end, "path": "shader_parameter/red"})
	quit(0)

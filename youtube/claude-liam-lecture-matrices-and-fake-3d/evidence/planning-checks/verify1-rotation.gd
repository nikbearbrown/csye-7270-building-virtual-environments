extends SceneTree
# Claims about turning, checked in a real window of Godot 4.7.2 (non-headless):
#  R1: a sprite turned by the shader table (angle 0.5236) draws the same pixels as a sprite turned by Godot's own Node2D.rotation = 0.5236
#      (so a positive shader angle turns the same way Godot does: clockwise on screen, y pointing down)
#  R2: Transform2D(rotation, origin) keeps the turn in its x and y columns and the slide in origin (the table Godot keeps for every 2D node)
#  R3: Vector2.RIGHT.rotated(PI / 2) lands on (0, 1), which is DOWN on screen
# Run: godot --path <project dir> --script res://verify1-rotation.gd
const TURN := "shader_type canvas_item;\nuniform float angle = 0.0;\nvoid vertex() {\n\tvec2 across = vec2(cos(angle), sin(angle));\n\tvec2 down = vec2(-sin(angle), cos(angle));\n\tVERTEX = mat2(across, down) * VERTEX;\n}\n"

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func frames(n: int) -> void:
	for i in range(n): await process_frame

func gradient_texture() -> ImageTexture:
	var img := Image.create(128, 128, false, Image.FORMAT_RGBA8)
	for y in 128:
		for x in 128:
			img.set_pixel(x, y, Color(x / 127.0, y / 127.0, 0.0, 1.0))
	return ImageTexture.create_from_image(img)


func compare() -> Array:
	RenderingServer.force_draw(false)
	var img := root.get_texture().get_image()
	var stage := Color("#D9D5CA")
	var maxdiff := 0.0
	var n_over := 0
	var n := 0
	var nl := 0
	var nr := 0
	for y in range(60, 300):
		for x in range(40, 280):
			var ca := img.get_pixel(x, y)
			var cb := img.get_pixel(x + 320, y)
			var d := maxf(maxf(absf(ca.r - cb.r), absf(ca.g - cb.g)), absf(ca.b - cb.b))
			maxdiff = maxf(maxdiff, d)
			n += 1
			if d > 0.02: n_over += 1
			if absf(ca.r - stage.r) + absf(ca.g - stage.g) + absf(ca.b - stage.b) > 0.1: nl += 1
			if absf(cb.r - stage.r) + absf(cb.g - stage.g) + absf(cb.b - stage.b) > 0.1: nr += 1
	return [n, maxdiff, n_over, nl, nr]

func run() -> void:
	root.size = Vector2i(640, 360)
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	var tex := gradient_texture()
	var node_turned := Sprite2D.new()
	node_turned.texture = tex
	node_turned.position = Vector2(160, 180)
	node_turned.rotation = 0.5236
	var shader_turned := Sprite2D.new()
	shader_turned.texture = tex
	shader_turned.position = Vector2(480, 180)
	var sh := Shader.new()
	sh.code = TURN
	var mat := ShaderMaterial.new()
	mat.shader = sh
	mat.set_shader_parameter("angle", 0.5236)
	shader_turned.material = mat
	root.add_child(node_turned)
	root.add_child(shader_turned)
	await frames(4)
	var same := compare()
	out("R1-shader-turn-equals-node-rotation", {"angle": 0.5236, "pixels_compared": same[0], "sprite_pixels_left": same[3], "sprite_pixels_right": same[4], "max_channel_difference": snappedf(same[1], 0.0001),
		"pixels_differing_by_more_than_0.02": same[2], "reading": "left sprite uses Node2D.rotation, right sprite uses the 2x2 table in vertex(); equal pixels mean the same direction and the same angle"})
	# negative control: the opposite angle must NOT match, otherwise the comparison proves nothing
	mat.set_shader_parameter("angle", -0.5236)
	await frames(3)
	var ctrl := compare()
	out("R1b-control-opposite-angle-differs", {"angle": -0.5236, "max_channel_difference": snappedf(ctrl[1], 0.0001), "pixels_differing_by_more_than_0.02": ctrl[2],
		"reading": "the opposite angle gives a different picture, so the equal result above is a real match"})

	var t := Transform2D(0.5236, Vector2(100, 0))
	out("R2-transform2d-columns", {"x_column": [snappedf(t.x.x, 0.0001), snappedf(t.x.y, 0.0001)], "y_column": [snappedf(t.y.x, 0.0001), snappedf(t.y.y, 0.0001)], "origin": [t.origin.x, t.origin.y],
		"cos_sin_of_angle": [snappedf(cos(0.5236), 0.0001), snappedf(sin(0.5236), 0.0001)], "reading": "x column = (cos, sin); y column = (-sin, cos); slide = origin"})
	var r := Vector2.RIGHT.rotated(PI / 2.0)
	out("R3-rotated-points-down", {"RIGHT.rotated(PI/2)": [snappedf(r.x, 0.0001), snappedf(r.y, 0.0001)], "reading": "(0, 1): positive y is down on screen, so the quarter turn is clockwise"})
	quit(0)

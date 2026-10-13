extends SceneTree
# Two claims about what vertex() works on, checked in a real window of Godot 4.7.2 (non-headless):
#  O1: VERTEX is measured in pixels from the node's origin. For a centred Sprite2D the origin is the middle, so VERTEX.x runs -64 to 64 on a
#      128 pixel sprite; for a Sprite2D with centered = false the origin is the top left corner, so VERTEX.x runs 0 to 128.
#      Test: VERTEX.x *= 2.0 doubles the distance from the ORIGIN, so the centred sprite grows both ways and the other one grows to the right only.
#  V1: a plain Sprite2D is drawn from its four corners: a sine ripple added in vertex() does NOT bend the top edge; the edge stays a straight
#      line between the two moved corners (the interior points are interpolated, not calculated).
# Run: godot --path <project dir> --script res://verify2-origin-and-corners.gd
const DOUBLE_X := "shader_type canvas_item;\nvoid vertex() {\n\tVERTEX.x *= 2.0;\n}\n"
const RIPPLE := "shader_type canvas_item;\nvoid vertex() {\n\tVERTEX.y += 30.0 * sin(VERTEX.x * 0.2);\n}\n"

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func frames(n: int) -> void:
	for i in range(n): await process_frame

func white_texture() -> ImageTexture:
	var img := Image.create(128, 128, false, Image.FORMAT_RGBA8)
	img.fill(Color.WHITE)
	return ImageTexture.create_from_image(img)

func shader_material(code: String) -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = code
	var m := ShaderMaterial.new()
	m.shader = sh
	return m

func is_sprite(c: Color) -> bool:
	return c.r > 0.97 and c.g > 0.97 and c.b > 0.97

func x_extent(img: Image, x_from: int, x_to: int) -> Array:
	var lo := 100000
	var hi := -1
	for y in range(0, img.get_height()):
		for x in range(x_from, x_to):
			if is_sprite(img.get_pixel(x, y)):
				lo = mini(lo, x)
				hi = maxi(hi, x + 1)
	return [lo, hi]

func top_edge_y(img: Image, x: int) -> int:
	for y in range(0, img.get_height()):
		if is_sprite(img.get_pixel(x, y)): return y
	return -1

func run() -> void:
	root.size = Vector2i(640, 360)
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	var tex := white_texture()
	var centred := Sprite2D.new()
	centred.texture = tex
	centred.position = Vector2(160, 180)
	centred.material = shader_material(DOUBLE_X)
	var corner := Sprite2D.new()
	corner.texture = tex
	corner.centered = false
	corner.position = Vector2(330, 116)
	corner.material = shader_material(DOUBLE_X)
	root.add_child(centred)
	root.add_child(corner)
	await frames(4)
	RenderingServer.force_draw(false)
	var img := root.get_texture().get_image()
	var a := x_extent(img, 0, 310)
	var b := x_extent(img, 310, 640)
	out("O1-origin-is-the-middle-only-when-centred", {"centred_sprite_at_x_160": {"x_from": a[0], "x_to": a[1], "relative_to_node": [a[0] - 160, a[1] - 160]},
		"not_centred_sprite_at_x_330": {"x_from": b[0], "x_to": b[1], "relative_to_node": [b[0] - 330, b[1] - 330]},
		"reading": "centred: -128..128 (doubled from -64..64). not centred: 0..256 (doubled from 0..128), so its origin is its left edge"})
	centred.queue_free()
	corner.queue_free()
	await frames(2)

	var rip := Sprite2D.new()
	rip.texture = tex
	rip.position = Vector2(320, 180)
	rip.material = shader_material(RIPPLE)
	root.add_child(rip)
	await frames(4)
	RenderingServer.force_draw(false)
	var img2 := root.get_texture().get_image()
	var rows: Array = []
	for rel in [-60, -30, 0, 30, 60]:
		var measured := top_edge_y(img2, 320 + rel) - 180
		var linear := -64.0 + 30.0 * sin(64.0 * 0.2) * (rel / 64.0)     # straight line between the two moved top corners
		var sine := -64.0 + 30.0 * sin(rel * 0.2)                      # what a calculation at every pixel would give
		rows.append({"x_rel": rel, "top_edge_y_measured": measured, "straight_line_prediction": snappedf(linear, 0.1), "sine_prediction": snappedf(sine, 0.1)})
	out("V1-top-edge-stays-straight", {"rows": rows, "reading": "measured values follow the straight-line column, not the sine column: only the four corners were moved"})
	quit(0)

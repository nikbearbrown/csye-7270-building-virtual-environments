extends SceneTree
# Check 6: COLOR in vertex(). Docs: in vertex(), COLOR is the vertex colour times the CanvasItem's modulate times self_modulate;
# in fragment(), the incoming COLOR is that times the texture. So darkening COLOR in vertex() should reach the picture, and assigning it should drop the modulate.
# A white 128 px sprite with modulate (0.2, 0.9, 0.2) is drawn four ways; the centre pixel is read.
const V = preload("res://vscene.gd")

func _initialize() -> void:
	call_deferred("run")

func centre(img: Image, x: int, y: int) -> Array:
	var c := img.get_pixel(x, y)
	return [snappedf(c.r, 0.001), snappedf(c.g, 0.001), snappedf(c.b, 0.001)]

func run() -> void:
	V.setup(root, 640, 360)
	var white := V.white_image(128, 128)
	var variants := [
		["no_shader", null, Color(0.2, 0.9, 0.2), Color.WHITE],
		["vertex: COLOR.rgb *= 0.5", V.check_shader("c9-color-halve"), Color(0.2, 0.9, 0.2), Color.WHITE],
		["vertex: COLOR = vec4(1.0)", V.check_shader("c9-color-replace"), Color(0.2, 0.9, 0.2), Color.WHITE],
		["vertex: COLOR.rgb *= 0.5 with self_modulate (0.2,0.9,0.2)", V.check_shader("c9-color-halve"), Color.WHITE, Color(0.2, 0.9, 0.2)],
	]
	var xs := [100, 240, 380, 520]
	for i in range(variants.size()):
		var v: Array = variants[i]
		var sp := V.sprite(white, Vector2(xs[i], 180), 1.0)
		sp.modulate = v[2]
		sp.self_modulate = v[3]
		if v[1] != null:
			sp.material = V.material_from(v[1])
		root.add_child(sp)
	await V.frames(self, 4)
	var im := V.grab(root)
	im.save_png(V.png_dir() + "/verify6-color.png")
	for i in range(variants.size()):
		V.out("6-color-in-vertex", {"variant": variants[i][0], "modulate": [variants[i][2].r, variants[i][2].g, variants[i][2].b], "centre_pixel": centre(im, xs[i], 180)})
	quit(0)

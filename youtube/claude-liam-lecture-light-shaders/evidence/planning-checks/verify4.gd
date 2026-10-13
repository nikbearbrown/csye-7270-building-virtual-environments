extends SceneTree
# verify4: where light() lives and what it can read.
#  O: two sprites, one light: a light() on one sprite does not change the other (the function belongs to the thing being lit).
#  U: UV can be read in light().   C: COLOR in light() is what fragment() produced.
#  R: render_mode unshaded (skips light() and ignores the dusk tint?) and light_only (visible only where a light reaches).
#  N: light() runs once per light, results add (ambient 0.2 + constant 0.2 per light), counted with 0, 1, 2, 3 lights.
# Run: godot --path <project dir> --script res://verify4.gd
const LL := preload("res://lightlab.gd")

func _initialize() -> void: call_deferred("run")
func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))
func frames(n: int) -> void:
	for i in range(n): await process_frame
func grab() -> Image:
	RenderingServer.force_draw(false)
	var im := root.get_texture().get_image()
	im.convert(Image.FORMAT_RGBA8)
	return im
func clear() -> void:
	for c in root.get_children(): c.queue_free()
	await frames(2)
func code(body: String, extra: String = "", head: String = "shader_type canvas_item;\n") -> String:
	return head + extra + "void light() {\n\t" + body + "\n}\n"

func run() -> void:
	root.size = Vector2i(320, 180)
	var soft := LL.radial_tex(256)
	var white := LL.solid_tex(Color.WHITE, 128)
	var grey := LL.solid_tex(Color(0.6, 0.6, 0.6), 64)

	# ---- O: ownership. Left sprite default, right sprite wears light(){ LIGHT = vec4(0.0,0.0,0.0,1.0) } (a light that adds nothing), one light between them.
	await clear()
	root.add_child(LL.canvas_mod(Color(0.2, 0.2, 0.2)))
	root.add_child(LL.sprite(grey, Vector2(80, 90), Vector2(1.5, 1.5)))
	root.add_child(LL.sprite(grey, Vector2(240, 90), Vector2(1.5, 1.5), LL.shader_mat(code(""))))
	root.add_child(LL.point_light(Vector2(160, 90), white, 4.0, 0.8))
	await frames(4)
	var im := grab()
	out("O-two-sprites-one-light", {"left_default_centre": LL.px(im, 80, 90), "right_empty_light_centre": LL.px(im, 240, 90),
		"reading": "ambient only would be 0.6*0.2=0.12; default lit is 0.6*(0.2+0.8)=0.60"})

	# ---- U: UV in light()  and  C: COLOR from fragment ----
	await clear()
	root.add_child(LL.canvas_mod(Color.BLACK))
	var uv_code := code("LIGHT = vec4(UV.x, UV.y, 0.0, 1.0);")
	root.add_child(LL.sprite(LL.solid_tex(Color.WHITE, 64), Vector2(160, 90), Vector2(3, 2), LL.shader_mat(uv_code)))
	root.add_child(LL.point_light(Vector2(160, 90), white, 4.0, 1.0))
	await frames(4)
	im = grab()
	# sprite spans x 64..256, y 26..154
	out("U-uv-in-light", {"top_left_of_sprite": LL.px(im, 68, 30), "top_right": LL.px(im, 252, 30), "bottom_left": LL.px(im, 68, 150), "bottom_right": LL.px(im, 252, 150),
		"reading": "if UV works in light(): black, red, green, yellow corners (like fragment)"})
	await clear()
	root.add_child(LL.canvas_mod(Color.BLACK))
	var fc_code := "shader_type canvas_item;\nvoid fragment() { COLOR = vec4(0.0, 0.8, 0.0, 1.0); }\nvoid light() { LIGHT = vec4(COLOR.rgb, 1.0); }\n"
	root.add_child(LL.sprite(LL.solid_tex(Color(0.9, 0.1, 0.1), 64), Vector2(160, 90), Vector2(2, 2), LL.shader_mat(fc_code)))
	root.add_child(LL.point_light(Vector2(160, 90), white, 4.0, 1.0))
	await frames(4)
	out("C-color-in-light-is-fragment-output", {"centre": LL.px(grab(), 160, 90), "reading": "texture is red (0.9,0.1,0.1); fragment() sets COLOR to green (0,0.8,0); light() returns COLOR.rgb. Green = COLOR in light() is fragment's output"})

	# ---- R: render modes. Sprite colour (0.6,0.3,0.9), dusk 0.2, one light on it.
	var sc := Color(0.6, 0.3, 0.9)
	var render_cases := {
		"normal-default": "",
		"light-written": "shader_type canvas_item;\nvoid light() { LIGHT = vec4(0.1, 0.1, 0.1, 1.0); }\n",
		"unshaded": "shader_type canvas_item;\nrender_mode unshaded;\nvoid light() { LIGHT = vec4(0.1, 0.1, 0.1, 1.0); }\n",
		"unshaded-no-light-fn": "shader_type canvas_item;\nrender_mode unshaded;\nvoid fragment() { }\n",
		"light_only-default-light": "shader_type canvas_item;\nrender_mode light_only;\nvoid fragment() { }\n",
	}
	for k in render_cases:
		for lit in [true, false]:
			await clear()
			root.add_child(LL.canvas_mod(Color(0.2, 0.2, 0.2)))
			root.add_child(LL.sprite(LL.solid_tex(sc, 64), Vector2(160, 90), Vector2(2, 2), LL.shader_mat(render_cases[k]) if render_cases[k] != "" else null))
			if lit:
				root.add_child(LL.point_light(Vector2(160, 90), white, 4.0, 0.5))
			await frames(4)
			var cc := grab().get_pixel(160, 90)
			out("R-" + k + ("-with-light" if lit else "-no-light"), {"centre_rgb": [snappedf(cc.r, 0.001), snappedf(cc.g, 0.001), snappedf(cc.b, 0.001)], "stage_behind_is": "clear colour"})

	# ---- N: light count with a non-black ambient ----
	await clear()
	root.add_child(LL.canvas_mod(Color(0.2, 0.2, 0.2)))
	root.add_child(LL.sprite(LL.solid_tex(Color(1, 1, 1), 64), Vector2(160, 90), Vector2(2, 2), LL.shader_mat(code("LIGHT = vec4(0.2, 0.2, 0.2, 1.0);"))))
	await frames(3)
	var counts := [grab().get_pixel(160, 90).r]
	var lights: Array = []
	for n in range(1, 5):
		var l := LL.point_light(Vector2(160, 90), white, 4.0, 1.0)
		root.add_child(l)
		lights.append(l)
		await frames(3)
		counts.append(grab().get_pixel(160, 90).r)
	out("N-light-count-ambient0.2-const0.2", {"red_by_light_count_0_to_4": counts.map(func(v): return snappedf(v, 0.001)), "reading": "white surface: ambient 0.2 then +0.2 per light (0.2, 0.4, 0.6, 0.8, 1.0)"})
	quit(0)

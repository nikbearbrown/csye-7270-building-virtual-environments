extends SceneTree
# verify7: (a) the multi-line rebuild equals the one-line rebuild and the default; (b) the docs' normal-map version of light() vs the default on a dome normal map;
# (c) banded light (floor of the falloff); (d) a soft beam edge with smoothstep; (e) the numbers for "surface 0.5, ambient 0.2, lamps 0.4": one, two, three lamps.
# Run: godot --path <project dir> --script res://verify7.gd
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

func diff(a: Image, b: Image) -> Dictionary:
	var maxd := 0.0
	var cnt := 0
	for y in a.get_height():
		for x in a.get_width():
			var ca := a.get_pixel(x, y)
			var cb := b.get_pixel(x, y)
			var d := maxf(maxf(absf(ca.r - cb.r), absf(ca.g - cb.g)), absf(ca.b - cb.b))
			maxd = maxf(maxd, d)
			if d > 0.004: cnt += 1
	return {"max_abs_diff": snappedf(maxd, 0.001), "pixels_differing_by_more_than_1_of_255": cnt}

func gradient_surface() -> ImageTexture:
	var im := Image.create(320, 180, false, Image.FORMAT_RGBA8)
	for y in 180:
		for x in 320:
			var t := x / 319.0
			im.set_pixel(x, y, Color(0.9 - 0.7 * t, 0.5, 0.2 + 0.7 * t, 1.0))
	return ImageTexture.create_from_image(im)

func dome_normal() -> ImageTexture:
	var im := Image.create(320, 180, false, Image.FORMAT_RGBA8)
	var cx := 160.0
	var cy := 90.0
	var R := 88.0
	for y in 180:
		for x in 320:
			var nx := (x - cx) / R
			var ny := (y - cy) / R
			var r2 := nx * nx + ny * ny
			var n := Vector3(0, 0, 1)
			if r2 < 1.0:
				n = Vector3(nx, ny, sqrt(1.0 - r2))
			im.set_pixel(x, y, Color(n.x * 0.5 + 0.5, n.y * 0.5 + 0.5, n.z * 0.5 + 0.5, 1.0))
	return ImageTexture.create_from_image(im)

func render(code: String, surface: Texture2D, lights: Array, ambient: Color, extra: Callable = Callable()) -> Image:
	await clear()
	root.add_child(LL.canvas_mod(ambient))
	var mat: ShaderMaterial = LL.shader_mat(code) if code != "" else null
	var spr := LL.sprite(surface, Vector2(160, 90), Vector2.ONE, mat)
	root.add_child(spr)
	for l in lights: root.add_child(l)
	if extra.is_valid(): extra.call(root, spr)
	await frames(5)
	return grab()

func run() -> void:
	root.size = Vector2i(320, 180)
	var surf := gradient_surface()
	var soft := LL.radial_tex(256)
	var mk_lights := func() -> Array:
		return [LL.point_light(Vector2(120, 90), soft, 1.0, 1.4, Color(1.0, 0.9, 0.7)), LL.point_light(Vector2(210, 100), soft, 0.8, 1.0, Color(0.4, 0.7, 1.0))]
	var amb := Color(0.25, 0.27, 0.35)
	var base: Image = await render("", surf, mk_lights.call(), amb)

	# (a) three-line rebuild
	var three := "shader_type canvas_item;\n\nvoid light() {\n\tvec3 rgb = COLOR.rgb * LIGHT_COLOR.rgb * LIGHT_ENERGY;\n\tLIGHT = vec4(rgb, LIGHT_COLOR.a);\n}\n"
	var im: Image = await render(three, surf, mk_lights.call(), amb)
	var d1 := diff(base, im)
	out("A-three-line-rebuild-vs-default", d1)

	# (b) normal map on a dome, lights raised to height 100
	var ct := CanvasTexture.new()
	ct.diffuse_texture = surf
	ct.normal_texture = dome_normal()
	var tall := func() -> Array:
		var a := LL.point_light(Vector2(120, 90), soft, 1.0, 1.4, Color(1.0, 0.9, 0.7), 100.0)
		var b := LL.point_light(Vector2(210, 100), soft, 0.8, 1.0, Color(0.4, 0.7, 1.0), 100.0)
		return [a, b]
	var docs_code := "shader_type canvas_item;\n\nvoid light() {\n\tfloat cNdotL = max(0.0, dot(NORMAL, LIGHT_DIRECTION));\n\tLIGHT = vec4(LIGHT_COLOR.rgb * COLOR.rgb * LIGHT_ENERGY * cNdotL, LIGHT_COLOR.a);\n}\n"
	var nbase: Image = await render("", ct, tall.call(), amb)
	var nreb: Image = await render(three, ct, tall.call(), amb)
	var ndocs: Image = await render(docs_code, ct, tall.call(), amb)
	var dd := diff(nbase, ndocs)
	dd["default_vs_one_line_rebuild"] = diff(nbase, nreb)
	dd["centre_default_rebuild_docs"] = [LL.px(nbase, 150, 60), LL.px(nreb, 150, 60), LL.px(ndocs, 150, 60)]
	out("B-docs-normal-map-version-vs-default", dd)
	# flat vs dome sanity: does the normal map change the default at all?
	var nflat: Image = await render("", surf, tall.call(), amb)
	out("B2-normal-map-changes-the-default", diff(nflat, nbase))

	# (c) banded light: the soft edge (alpha) rounded down to quarters. Probe along +x from lamp a at (120,90): alpha falls linearly from 1 at the centre to 0 at 128 px.
	var band := "shader_type canvas_item;\n\nvoid light() {\n\tfloat bands = floor(LIGHT_COLOR.a * 4.0) / 4.0;\n\tLIGHT = vec4(COLOR.rgb * LIGHT_COLOR.rgb * LIGHT_ENERGY, bands);\n}\n"
	var one := func() -> Array: return [LL.point_light(Vector2(160, 90), soft, 1.0, 1.0, Color.WHITE)]
	var wsurf := LL.solid_tex(Color(0.5, 0.5, 0.5), 64)
	var big := func(r, s): s.scale = Vector2(5, 3)
	var plain: Image = await render("", wsurf, one.call(), Color(0.2, 0.2, 0.2), big)
	var banded: Image = await render(band, wsurf, one.call(), Color(0.2, 0.2, 0.2), big)
	var pr := []
	var br := []
	for d in [0, 16, 32, 48, 64, 80, 96, 112, 124]:
		pr.append(snappedf(plain.get_pixel(160 + d, 90).r, 0.001))
		br.append(snappedf(banded.get_pixel(160 + d, 90).r, 0.001))
	out("C-banded-light", {"distance_from_lamp_px": [0, 16, 32, 48, 64, 80, 96, 112, 124], "smooth_default_red": pr, "banded_red": br, "reading": "grey 0.5 surface, ambient 0.2, white lamp energy 1: smooth = 0.5*(0.2+alpha); banded = 0.5*(0.2+floor(alpha*4)/4)"})

	# (d) soft beam edge: smoothstep(0.90, 0.99, dot) vs step(0.95, dot) as a function of the angle from the aim
	var tex_lines := "shader_type canvas_item;\nuniform float a = 0.0;\nuniform int soft_edge = 0;\nvoid light() {\n\tvec2 aim = vec2(cos(a), sin(a));\n\tfloat agree = dot(-LIGHT_DIRECTION.xy, aim);\n\tfloat m = soft_edge == 1 ? smoothstep(0.90, 0.99, agree) : step(0.95, agree);\n\tLIGHT = vec4(vec3(m), 1.0);\n}\n"
	var sres := {}
	for se in [0, 1]:
		await clear()
		root.add_child(LL.canvas_mod(Color.BLACK))
		var fs := LL.sprite(LL.solid_tex(Color.WHITE, 64), Vector2(160, 90), Vector2(6, 6), LL.shader_mat(tex_lines))
		(fs.material as ShaderMaterial).set_shader_parameter("soft_edge", se)
		root.add_child(fs)
		root.add_child(LL.point_light(Vector2(160, 90), LL.solid_tex(Color.WHITE, 128), 4.0, 1.0))
		await frames(4)
		var im2 := grab()
		var vals := []
		for deg in [0, 5, 10, 15, 18, 20, 25, 30]:
			var p := Vector2(160, 90) + 70.0 * Vector2(cos(deg_to_rad(deg)), sin(deg_to_rad(deg)))
			vals.append(snappedf(im2.get_pixel(int(p.x), int(p.y)).r, 0.01))
		sres["soft" if se == 1 else "hard"] = vals
	out("D-beam-edge-hard-vs-soft", {"degrees_off_aim": [0, 5, 10, 15, 18, 20, 25, 30], "mask": sres, "reading": "step(0.95) cuts at acos(0.95)=18.2 deg; smoothstep(0.90,0.99) fades between acos(0.99)=8.1 and acos(0.90)=25.8 deg"})

	# (e) the numbers for the formula beat: grey surface 0.5, ambient 0.2, solid white lamps of energy 0.4: 0, 1, 2, 3 lamps
	await clear()
	root.add_child(LL.canvas_mod(Color(0.2, 0.2, 0.2)))
	root.add_child(LL.sprite(LL.solid_tex(Color(0.5, 0.5, 0.5), 64), Vector2(160, 90), Vector2(5, 3)))
	await frames(3)
	var counts := [grab().get_pixel(160, 90).r]
	var white := LL.solid_tex(Color.WHITE, 128)
	for n in range(1, 4):
		root.add_child(LL.point_light(Vector2(160, 90), white, 4.0, 0.4))
		await frames(3)
		counts.append(grab().get_pixel(160, 90).r)
	out("E-formula-numbers", {"red_by_lamp_count_0_to_3": counts.map(func(v): return snappedf(v, 0.001)), "expected": [0.1, 0.3, 0.5, 0.7], "formula": "0.5 * (0.2 + 0.4 n)"})
	quit(0)

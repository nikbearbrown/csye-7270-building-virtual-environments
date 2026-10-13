extends SceneTree
# verify3: does the one-line rebuilt light() match Godot's default lighting? Same scene rendered twice (no light() vs. rebuilt), compared pixel for pixel.
# Scene: a 320x180 sprite with a left-to-right colour gradient, dusk CanvasModulate, two coloured point lights with a soft radial texture.
# Then variants that change one thing (alpha forced to 1, no energy, no surface colour), and the two things the rebuild might miss: normal maps and shadows.
# Run: godot --path <project dir> --script res://verify3.gd
const LL := preload("res://lightlab.gd")
const DEFAULT_CODE := ""
const REBUILT := "shader_type canvas_item;\nvoid light() {\n\tLIGHT = vec4(COLOR.rgb * LIGHT_COLOR.rgb * LIGHT_ENERGY, LIGHT_COLOR.a);\n}\n"

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

func gradient_surface() -> ImageTexture:
	var im := Image.create(320, 180, false, Image.FORMAT_RGBA8)
	for y in 180:
		for x in 320:
			var t := x / 319.0
			im.set_pixel(x, y, Color(0.9 - 0.7 * t, 0.5, 0.2 + 0.7 * t, 1.0))
	return ImageTexture.create_from_image(im)

func diff(a: Image, b: Image) -> Dictionary:
	var maxd := 0.0
	var cnt := 0
	var at := Vector2i.ZERO
	for y in a.get_height():
		for x in a.get_width():
			var ca := a.get_pixel(x, y)
			var cb := b.get_pixel(x, y)
			var d := maxf(maxf(absf(ca.r - cb.r), absf(ca.g - cb.g)), absf(ca.b - cb.b))
			if d > maxd:
				maxd = d
				at = Vector2i(x, y)
			if d > 0.004:
				cnt += 1
	return {"max_abs_diff": snappedf(maxd, 0.001), "pixels_differing_by_more_than_1_of_255": cnt, "worst_pixel": [at.x, at.y]}

# Build the scene and return the rendered image. extra(root, sprite) can add shadow casters etc.
func render(code: String, surface: Texture2D, extra: Callable = Callable()) -> Image:
	await clear()
	root.add_child(LL.canvas_mod(Color(0.25, 0.27, 0.35)))
	var mat: ShaderMaterial = LL.shader_mat(code) if code != "" else null
	var spr := LL.sprite(surface, Vector2(160, 90), Vector2.ONE, mat)
	root.add_child(spr)
	var soft := LL.radial_tex(256)
	var a := LL.point_light(Vector2(120, 90), soft, 1.0, 1.4, Color(1.0, 0.9, 0.7), 0.0)
	var b := LL.point_light(Vector2(210, 100), soft, 0.8, 1.0, Color(0.4, 0.7, 1.0), 0.0)
	root.add_child(a)
	root.add_child(b)
	if extra.is_valid():
		extra.call(root, spr, a, b)
	await frames(5)
	return grab()

func run() -> void:
	root.size = Vector2i(320, 180)
	var surf := gradient_surface()
	var base := await render("", surf)
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(), "image": [base.get_width(), base.get_height()]})
	var probes := [Vector2i(120, 90), Vector2i(60, 90), Vector2i(180, 60), Vector2i(210, 100), Vector2i(260, 140), Vector2i(10, 10), Vector2i(315, 175)]
	var base_vals := []
	for p in probes: base_vals.append(LL.px(base, p.x, p.y))
	out("R0-default-probes", {"probes_xy": probes.map(func(p): return [p.x, p.y]), "default_rgb": base_vals})

	var variants := {
		"R1-rebuilt-default": REBUILT,
		"R2-alpha-forced-to-1": "shader_type canvas_item;\nvoid light() {\n\tLIGHT = vec4(COLOR.rgb * LIGHT_COLOR.rgb * LIGHT_ENERGY, 1.0);\n}\n",
		"R3-no-energy": "shader_type canvas_item;\nvoid light() {\n\tLIGHT = vec4(COLOR.rgb * LIGHT_COLOR.rgb, LIGHT_COLOR.a);\n}\n",
		"R4-no-surface-colour": "shader_type canvas_item;\nvoid light() {\n\tLIGHT = vec4(LIGHT_COLOR.rgb * LIGHT_ENERGY, LIGHT_COLOR.a);\n}\n",
	}
	for k in variants:
		var im := await render(variants[k], surf)
		var vals := []
		for p in probes: vals.append(LL.px(im, p.x, p.y))
		var d := diff(base, im)
		d["rgb_at_probes"] = vals
		out(k, d)

	# --- normal map: default lighting reads it, a rebuilt light() ignores NORMAL ---
	var ni := Image.create(320, 180, false, Image.FORMAT_RGBA8)
	ni.fill(Color(0.8, 0.5, 0.85))   # normals leaning to one side
	var ct := CanvasTexture.new()
	ct.diffuse_texture = surf
	ct.normal_texture = ImageTexture.create_from_image(ni)
	var raise := func(r, s, a, b): a.height = 100.0; b.height = 100.0
	var nbase := await render("", ct, raise)
	var nreb := await render(REBUILT, ct, raise)
	var dn := diff(nbase, nreb)
	dn["default_vs_rebuilt_at_120_90"] = [LL.px(nbase, 120, 90), LL.px(nreb, 120, 90)]
	out("N-normal-map-default-vs-rebuilt", dn)

	# --- shadows: a square occluder between light a and the right side of the sprite ---
	var shadows := func(r, s, a, b):
		a.shadow_enabled = true
		var occ := LightOccluder2D.new()
		var poly := OccluderPolygon2D.new()
		poly.polygon = PackedVector2Array([Vector2(-14, -14), Vector2(14, -14), Vector2(14, 14), Vector2(-14, 14)])
		occ.occluder = poly
		occ.position = Vector2(160, 90)
		r.add_child(occ)
	var sbase := await render("", surf, shadows)
	var sreb := await render(REBUILT, surf, shadows)
	var ds := diff(sbase, sreb)
	ds["default_vs_rebuilt_in_shadow_at_190_90"] = [LL.px(sbase, 190, 90), LL.px(sreb, 190, 90)]
	ds["shadow_check_default_unshadowed_vs_shadowed_at_190_90"] = [LL.px(base, 190, 90), LL.px(sbase, 190, 90)]
	out("S-shadows-default-vs-rebuilt", ds)
	quit(0)

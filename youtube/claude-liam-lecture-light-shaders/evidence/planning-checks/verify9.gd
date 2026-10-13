extends SceneTree
# verify9: the film's own shader FILES (lab-shaders/) against Godot's default lighting, and the tween the film shows.
#  a) 03-light-default.gdshader vs default lighting: plain, with a shadow caster, with a normal map (also 18-normal-map-docs.gdshader).  320x180 test scene, two coloured soft lamps.
#  b) C04: brightness steps at the overlap of one, two, three lamps (1920x1080 capture scene).
#  c) the tween of B36 on the ring shader's `radius` uniform: set first, then tween (linear by default); and the failure when the uniform was never set.
# Run: godot --path <project dir> --script res://verify9.gd -- <lab-shaders dir> <captures.json>
const LL := preload("res://lightlab.gd")
const LS := preload("res://light_scene.gd")
var SH := ""
var CAPS := ""

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
func file_code(name: String) -> String:
	return FileAccess.get_file_as_string(SH.path_join(name))

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
	return {"max_abs_diff": snappedf(maxd, 0.001), "pixels_differing_by_more_than_1_of_255": cnt, "pixels": a.get_width() * a.get_height()}

func gradient_surface() -> ImageTexture:
	var im := Image.create(320, 180, false, Image.FORMAT_RGBA8)
	for y in 180:
		for x in 320:
			var t := x / 319.0
			im.set_pixel(x, y, Color(0.9 - 0.7 * t, 0.5, 0.2 + 0.7 * t, 1.0))
	return ImageTexture.create_from_image(im)

func dome_normal() -> ImageTexture:
	var im := Image.create(320, 180, false, Image.FORMAT_RGBA8)
	for y in 180:
		for x in 320:
			var nx := (x - 160.0) / 88.0
			var ny := (y - 90.0) / 88.0
			var r2 := nx * nx + ny * ny
			var n := Vector3(0, 0, 1)
			if r2 < 1.0:
				n = Vector3(nx, ny, sqrt(1.0 - r2))
			im.set_pixel(x, y, Color(n.x * 0.5 + 0.5, n.y * 0.5 + 0.5, n.z * 0.5 + 0.5, 1.0))
	return ImageTexture.create_from_image(im)

func render(code: String, surface: Texture2D, height: float, shadow: bool) -> Image:
	await clear()
	root.add_child(LL.canvas_mod(Color(0.25, 0.27, 0.35)))
	var spr := LL.sprite(surface, Vector2(160, 90), Vector2.ONE, LL.shader_mat(code) if code != "" else null)
	root.add_child(spr)
	var soft := LL.radial_tex(256)
	var a := LL.point_light(Vector2(120, 90), soft, 1.0, 1.4, Color(1.0, 0.9, 0.7), height)
	var b := LL.point_light(Vector2(210, 100), soft, 0.8, 1.0, Color(0.4, 0.7, 1.0), height)
	root.add_child(a)
	root.add_child(b)
	if shadow:
		a.shadow_enabled = true
		var occ := LightOccluder2D.new()
		var poly := OccluderPolygon2D.new()
		poly.polygon = PackedVector2Array([Vector2(-14, -14), Vector2(14, -14), Vector2(14, 14), Vector2(-14, 14)])
		occ.occluder = poly
		occ.position = Vector2(160, 90)
		root.add_child(occ)
	await frames(5)
	return grab()

func run() -> void:
	var args := OS.get_cmdline_user_args()
	SH = args[0]
	CAPS = args[1]
	root.size = Vector2i(320, 180)
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name()})
	var surf := gradient_surface()
	var dflt := file_code("03-light-default.gdshader")
	var docs := file_code("18-normal-map-docs.gdshader")
	# a1: plain
	var base := await render("", surf, 0.0, false)
	var reb := await render(dflt, surf, 0.0, false)
	out("A1-file-03-vs-default-plain", diff(base, reb))
	# a2: shadows
	var sb := await render("", surf, 0.0, true)
	var sr := await render(dflt, surf, 0.0, true)
	var shadow_present := diff(base, sb)
	var d2 := diff(sb, sr)
	d2["a_shadow_really_changes_the_default_(pixels)"] = shadow_present["pixels_differing_by_more_than_1_of_255"]
	out("A2-file-03-vs-default-with-shadow", d2)
	# a3: normal map (lamps raised to height 100)
	var ct := CanvasTexture.new()
	ct.diffuse_texture = surf
	ct.normal_texture = dome_normal()
	var nb := await render("", ct, 100.0, false)
	var nr := await render(dflt, ct, 100.0, false)
	var nd := await render(docs, ct, 100.0, false)
	var flat := await render("", surf, 100.0, false)
	var d3 := {"default_vs_file_03": diff(nb, nr), "default_vs_docs_file_18": diff(nb, nd), "normal_map_really_changes_the_default": diff(flat, nb)}
	out("A3-normal-map", d3)
	# a4: the docs file on a sprite WITHOUT a normal map is black-ish (dot with the default normal), so it is only for normal-mapped sprites
	var plain_docs := await render(docs, surf, 0.0, false)
	out("A4-docs-file-without-a-normal-map", {"centre_default": LL.px(base, 120, 90), "centre_docs_file": LL.px(plain_docs, 120, 90), "reading": "without a normal map the docs version adds nothing at lamp height 0: use it only with a normal map"})

	# b) C04 steps (lamps at (860,590) (1060,590) (960,420), energy 0.4, scale 3.5; appear 0.9 / 3.4 in the final timeline, here read at generous times)
	var steps := []
	for tt in [0.4, 2.0, 5.0]:
		var sv := SubViewport.new()
		sv.size = Vector2i(1920, 1080)
		sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		root.add_child(sv)
		var s: Node2D = LS.new()
		s.manual = true
		s.setup("C04", SH, CAPS)
		sv.add_child(s)
		await frames(3)
		while s.t < tt:
			s.step(1.0 / 30.0)
			await process_frame
		await frames(2)
		RenderingServer.force_draw(false)
		var im := sv.get_texture().get_image()
		steps.append({"t": tt, "lamps_on": s.state()["lamps"].filter(func(l): return l["enabled"]).size(), "rgb_at_overlap_(960,540)": LL.px(im, 960, 540), "rgb_far_(1600,200)": LL.px(im, 1600, 200)})
		sv.queue_free()
		await frames(2)
	out("B-C04-overlap-steps", {"steps": steps})

	# c) the tween: radius set to 0 first, then tween to 880 over 3 s on the real ring shader; read the lit radius in a 1920x1080 SubViewport at 1, 2 and 3 s
	await clear()
	var sv2 := SubViewport.new()
	sv2.size = Vector2i(1920, 1080)
	sv2.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(sv2)
	sv2.add_child(LL.canvas_mod(Color(0.0, 0.0, 0.0)))
	var floor_spr := LL.sprite(LL.solid_tex(Color.WHITE, 64), Vector2(960, 540), Vector2(30, 17), LL.shader_mat(file_code("15-ring-light.gdshader")))
	sv2.add_child(floor_spr)
	sv2.add_child(LL.point_light(Vector2(960, 540), LL.radial_tex(256), 7.0, 1.0, Color.WHITE))
	await frames(3)
	var mat := floor_spr.material as ShaderMaterial
	var before_set = mat.get_shader_parameter("radius")
	mat.set_shader_parameter("radius", 0.0)
	var tween := create_tween()
	tween.tween_property(mat, "shader_parameter/radius", 880.0, 3.0)
	var reads := []
	var t0 := Time.get_ticks_msec()
	for k in range(3):
		await create_timer(1.0).timeout
		await frames(2)
		RenderingServer.force_draw(false)
		var im2 := sv2.get_texture().get_image()
		var rad = mat.get_shader_parameter("radius")
		var first := -1
		var last := -1
		for d in range(0, 900):
			if im2.get_pixel(960 + d, 540).r > 0.02:
				if first < 0: first = d
				last = d
		reads.append({"wall_s": snappedf((Time.get_ticks_msec() - t0) / 1000.0, 0.01), "radius_uniform": snappedf(float(rad), 0.1), "lit_from_px": first, "lit_to_px": last})
	out("C-tween-ring", {"get_shader_parameter_before_any_set": str(before_set), "reads": reads, "reading": "the ring's outer edge (lit_to_px) follows the radius uniform; the thickness is 60 px"})
	# the failure: tween a uniform that was never set from code
	await clear()
	var m2 := LL.shader_mat(file_code("15-ring-light.gdshader"))
	var tw2 := create_tween()
	print("(expected error line follows: tween on a uniform never set from code)")
	tw2.tween_property(m2, "shader_parameter/radius", 880.0, 1.0)
	await frames(3)
	out("C2-tween-never-set", {"note": "see the ERROR line above in the log: the tweened property does not exist until the uniform is set once from code"})
	quit(0)

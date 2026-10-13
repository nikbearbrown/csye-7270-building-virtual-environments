extends SceneTree
# Experiment D (Reflections layout): the polish act. Same pond as exp_c_pond.gd (geometry in pond_common.gd).
#
#   D1  the final shader (03-reflection-final): effective alpha over water and over the coast ring; what the tint does.
#   D2  equals against distance on a mask whose water is painted at HALF strength (128 / 255):
#         04-compare-equal  (mask == vec3(0.5, 0.0, 0.0))        and   05-compare-distance  (distance(...) < 0.1)
#       plus the same equals line on the pure-red mask (it works there).
#   D3  what the screen texture actually holds for painted values (probe shader, one pixel).
#   D4  the same comparisons with Viewport.use_hdr_2d = true (2D drawn in linear light in a 16-bit float buffer).
#
# Run: godot --path <scratch project> [--rendering-method gl_compatibility] --script res://exp_d_polish.gd
# Output: one RESULT line per case.

const P = preload("res://pond_common.gd")
const SHADERS := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-reflections/lab-shaders/"
const TEAL := Color("#5FA391")

var tex := {}
var cur := {}
var probe_rect: ColorRect

func _initialize() -> void:
	call_deferred("run")

func frames(n: int) -> void:
	for i in range(n):
		await process_frame

func grab() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func out(id: String, d: Dictionary) -> void:
	d["case"] = id
	d["renderer"] = RenderingServer.get_current_rendering_method()
	d["hdr_2d"] = root.use_hdr_2d
	print("RESULT " + JSON.stringify(d))

func rgb(c: Color) -> Array:
	return [snappedf(c.r, 0.0001), snappedf(c.g, 0.0001), snappedf(c.b, 0.0001)]

func mat_from_code(code: String) -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = code
	var m := ShaderMaterial.new()
	m.shader = sh
	return m

func new_pond(shader_file: String, x: float, mask_key: String, code_override: String = "") -> void:
	if cur.has("scene"):
		cur["scene"].queue_free()
		await process_frame
	cur = P.build_pond(root, SHADERS, shader_file, x, {"mask_tex": tex[mask_key], "ground_tex": tex["ground"], "char_tex": tex["char"]})
	if code_override != "":
		cur["reflection"].material = mat_from_code(code_override)

func visible_pixels(x: float) -> Dictionary:
	await frames(3)
	var a := grab()
	cur["reflection"].visible = false
	await frames(2)
	var b := grab()
	cur["reflection"].visible = true
	await frames(1)
	var n := 0
	var left := int(round(x)) - P.SPRITE_N / 2
	var top := int(round(P.PLAYER_Y + P.REFLECT_OFFSET)) - P.SPRITE_N / 2
	for sy in range(top, top + P.SPRITE_N):
		for sx in range(left, left + P.SPRITE_N):
			var pa := a.get_pixel(sx, sy)
			var pb := b.get_pixel(sx, sy)
			if absf(pa.r - pb.r) + absf(pa.g - pb.g) + absf(pa.b - pb.b) > 0.03:
				n += 1
	return {"with": a, "without": b, "visible": n}

func alpha_estimate(with_img: Image, without_img: Image, px: int, py: int, base: Color) -> Dictionary:
	# obs = mix(bg, refl, alpha)  ->  alpha = (obs - bg) / (refl - bg), averaged over the channels where refl differs from bg
	var obs := with_img.get_pixel(px, py)
	var bg := without_img.get_pixel(px, py)
	var num := 0.0
	var cnt := 0
	for ch in range(3):
		var d: float = base[ch] - bg[ch]
		if absf(d) > 0.1:
			var o: float = obs[ch]
			var b: float = bg[ch]
			num += (o - b) / d
			cnt += 1
	return {"pixel": [px, py], "kind": P.kind(px, py), "bg": rgb(bg), "observed": rgb(obs), "alpha_estimate": snappedf(num / maxf(cnt, 1), 0.001)}

func add_probe() -> void:
	probe_rect = ColorRect.new()
	probe_rect.size = Vector2(8, 8)
	var psh := Shader.new()
	psh.code = "shader_type canvas_item;\nuniform sampler2D screen_texture : hint_screen_texture, filter_nearest;\nuniform vec2 at = vec2(0.5, 0.5);\nvoid fragment() { COLOR = vec4(texture(screen_texture, at).rgb, 1.0); }\n"
	var pm := ShaderMaterial.new()
	pm.shader = psh
	probe_rect.material = pm
	cur["scene"].add_child(probe_rect)

func probe_screen(px: int, py: int) -> Array:
	# one pixel of the screen texture, as a shader sees it, shown in a small rect at the top-left and read back
	probe_rect.material.set_shader_parameter("at", Vector2((px + 0.5) / P.W, (py + 0.5) / P.H))
	await frames(3)
	var img := grab()
	return rgb(img.get_pixel(4, 4))

func run() -> void:
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	root.size = Vector2i(P.W, P.H)
	await frames(3)
	tex["mask"] = ImageTexture.create_from_image(P.make_mask_image())
	tex["mask_half_red"] = ImageTexture.create_from_image(P.make_mask_image(Color(128.0 / 255.0, 0.0, 0.0, 1.0), P.MASK_COAST))
	tex["ground"] = ImageTexture.create_from_image(P.make_ground_image())
	var char_img := P.make_character_image()
	tex["char"] = ImageTexture.create_from_image(char_img)
	out("env", {"engine": Engine.get_version_info()["string"], "adapter": RenderingServer.get_video_adapter_name()})


	for hdr in [false, true]:
		root.use_hdr_2d = hdr
		await frames(3)
		# ---- D1 (default 8-bit 2D only; HDR runs repeat the comparisons below). The reflection's centre is (x, 278 + 144 = 422).
		if not hdr:
			await new_pond("03-reflection-final.gdshader", 300.0, "mask")
			var r1 = await visible_pixels(300.0)
			var water_px := alpha_estimate(r1["with"], r1["without"], 300, 422, TEAL)
			cur["reflection"].material.set_shader_parameter("tint", TEAL)
			var r1b = await visible_pixels(300.0)
			out("D1a-final-shader-tint-set-to-the-sprite-colour-(tint-then-has-no-effect-if-passed-raw)", {"water": alpha_estimate(r1b["with"], r1b["without"], 300, 422, TEAL), "expected_alpha": 0.5})
			cur["reflection"].material.set_shader_parameter("tint", Color(0.2, 0.5, 1.0, 1.0))
			var r1c = await visible_pixels(300.0)
			var o: Color = r1c["with"].get_pixel(300, 422)
			var bgc: Color = r1c["without"].get_pixel(300, 422)
			out("D1b-final-shader-default-tint", {"water_px": water_px, "observed_default_tint": rgb(o), "bg": rgb(bgc),
				"predicted_if_tint_is_mixed_raw": rgb(bgc.lerp(TEAL.lerp(Color(0.2, 0.5, 1.0), 0.5), 0.5)),
				"predicted_if_tint_were_converted_to_linear": rgb(bgc.lerp(TEAL.lerp(Color(0.2, 0.5, 1.0).srgb_to_linear(), 0.5), 0.5)),
				"visible_pixels": r1c["visible"]})
			# coast: character at x=640; find a body pixel of the reflection that lies on the coast ring
			await new_pond("03-reflection-final.gdshader", 640.0, "mask")
			cur["reflection"].material.set_shader_parameter("tint", TEAL)
			var r1d = await visible_pixels(640.0)
			var found := Vector2i(-1, -1)
			var left := 640 - P.SPRITE_N / 2
			var top := int(P.PLAYER_Y + P.REFLECT_OFFSET) - P.SPRITE_N / 2
			for j in range(P.SPRITE_N):
				for i in range(P.SPRITE_N):
					if char_img.get_pixel(i, j).a > 0.5 and char_img.get_pixel(i, j).is_equal_approx(TEAL):
						var sx := left + i
						var sy := top + (P.SPRITE_N - 1 - j)
						if P.kind(sx, sy) == P.KIND_COAST:
							found = Vector2i(sx, sy)
			out("D1c-coast-ring-alpha", {"coast": alpha_estimate(r1d["with"], r1d["without"], found.x, found.y, TEAL), "expected_alpha": 0.3})

		# ---- D2 equals vs distance on the half-strength water mask; equals on pure red
		var eq_code := FileAccess.get_file_as_string(SHADERS + "04-compare-equal.gdshader")
		await new_pond("04-compare-equal.gdshader", 300.0, "mask_half_red")
		var d2a = await visible_pixels(300.0)
		out("D2a-equals-on-HALF-red-water", {"visible_reflection_pixels": d2a["visible"], "reference_pixels_if_it_worked": 16237})
		await new_pond("05-compare-distance.gdshader", 300.0, "mask_half_red")
		var d2b = await visible_pixels(300.0)
		out("D2b-distance-on-HALF-red-water", {"visible_reflection_pixels": d2b["visible"], "reference_pixels_if_it_worked": 16237})
		await new_pond("04-compare-equal.gdshader", 300.0, "mask", eq_code.replace("vec3(0.5, 0.0, 0.0)", "vec3(1.0, 0.0, 0.0)"))
		var d2c = await visible_pixels(300.0)
		out("D2c-equals-on-PURE-red-water", {"visible_reflection_pixels": d2c["visible"], "reference_pixels_if_it_worked": 16237})
		await new_pond("04-compare-equal.gdshader", 300.0, "mask_half_red", eq_code.replace("vec3(0.5, 0.0, 0.0)", "vec3(128.0 / 255.0, 0.0, 0.0)"))
		var d2d = await visible_pixels(300.0)
		out("D2d-equals-against-128-over-255-on-half-red-water", {"visible_reflection_pixels": d2d["visible"], "reference_pixels_if_it_worked": 16237})
		await new_pond("05-compare-distance.gdshader", 300.0, "mask")
		var d2e = await visible_pixels(300.0)
		out("D2e-distance-around-HALF-red-on-PURE-red-water", {"visible_reflection_pixels": d2e["visible"], "note": "constant 0.5, tolerance 0.1, mask pure red: distance 0.5, so no match (expected 0)"})
		await new_pond("02-reflection.gdshader", 300.0, "mask")
		var d2f = await visible_pixels(300.0)
		out("D2f-the-film-shader-(distance-from-pure-red)-on-pure-red-water", {"visible_reflection_pixels": d2f["visible"], "reference_pixels_if_it_worked": 16237})

		# ---- D3 what the screen texture holds
		await new_pond("02-reflection.gdshader", 300.0, "mask")
		add_probe()
		var coast_px := Vector2i(-1, -1)
		for y in range(360, 600):
			for x in range(600, 700):
				if P.kind(x, y) == P.KIND_COAST and coast_px.x < 0:
					coast_px = Vector2i(x, y)
		out("D3a-screen-texture-value-pure-red-water-mask", {"read_back": await probe_screen(100, 600)})
		out("D3b-screen-texture-value-pure-green-coast-mask", {"read_back": await probe_screen(coast_px.x, coast_px.y), "at": [coast_px.x, coast_px.y]})
		await new_pond("02-reflection.gdshader", 300.0, "mask_half_red")
		add_probe()
		out("D3c-screen-texture-value-half-red-water-mask-(128-painted)", {"read_back": await probe_screen(100, 600), "painted_as": 128.0 / 255.0})
	root.use_hdr_2d = false
	quit(0)

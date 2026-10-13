extends SceneTree
# verify5: direction as a mask, the bow-tie, the lighthouse, two lights, and a directional light.
# A big sprite is the floor; its light() writes a mask (1 = lit white, 0 = nothing). Ambient is black so the mask reads cleanly. One point light with an opaque white texture.
# Run: godot --path <project dir> --script res://verify5.gd
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
func floor_sprite(code: String) -> Sprite2D:
	return LL.sprite(LL.solid_tex(Color.WHITE, 64), Vector2(160, 90), Vector2(6, 6), LL.shader_mat(code))
func lit(im: Image, x: int, y: int) -> int:
	return 1 if im.get_pixel(x, y).r > 0.5 else 0
func mask_code(expr: String, extra: String = "") -> String:
	return "shader_type canvas_item;\n" + extra + "void light() {\n\tfloat mask = " + expr + ";\n\tLIGHT = vec4(vec3(mask), 1.0);\n}\n"

func run() -> void:
	root.size = Vector2i(320, 180)
	var white := LL.solid_tex(Color.WHITE, 128)
	var L := Vector2(160, 90)

	# ---- M1/M2: the half and the bow-tie ----
	for case in [["M1-half-step0-dir.x", "step(0.0, LIGHT_DIRECTION.x)"], ["M2-bowtie-step0.9-abs-dir.x", "step(0.9, abs(LIGHT_DIRECTION.x))"]]:
		await clear()
		root.add_child(LL.canvas_mod(Color.BLACK))
		root.add_child(floor_sprite(mask_code(case[1])))
		root.add_child(LL.point_light(L, white, 4.0, 1.0))
		await frames(4)
		var im := grab()
		var probes := {"left (100,90)": Vector2i(100, 90), "right (220,90)": Vector2i(220, 90), "above (160,30)": Vector2i(160, 30), "below (160,150)": Vector2i(160, 150),
			"left-up (100,70)": Vector2i(100, 70), "right-down (220,100)": Vector2i(220, 100), "left-up-steep (120,50)": Vector2i(120, 50)}
		var res := {}
		for k in probes: res[k] = lit(im, probes[k].x, probes[k].y)
		out(case[0], {"lit_1_or_0_at": res})

	# ---- Directional light: the arrow is the same everywhere, so the half mask lights everything or nothing ----
	for rot in [0.0, 90.0, -90.0]:
		await clear()
		root.add_child(LL.canvas_mod(Color.BLACK))
		root.add_child(floor_sprite(mask_code("step(0.0, LIGHT_DIRECTION.x)")))
		root.add_child(LL.dir_light(rot, 1.0))
		await frames(4)
		var im2 := grab()
		out("D-directional-half-mask-rot-%d" % int(rot), {"lit_at_left_right_top_bottom": [lit(im2, 100, 90), lit(im2, 220, 90), lit(im2, 160, 30), lit(im2, 160, 150)]})

	# ---- Lighthouse with a uniform angle: aim = (cos a, sin a), keep pixels whose direction FROM the light agrees with aim ----
	var lh := mask_code("step(0.95, dot(-LIGHT_DIRECTION.xy, aim))", "uniform float a = 0.0;\n").replace("void light() {\n", "void light() {\n\tvec2 aim = vec2(cos(a), sin(a));\n")
	for ang in [0.0, 90.0, 180.0, 270.0, 45.0]:
		await clear()
		root.add_child(LL.canvas_mod(Color.BLACK))
		var fs := floor_sprite(lh)
		(fs.material as ShaderMaterial).set_shader_parameter("a", deg_to_rad(ang))
		root.add_child(fs)
		root.add_child(LL.point_light(L, white, 4.0, 1.0))
		await frames(4)
		var im3 := grab()
		# scan a ring of radius 60 px around the light: which angles are lit?
		var lit_angles := []
		for i in range(0, 360, 5):
			var p := L + 60.0 * Vector2(cos(deg_to_rad(i)), sin(deg_to_rad(i)))
			if im3.get_pixel(int(p.x), int(p.y)).r > 0.5: lit_angles.append(i)
		out("L-lighthouse-angle-%d" % int(ang), {"aim_deg_clockwise_from_right": ang, "lit_on_ring_r60_at_degrees": lit_angles,
			"reading": "beam half-angle acos(0.95) = %.1f deg" % rad_to_deg(acos(0.95))})

	# ---- Lighthouse driven by TIME: read TIME in the same frame from a second sprite (red = fract(TIME/8)) ----
	await clear()
	root.add_child(LL.canvas_mod(Color.BLACK))
	var tcode := "shader_type canvas_item;\nvoid light() {\n\tvec2 aim = vec2(cos(TIME), sin(TIME));\n\tfloat mask = step(0.95, dot(-LIGHT_DIRECTION.xy, aim));\n\tLIGHT = vec4(vec3(mask), 1.0);\n}\n"
	var tfloor := floor_sprite(tcode)
	root.add_child(tfloor)
	var clock := LL.sprite(LL.solid_tex(Color.WHITE, 16), Vector2(8, 8), Vector2(1, 1), LL.shader_mat("shader_type canvas_item;\nrender_mode unshaded;\nvoid fragment() { COLOR = vec4(fract(TIME / 8.0), 0.0, 0.0, 1.0); }\n"))
	clock.z_index = 10
	root.add_child(clock)
	root.add_child(LL.point_light(L, white, 4.0, 1.0))
	await create_timer(0.7).timeout
	for rep in range(3):
		await frames(7 + rep * 11)
		var im4 := grab()
		var tval := im4.get_pixel(8, 8).r * 8.0
		var lit2 := []
		for i in range(0, 360, 5):
			var p := L + 60.0 * Vector2(cos(deg_to_rad(i)), sin(deg_to_rad(i)))
			if im4.get_pixel(int(p.x), int(p.y)).r > 0.5: lit2.append(i)
		out("T-lighthouse-TIME-sample-%d" % rep, {"TIME_mod_8_decoded_s": snappedf(tval, 0.01), "expected_beam_centre_deg": snappedf(fposmod(rad_to_deg(tval), 360.0), 0.1), "lit_on_ring_r60_at_degrees": lit2})

	# ---- two lights, one function: each gets its own arrows, so each lamp has its own beam (aim to the right, a = 0) ----
	await clear()
	root.add_child(LL.canvas_mod(Color.BLACK))
	var fs2 := floor_sprite(lh)
	(fs2.material as ShaderMaterial).set_shader_parameter("a", 0.0)
	root.add_child(fs2)
	var small := LL.solid_tex(Color.WHITE, 128)
	root.add_child(LL.point_light(Vector2(90, 60), small, 1.6, 1.0))
	root.add_child(LL.point_light(Vector2(90, 130), small, 1.6, 1.0))
	await frames(4)
	var im5 := grab()
	out("TL-two-lamps-same-function", {"right_of_lamp1_(150,60)": lit(im5, 150, 60), "right_of_lamp2_(150,130)": lit(im5, 150, 130), "between_lamps_(150,95)": lit(im5, 150, 95), "left_of_lamp1_(40,60)": lit(im5, 40, 60), "far_right_(250,60)_outside_lights": lit(im5, 250, 60),
		"reading": "each lamp lights its own wedge to the right; outside both light squares light() never runs"})
	quit(0)

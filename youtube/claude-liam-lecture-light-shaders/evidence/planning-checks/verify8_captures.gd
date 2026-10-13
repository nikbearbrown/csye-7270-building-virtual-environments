extends SceneTree
# verify8: probes on the film's own capture scenes (light_scene.gd + captures.json), rendered at 1920x1080, scale 1, in the renderer given on the command line.
# Method: the same scene is rendered with the capture's shader, with an EMPTY light() (the ambient only, "E") and with Godot's default lighting ("B").
# (shader - E) is exactly what the shader adds; (shader - E) / (B - E) is the share of the lamp that survives.
# Probe times come from the capture's own events in captures.json (shader switches, lamp appearances, sweeps), so the checks follow the narration-derived timeline.
# Run: godot --path <project dir> [--rendering-method gl_compatibility] --script res://verify8_captures.gd -- <lab-shaders dir> <captures.json>
const LS := preload("res://light_scene.gd")
var SH := ""
var CAPS := ""
var ALL: Dictionary = {}

func _initialize() -> void: call_deferred("run")
func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))
func frames(n: int) -> void:
	for i in range(n): await process_frame

func shot(id: String, at: float, mutate: Callable = Callable()) -> Image:
	var sv := SubViewport.new()
	sv.size = Vector2i(1920, 1080)
	sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(sv)
	var s: Node2D = LS.new()
	s.manual = true
	s.setup(id, SH, CAPS)
	if mutate.is_valid():
		mutate.call(s.cfg)
	sv.add_child(s)
	await frames(3)
	while s.t < at - 0.0001:
		s.step(1.0 / 30.0)
		await process_frame
	await frames(2)
	RenderingServer.force_draw(false)
	var im := sv.get_texture().get_image()
	im.convert(Image.FORMAT_RGBA8)
	sv.queue_free()
	await frames(2)
	return im

func px(im: Image, x: int, y: int) -> Array:
	var c := im.get_pixel(x, y)
	return [snappedf(c.r, 0.001), snappedf(c.g, 0.001), snappedf(c.b, 0.001)]

func sub(a: Image, b: Image, x: int, y: int) -> Array:
	var ca := a.get_pixel(x, y)
	var cb := b.get_pixel(x, y)
	return [snappedf(ca.r - cb.r, 0.001), snappedf(ca.g - cb.g, 0.001), snappedf(ca.b - cb.b, 0.001)]

# timeline helpers (seconds)
func sw_at(id: String, i: int) -> float:
	return float(ALL[id]["shader"][i]["at"])
func lamp_appear(id: String, i: int) -> float:
	return float(ALL[id]["lamps"][i].get("appear", 0.0))

# mutators
func as_empty(cfg: Dictionary) -> void:
	cfg["shader"] = [{"node": "floor", "file": "01-light-empty.gdshader", "at": 0}]
	cfg.erase("uniform_sweeps")
func as_default(cfg: Dictionary) -> void:
	cfg.erase("shader")
	cfg.erase("uniform_sweeps")
func with_shader(file: String, uniforms: Dictionary = {}) -> Callable:
	return func(cfg: Dictionary) -> void:
		cfg["shader"] = [{"node": "floor", "file": file, "at": 0, "uniforms": uniforms}]
		cfg.erase("uniform_sweeps")
		cfg.erase("props")

func ring_extent(a: Image, e: Image, c: Vector2, r: float, thr: float = 0.05) -> Dictionary:
	# which angles (clockwise from +x, degrees, 1 degree steps) are lit on a circle of radius r around c?
	var lit: Array = []
	for i in range(0, 360):
		var p := c + r * Vector2(cos(deg_to_rad(i)), sin(deg_to_rad(i)))
		if int(p.x) < 0 or int(p.x) >= 1920 or int(p.y) < 0 or int(p.y) >= 1080:
			continue
		var d := a.get_pixel(int(p.x), int(p.y)).r - e.get_pixel(int(p.x), int(p.y)).r
		if d > thr: lit.append(i)
	if lit.is_empty():
		return {"lit_degrees": 0}
	var biggest: int = 0
	var after_gap: int = lit[0]
	for k in range(lit.size()):
		var nxt: int = lit[(k + 1) % lit.size()] + (360 if k == lit.size() - 1 else 0)
		var gap: int = nxt - lit[k]
		if gap > biggest:
			biggest = gap
			after_gap = lit[(k + 1) % lit.size()]
	var span: int = 360 - biggest + 1
	var centre := fposmod(after_gap + (span - 1) / 2.0, 360.0)
	return {"lit_degrees": lit.size(), "span_deg": span, "centre_deg": snappedf(centre, 0.1)}

func run() -> void:
	var a := OS.get_cmdline_user_args()
	SH = a[0]
	CAPS = a[1]
	ALL = JSON.parse_string(FileAccess.get_file_as_string(CAPS))
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name()})
	var C := Vector2(960, 540)

	# ---- C02: the dim scene ----
	var a2: Dictionary = ALL["C02"]["ambient_to"]
	var c2a := await shot("C02", float(a2["t0"]) - 0.4)
	var c2b := await shot("C02", float(a2["t1"]) + 0.8)
	out("C02-ambient", {"t_before_after": [float(a2["t0"]) - 0.4, float(a2["t1"]) + 0.8], "floor_far_(1500,300)_before_after": [px(c2a, 1500, 300), px(c2b, 1500, 300)], "floor_near_lamp_(700,480)_before_after": [px(c2a, 700, 480), px(c2b, 700, 480)],
		"floor_edge_of_reach_(1100,520)_before_after": [px(c2a, 1100, 520), px(c2b, 1100, 520)], "reading": "before: no tint, tiles are fully lit; after: dusk tint, the lamp stands out"})

	# ---- C05: an empty light() on the floor; the blob keeps default lighting ----
	var s5 := sw_at("C05", 0)
	var c5a := await shot("C05", s5 - 0.4)
	var c5b := await shot("C05", s5 + 1.0)
	out("C05-empty-light", {"t_before_after": [s5 - 0.4, s5 + 1.0], "floor_(1100,540)_before_after": [px(c5a, 1100, 540), px(c5b, 1100, 540)], "floor_(800,540)_before_after": [px(c5a, 800, 540), px(c5b, 800, 540)],
		"blob_centre_(1250,700)_before_after": [px(c5a, 1250, 700), px(c5b, 1250, 700)], "reading": "floor goes back to tile x dusk (0.4 to 0.435 red); blob keeps its lit colour"})

	# ---- C06: the flat answer: card colour after 0,1,2,3 lamps ----
	var reds := []
	var times6 := [lamp_appear("C06", 0) - 0.2, lamp_appear("C06", 0) + 0.4, lamp_appear("C06", 1) + 0.4, lamp_appear("C06", 2) + 0.4]
	for tt in times6:
		var im := await shot("C06", tt)
		reds.append(px(im, 700, 700))
	out("C06-flat-light", {"times": times6, "card_rgb_at_(700,700)_after_0_1_2_3_lamps": reds, "reading": "card 0.7 grey x dusk (0.5,0.55,0.72) = (0.35,0.385,0.504); each lamp adds 0.2 to every channel"})

	# ---- C07: right half wears the rebuilt default, left half is default; compare with an all-default render ----
	var c7 := await shot("C07", 2.0)
	var c7d := await shot("C07", 2.0, as_default)
	var maxd := 0.0
	var cnt := 0
	for y in range(0, 1080, 1):
		for x in range(960, 1920, 1):
			var ca := c7.get_pixel(x, y)
			var cb := c7d.get_pixel(x, y)
			var dd := maxf(maxf(absf(ca.r - cb.r), absf(ca.g - cb.g)), absf(ca.b - cb.b))
			maxd = maxf(maxd, dd)
			if dd > 0.004: cnt += 1
	out("C07-rebuilt-default-1920x1080", {"max_abs_diff_right_half": snappedf(maxd, 0.001), "pixels_differing_by_more_than_1_of_255": cnt, "pixels_compared": 960 * 1080, "seam_(959,300)_(960,300)": [px(c7, 959, 300), px(c7, 960, 300)]})

	# ---- the lamp's own alpha painted (evidence shader alpha-paint.gdshader) minus empty = the falloff ----
	var ap := func(cfg: Dictionary) -> void:
		cfg["shader"] = [{"node": "floor", "file": SH.get_base_dir().path_join("evidence/planning-checks/alpha-paint.gdshader"), "at": 0}]
		cfg.erase("props")
		cfg.erase("uniform_sweeps")
	var c8p := await shot("C08", 0.5, ap)
	var c8e := await shot("C08", 0.5, as_empty)
	var rows := []
	for d in [150, 200, 250, 300, 350, 400]:
		rows.append(sub(c8p, c8e, 960 + d, 540)[0])
	out("ALPHA-paint-minus-empty", {"distance_px": [150, 200, 250, 300, 350, 400], "added_red": rows, "expected_1_minus_d_over_409.6": [0.634, 0.512, 0.39, 0.268, 0.146, 0.024],
		"reading": "scale 3.2 -> texture 819 px, radius 409.6; values near 1 are clipped at white by the ambient floor"})

	# ---- C08: the hard square (alpha forced to one) ----
	var c8h := await shot("C08", sw_at("C08", 0) + 1.0)
	out("C08-hard-square", {"added_red_at_390_inside_and_430_outside_the_quad": [sub(c8h, c8e, 960 + 390, 540)[0], sub(c8h, c8e, 960 + 430, 540)[0]], "quad_half_width_px": 409.6})

	# ---- C09: bands on the tile floor ----
	var tb := sw_at("C09", 0) + 1.0
	var c9 := await shot("C09", tb)
	var c9d := await shot("C09", tb, as_default)
	var c9e := await shot("C09", tb, as_empty)
	var braw := []
	var draw := []
	for d in [100, 200, 300, 400, 500, 600]:
		braw.append(sub(c9, c9e, 960 + d, 540)[0])
		draw.append(sub(c9d, c9e, 960 + d, 540)[0])
	out("C09-bands", {"distance_px": [100, 200, 300, 400, 500, 600], "smooth_added_red": draw, "banded_added_red": braw, "reading": "tile floor: values depend on the tile colour and clip near the lamp; the grey-surface numbers are in verify7 C"})

	# ---- C10: pulse: red at 330 px from the lamp over 2 seconds after it starts ----
	var pr := []
	var sv := SubViewport.new()
	sv.size = Vector2i(1920, 1080)
	sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(sv)
	var s10: Node2D = LS.new()
	s10.manual = true
	s10.setup("C10", SH, CAPS)
	sv.add_child(s10)
	await frames(3)
	while s10.t < sw_at("C10", 0) + 0.1:
		s10.step(1.0 / 30.0)
		await process_frame
	for i in range(60):
		s10.step(1.0 / 30.0)
		await process_frame
		RenderingServer.force_draw(false)
		pr.append(sv.get_texture().get_image().get_pixel(960 + 330, 540).r)
		await process_frame
	sv.queue_free()
	await frames(2)
	out("C10-pulse", {"red_at_330px_min": snappedf(pr.min(), 0.001), "red_at_330px_max": snappedf(pr.max(), 0.001), "samples": pr.size(), "reading": "the lamp's brightness at one point swings up and down on its own after the shader switches on"})

	# ---- C11: unshaded bulb ----
	var s11 := sw_at("C11", 0)
	var c11a := await shot("C11", s11 - 0.4)
	var c11b := await shot("C11", s11 + 1.0)
	out("C11-unshaded", {"bulb1_default_before_after": [px(c11a, 700, 540), px(c11b, 700, 540)], "bulb2_before_after_unshaded": [px(c11a, 1220, 540), px(c11b, 1220, 540)], "bulb_own_colour": [1.0, 0.93, 0.62]})

	# ---- C12/C13/C14: direction masks, as the share of the lamp that survives at 300 px from the lamp ----
	var offs := {"left": Vector2(-300, 0), "right": Vector2(300, 0), "above": Vector2(0, -300), "below": Vector2(0, 300), "left_up_steep": Vector2(-120, -260)}
	for pair in [["C12", "across: left 1, right 0, above and below 0.5, steep 0.7"], ["C13", "step(0,x): left 1, right 0, above 0, below 0, steep 1"], ["C14", "bow-tie: left 1, right 1, above 0, below 0, steep 0"]]:
		var id: String = pair[0]
		var last := float(ALL[id]["shader"][ALL[id]["shader"].size() - 1]["at"])
		var A := await shot(id, last + 0.8)
		var B := await shot(id, last + 0.8, as_default)
		var E := await shot(id, last + 0.8, as_empty)
		var res := {}
		for dir in offs:
			var p: Vector2 = C + offs[dir]
			var num := A.get_pixel(int(p.x), int(p.y)).r - E.get_pixel(int(p.x), int(p.y)).r
			var den := B.get_pixel(int(p.x), int(p.y)).r - E.get_pixel(int(p.x), int(p.y)).r
			res[dir] = snappedf(num / den, 0.01) if absf(den) > 0.01 else null
		out(id + "-share-of-lamp-at-300px", {"t": last + 0.8, "share_by_direction": res, "reading": pair[1]})

	# ---- C15: the lighthouse beam width on a ring of radius 300 (hard edge, cutoff 0.95 -> half angle 18.2 deg) ----
	var A15 := await shot("C15", 3.0)
	var E15 := await shot("C15", 3.0, as_empty)
	var ext15 := ring_extent(A15, E15, C, 300.0)
	ext15["expected_span_deg"] = snappedf(2.0 * rad_to_deg(acos(0.95)), 0.1)
	out("C15-lighthouse-width", ext15)

	# ---- C16: cutoff 0.99, 0.95, 0.9, 0.8, 0.7 -> widths ----
	var widths := {}
	for cut in [0.99, 0.95, 0.9, 0.8, 0.7]:
		var A16 := await shot("C16", 2.0, with_shader("12-lighthouse-width.gdshader", {"cutoff": cut}))
		var E16 := await shot("C16", 2.0, with_shader("01-light-empty.gdshader"))
		var ex := ring_extent(A16, E16, C, 300.0)
		widths[str(cut)] = {"span_deg": ex.get("span_deg"), "expected_deg": snappedf(2.0 * rad_to_deg(acos(cut)), 0.1)}
	out("C16-cutoff-widths", widths)

	# ---- C18: two lamps, two beam colours (warm left, cool right) ----
	var t18 := lamp_appear("C18", 1) + 1.5
	var A18 := await shot("C18", t18)
	var E18 := await shot("C18", t18, as_empty)
	var beam_cols := {}
	for k in [["left_lamp", Vector2(560, 540)], ["right_lamp", Vector2(1360, 540)]]:
		var best := Vector3.ZERO
		var found := false
		for i in range(0, 360, 2):
			var p: Vector2 = k[1] + 150.0 * Vector2(cos(deg_to_rad(i)), sin(deg_to_rad(i)))
			var cA := A18.get_pixel(int(p.x), int(p.y))
			var cE := E18.get_pixel(int(p.x), int(p.y))
			var add := Vector3(cA.r - cE.r, cA.g - cE.g, cA.b - cE.b)
			if add.length() > best.length():
				best = add
				found = true
		beam_cols[k[0]] = [snappedf(best.x, 0.001), snappedf(best.y, 0.001), snappedf(best.z, 0.001)] if found else null
	out("C18-two-lamps-beam-colours", {"t": t18, "strongest_added_rgb_on_ring_r150": beam_cols, "reading": "warm lamp: red > blue; cool lamp: blue > red"})

	# ---- C19: reach: with alpha forced to 1 the lamp's whole texture square is lit; light() never runs outside it (scale 2.5 -> half width 320 px) ----
	var A19 := await shot("C19", 0.5, with_shader("04-light-hard-edge.gdshader"))
	var E19 := await shot("C19", 0.5, with_shader("01-light-empty.gdshader"))
	var edge := {}
	for d in [200, 300, 315, 325, 340]:
		edge[str(d)] = snappedf(sub(A19, E19, 960 + d, 540)[0], 0.001)
	out("C19-reach-square", {"added_red_at_px_right_of_lamp": edge, "quad_half_width_px": 320.0})

	# ---- C20: distance painted as d/1000: added value at 1, 250, 500 px ----
	var A20 := await shot("C20", 2.0)
	var E20 := await shot("C20", 2.0, as_empty)
	out("C20-distance", {"added_red_at_1_250_500_px": [sub(A20, E20, 960 + 1, 540)[0], sub(A20, E20, 960 + 250, 540)[0], sub(A20, E20, 960 + 500, 540)[0]], "expected_d_over_1000": [0.001, 0.25, 0.5]})

	# ---- C21 / C22 / C23: the ring ----
	var ds := [370, 380, 395, 440, 445, 455, 470]
	var A21 := await shot("C21", 0.5)
	var E21 := await shot("C21", 0.5, as_empty)
	var r21 := {}
	for d in ds: r21[str(d)] = 1 if sub(A21, E21, 960 + d, 540)[0] > 0.03 else 0
	out("C21-ring-450-60", {"lit_at_px_from_lamp": r21, "expected": "lit where 390 <= d < 450"})
	var sw: Dictionary = ALL["C22"]["uniform_sweeps"][0]
	var t22 := (float(sw["t0"]) + float(sw["t1"])) / 2.0
	var A22 := await shot("C22", t22)
	var E22 := await shot("C22", t22, as_empty)
	var r22 := {}
	for d in [370, 385, 400, 435, 445, 460]: r22[str(d)] = 1 if sub(A22, E22, 960 + d, 540)[0] > 0.03 else 0
	out("C22-ring-expanding-halfway", {"t": t22, "radius_expected_880_over_2": 440.0, "lit_at_px_from_lamp": r22, "expected": "radius 440, thickness 60: lit where 380 <= d < 440"})
	var zz: Dictionary = ALL["C23"]["zoom"]
	var A23a := await shot("C23", 1.0)
	var E23a := await shot("C23", 1.0, as_empty)
	var A23b := await shot("C23", float(zz["t1"]) + 0.5)
	var E23b := await shot("C23", float(zz["t1"]) + 0.5, as_empty)
	var z1 := {}
	var z2 := {}
	for d in [380, 395, 440, 455]:
		z1[str(d)] = 1 if sub(A23a, E23a, 960 + d, 540)[0] > 0.03 else 0
		z2[str(d)] = 1 if sub(A23b, E23b, 960 + d, 540)[0] > 0.03 else 0
	out("C23-zoom", {"zoom_1_lit_at_px": z1, "zoom_2_lit_at_px": z2, "reading": "same screen pixels at both zooms: the ring ignores the camera zoom"})

	# ---- C24: stripes stay put while the floor slides ----
	var cols0 := []
	var cols1 := []
	var t_stripes := sw_at("C24", 0) + 0.5
	var t_slid: float = float(ALL["C24"]["moves"][0]["t1"]) + 0.2
	for k in [[t_stripes, cols0], [t_slid, cols1]]:
		var A24 := await shot("C24", k[0])
		var E24 := await shot("C24", k[0], as_empty)
		for x in range(0, 1920):
			if A24.get_pixel(x, 540).r - E24.get_pixel(x, 540).r > 0.03: k[1].append(x)
	out("C24-stripes-anchored", {"t_before_slide_after_slide": [t_stripes, t_slid], "same_columns": cols0 == cols1, "first_lit_columns": cols0.slice(0, 40), "count_before": cols0.size(), "count_after": cols1.size(),
		"reading": "step(mod(x+0.5,128),16): lit where mod <= 16 inside the lamp's reach"})

	# ---- C25: grid lines ----
	var t25 := sw_at("C25", 1) + 0.5
	var A25 := await shot("C25", t25)
	var E25 := await shot("C25", t25, as_empty)
	var hlines := []
	var start := -1
	for y in range(300, 800):
		var lit := A25.get_pixel(1000, y).r - E25.get_pixel(1000, y).r > 0.03
		if lit and start < 0: start = y
		if not lit and start >= 0:
			hlines.append([start, y - 1])
			start = -1
	out("C25-grid", {"horizontal_line_runs_(y_from,to)_at_x=1000": hlines.slice(0, 8), "expected": "runs 16 px tall every 128 px, anchored at y = 0 (screen): y in [384,399], [512,527], [640,655], [768,783]"})
	quit(0)

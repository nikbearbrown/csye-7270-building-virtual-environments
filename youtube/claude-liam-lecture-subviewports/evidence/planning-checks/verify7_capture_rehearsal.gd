extends SceneTree
# SubViewports film, check 7: the capture rehearsal. Every capture scene of the film (capture_scene.gd, ids c01 .. c21) is built into a 1280 x 720 canvas,
# stepped by 1/30 s per frame, and probed at the times CAPTURE-PLAN.md lists. The numbers printed here are the "verified result to reproduce".
# A TIME probe (a 12 px rectangle in the top-left corner) is added by this script only; the capture scenes do not contain it.
# Run: godot --path <project> --fixed-fps 30 --script res://verify7_capture_rehearsal.gd [-- c05 c06 ...]   (no ids = all)

const STAGE := Common.STAGE
const CLEAR := Common.CLEAR
const TEAL := Common.TEAL
const EYE := Color("#FAF9F5")

var sc: CaptureScene
var canvas: Node2D
var tprobe: ColorRect

func _initialize() -> void: call_deferred("run")

func img() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func start(id: String) -> void:
	canvas = Node2D.new()
	root.add_child(canvas)
	sc = CaptureScene.new(id)
	sc.build(canvas)
	tprobe = ColorRect.new()
	tprobe.size = Vector2(12, 12)
	tprobe.material = Common.material_from_code(Common.TIME_PROBE_CODE)
	root.add_child(tprobe)

func finish() -> void:
	canvas.queue_free()
	tprobe.queue_free()
	sc = null
	await process_frame
	await process_frame

# step the scene to time t (frames of 1/30 s) and return the main image
func at(t: float) -> Image:
	var frames := int(round(t * 30.0))
	for f in range(frames + 1):
		sc.update(float(f) / 30.0)
		await process_frame
		RenderingServer.force_draw(false)   # exactly one real draw per logical frame, as Movie Maker does (a covered window is not drawn on every frame; RESULTS.md)
	sc.update(t)
	await process_frame
	return img()

func advance(from_t: float, to_t: float) -> Image:
	var f0 := int(round(from_t * 30.0))
	var f1 := int(round(to_t * 30.0))
	for f in range(f0 + 1, f1 + 1):
		sc.update(float(f) / 30.0)
		await process_frame
		RenderingServer.force_draw(false)
	return img()

func count_color(image: Image, target: Color, tol: float = 0.03) -> int:
	var n := 0
	for y in image.get_height():
		for x in image.get_width():
			var c := image.get_pixel(x, y)
			if c.a > 0.5 and Common.diff(c, target) < tol:
				n += 1
	return n

func implied_fade(screen: Color, picture: Color) -> float:
	var best := 0
	var gap := 0.0
	var ch := func(c: Color, i: int) -> float: return [c.r, c.g, c.b][i]
	for i in 3:
		if absf(ch.call(picture, i) - ch.call(STAGE, i)) > gap:
			gap = absf(ch.call(picture, i) - ch.call(STAGE, i))
			best = i
	return (ch.call(STAGE, best) - ch.call(screen, best)) / (ch.call(STAGE, best) - ch.call(picture, best))

func vp_of(node_name: String) -> SubViewport:
	return (sc.n[node_name] as Node).get_parent() as SubViewport

func edge_runs(image: Image, y: int, x0: int, x1: int, bg: Color) -> Array:
	var edges: Array = []
	var prev := false
	for x in range(x0, x1):
		var on := Common.diff(image.get_pixel(x, y), bg) > 0.01
		if x > x0 and on != prev:
			edges.append(x)
		prev = on
	return edges

func top_edge(image: Image, x: int, y0: int) -> int:
	for y in range(y0, image.get_height()):
		if Common.diff(image.get_pixel(x, y), STAGE) > 0.05:
			return y
	return -1

func second_diffs(ys: Array) -> Array:
	var sd: Array = []
	for i in range(1, ys.size() - 1):
		sd.append(ys[i - 1] - 2 * ys[i] + ys[i + 1])
	return sd

func run() -> void:
	root.size = Vector2i(1280, 720)
	var wanted: Array = OS.get_cmdline_user_args()
	var ids := ["c01", "c02", "c03", "c04a", "c04b", "c05", "c06", "c07", "c08", "c09", "c10", "c11", "c12", "c13", "c14", "c15", "c16", "c17", "c18", "c19", "c20", "c21"]
	Common.out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(), "fps": 30, "canvas": [1280, 720]})
	for id: String in ids:
		if wanted.size() > 0 and not (id in wanted):
			continue
		start(id)
		await process_frame
		match id:
			"c01":
				var a := await at(3.0)
				var b := await advance(3.0, 9.0)
				var diff_px := 0
				for y in range(104, 616, 4):
					for x in range(384, 896, 4):
						if Common.diff(a.get_pixel(x, y), b.get_pixel(x, y)) > 0.05:
							diff_px += 1
				var coloured := 0
				for y in range(104, 616, 4):
					for x in range(384, 896, 4):
						if Common.diff(b.get_pixel(x, y), STAGE) > 0.05:
							coloured += 1
				Common.out("c01-hook", {"pixels_that_differ_between_3_s_and_9_s_of_16384_sampled": diff_px, "non_stage_pixels_sampled_at_9_s": coloured, "reading": "the picture is alive: stripes slide, the blob turns, the mesh waves"})
			"c02":
				var a := await at(6.0)
				var cen_before := a.get_pixel(640, 360)
				var b := await advance(6.0, 8.5)
				Common.out("c02-texture-appears", {"centre_at_6_s": Common.rgb(cen_before), "centre_at_8.5_s": Common.rgb(b.get_pixel(640, 360)), "box_corner_at_8.5_s": Common.rgb(b.get_pixel(384 + 20, 104 + 20)), "stage": Common.rgb(STAGE), "teal": Common.rgb(TEAL), "clear": Common.rgb(CLEAR), "reading": "stage until the texture is handed over at 7.0 s; then the picture: teal blob in the clear-coloured box"})
			"c03":
				var a := await at(7.0)
				var row_y := 360
				var soft := func(image: Image) -> int:
					var n := 0
					for x in range(668, 668 + 512):
						var c := image.get_pixel(x, row_y)
						if Common.diff(c, CLEAR) > 0.02 and Common.diff(c, TEAL) > 0.02:
							n += 1
					return n
				var soft_lin: int = soft.call(a)
				var b := await advance(7.0, 14.0)
				var soft_near: int = soft.call(b)
				var runs: Array = []
				var cur := Color(-1, -1, -1, -1)
				var l := 0
				for x in range(668, 668 + 512):
					var c := b.get_pixel(x, row_y)
					if c.is_equal_approx(cur):
						l += 1
					else:
						if l > 0: runs.append(l)
						cur = c
						l = 1
				runs.append(l)
				Common.out("c03-size-is-resolution", {"left_picture_px": 512, "right_picture_px": 128, "right_drawn_at_scale": 4, "soft_edge_pixels_on_the_blob_row_linear_at_7_s": soft_lin, "soft_edge_pixels_nearest_at_14_s": soft_near, "run_lengths_nearest": runs.slice(0, 8), "reading": "Linear: a soft edge of several pixels; Nearest: a hard step, runs in multiples of 4"})
			"c04a":
				await at(0.5)
				var a := await advance(0.5, 5.0)
				var pic0 := vp_of("blob").get_texture().get_image()
				var whole := count_color(pic0, TEAL)
				var eyes_whole := count_color(pic0, EYE)
				var b := await advance(5.0, 10.0)
				var pic := vp_of("blob").get_texture().get_image()
				Common.out("c04a-origin", {"teal_pixels_at_5_s_before_the_slide": whole, "eye_pixels_at_5_s_before_the_slide": eyes_whole, "teal_pixels_at_10_s": count_color(pic, TEAL), "eye_pixels_at_10_s": count_color(pic, EYE), "whole_blob_teal_pixels": 55202, "fraction": snappedf(float(count_color(pic, TEAL)) / 55202.0, 0.001), "reading": "the whole blob in the middle until the slide starts at 6.4 s; at (0, 0) from 8.6 s on: a quarter of the blob, no eyes"})
			"c04b":
				var res := {}
				var a := await at(0.2)
				res["0.2 s (sprite at 0,0)"] = count_color(vp_of("blob").get_texture().get_image(), TEAL)
				var b := await advance(0.2, 3.7)
				res["3.7 s (middle, whole)"] = count_color(vp_of("blob").get_texture().get_image(), TEAL)
				var c := await advance(3.7, 9.0)
				res["9.0 s (sliding off the right edge, cut)"] = count_color(vp_of("blob").get_texture().get_image(), TEAL)
				var d := await advance(9.0, 14.0)
				res["14.0 s (end: centre at x = 560, mostly outside)"] = count_color(vp_of("blob").get_texture().get_image(), TEAL)
				Common.out("c04b-cut-off", {"teal_pixels_in_the_picture": res, "whole_blob": 55202})
			"c05":
				var a := await at(6.0)
				var b := await advance(6.0, 10.0)
				Common.out("c05-transparent", {"empty_pixel_at_6_s": Common.rgb(a.get_pixel(404, 124)), "empty_pixel_at_10_s": Common.rgb(b.get_pixel(404, 124)), "clear": Common.rgb(CLEAR), "stage": Common.rgb(STAGE), "reading": "the clear-coloured box until 8 s, then the stage (and the grid lines) shows through"})
			"c06":
				var a := await at(6.0)
				var mix_c := a.get_pixel(807, 360)
				var b := await advance(6.0, 12.0)
				Common.out("c06-premultiplied", {"ring_pixel_screen_807_360_with_Mix_at_6_s": Common.rgb(mix_c), "ring_pixel_with_Premultiplied_Alpha_at_12_s": Common.rgb(b.get_pixel(807, 360)), "reading": "Mix darkens the half-transparent ring; Premultiplied Alpha matches the right answer (0.890, 0.796, 0.576 in Forward+)"})
			"c07":
				var a := await at(5.0)
				var b := await advance(5.0, 9.0)
				Common.out("c07-inner-shader", {"centre_at_5_s": Common.rgb(a.get_pixel(640, 360)), "centre_at_9_s": Common.rgb(b.get_pixel(640, 360)), "reading": "the plain teal blob until 7 s, then the gradient (0.651, 0.698, 0.459 at the sprite's middle)"})
			"c08":
				await at(3.0)
				var b := await advance(3.0, 6.0)
				var worst := 0.0
				for y in range(150, 570, 6):
					for x in range(120, 580, 6):
						worst = maxf(worst, Common.diff(b.get_pixel(100 + (x - 100), y), b.get_pixel(668 + (x - 100), y)))
				Common.out("c08-passthrough", {"largest_channel_difference_between_the_two_displays": snappedf(worst, 0.0001), "reading": "the plain display (left) and the pass-through shader display (right) are identical while the sprite slides"})
			"c09":
				var a := await at(3.0)
				var b := await advance(3.0, 8.0)
				var pic := vp_of("blob").get_texture().get_image()
				var rows: Array = []
				for dx: int in [-60, 0, 60]:
					var px: int = 256 + dx
					var pc := pic.get_pixel(px, 296)
					rows.append({"picture_x": px, "expected_x_over_512": snappedf((px + 0.5) / 512.0, 0.001), "implied_fade": snappedf(implied_fade(b.get_pixel(384 + px, 104 + 296), pc), 0.001)})
				Common.out("c09-fade", {"fade_at_8_s": rows, "full_colour_at_3_s_centre": Common.rgb(a.get_pixel(640, 360 + 40)), "reading": "after 4.5 s the picture fades from the left edge (0) to the right edge (1) of the 512 px picture"})
			"c10":
				var a := await at(0.2)
				var pic0 := vp_of("blob").get_texture().get_image()
				var before := {"red_100px_above": snappedf(pic0.get_pixel(256, 156).r, 0.001), "red_100px_below": snappedf(pic0.get_pixel(256, 356).r, 0.001)}
				var b := await advance(0.2, 5.0)
				var pic1 := vp_of("blob").get_texture().get_image()
				var after := {"red_100px_above": snappedf(pic1.get_pixel(256, 156).r, 0.001), "red_100px_below": snappedf(pic1.get_pixel(256, 356).r, 0.001)}
				var rows: Array = []
				for dx: int in [-60, 0, 60]:
					var px: int = 256 + dx
					var pc := pic1.get_pixel(px, 296)
					if pc.a > 0.99:
						rows.append({"picture_x": px, "expected_x_over_512": snappedf((px + 0.5) / 512.0, 0.001), "implied_fade": snappedf(implied_fade(b.get_pixel(384 + px, 104 + 296), pc), 0.001)})
				Common.out("c10-turn", {"gradient_before_the_turn_at_0.2_s": before, "gradient_after_half_a_turn_at_5_s": after, "fade_after_the_turn": rows, "reading": "the gradient flips (gold moves from below to above); the fade is unchanged"})
			"c11":
				var b := await at(0.0)
				var left: Array = []
				for cx: int in [190, 490]:
					left.append({"sprite_centre_x": cx, "implied_fade": snappedf(implied_fade(b.get_pixel(cx, 360), TEAL), 0.001)})
				var right: Array = []
				for cx: int in [810, 1110]:
					right.append({"sprite_centre_x": cx, "implied_fade": snappedf(implied_fade(b.get_pixel(cx, 360), TEAL), 0.001)})
				Common.out("c11-group", {"one_fade_per_sprite": left, "one_fade_on_the_picture": right, "reading": "per sprite: 0.5 at both centres (each restarts); on the picture: about 0.25 and 0.75 (one fade across both)"})
			"c12":
				var b := await at(4.0)
				var y := 104 + 8 * 34
				var stripe_edges := edge_runs(b, y, 384 + 8 * 10, 384 + 8 * 54, STAGE)
				var res_s: Array = []
				for e: int in stripe_edges:
					res_s.append((e - 384) % 8)
				Common.out("c12-per-display-pixel", {"edge_x_positions_in_the_display_at_4_s": stripe_edges, "mod_8": res_s, "reading": "the blob's own edges fall on multiples of 8; stripe edges land on any display pixel"})
			"c13":
				var checked := 0
				for t: float in [2.0, 6.0, 10.0]:
					var image: Image
					if t == 2.0:
						image = await at(t)
					else:
						image = await advance(t - 4.0, t)
					var m := (sc.n["display"] as Sprite2D).material as ShaderMaterial
					var w: float = m.get_shader_parameter("width")
					var cnt: float = m.get_shader_parameter("count")
					var pic := vp_of("blob").get_texture().get_image()
					var mism := 0
					var n := 0
					for py in range(130, 390, 4):
						for px in range(130, 390, 4):
							if pic.get_pixel(px, py).a < 0.99:
								continue
							var d := ((px + 0.5) + (py + 0.5)) / 512.0
							var s := d * cnt - floorf(d * cnt)
							if absf(s - w) < 0.05 or s < 0.03 or s > 0.97:
								continue
							var on_got := Common.diff(image.get_pixel(384 + px, 104 + py), STAGE) > 0.03
							n += 1
							if (s < w) != on_got:
								mism += 1
					Common.out("c13-stripes-dials-at-%s-s" % str(t), {"width": snappedf(w, 0.001), "count": snappedf(cnt, 0.01), "pixels_checked": n, "mismatches": mism})
			"c14":
				var b := await at(4.0)
				var T := Common.time_of(b)
				var pic := vp_of("blob").get_texture().get_image()
				var mism := 0
				var n := 0
				for py in range(130, 390, 4):
					for px in range(130, 390, 4):
						if pic.get_pixel(px, py).a < 0.99:
							continue
						var d := ((px + 0.5) + (py + 0.5)) / 512.0 - T * 0.12
						var s := d * 6.0 - floorf(d * 6.0)
						if absf(s - 0.5) < 0.05 or s < 0.03 or s > 0.97:
							continue
						var on_got := Common.diff(b.get_pixel(384 + px, 104 + py), STAGE) > 0.03
						n += 1
						if (s < 0.5) != on_got:
							mism += 1
				Common.out("c14-moving-stripes", {"TIME_read": snappedf(T, 0.001), "pixels_checked": n, "mismatches": mism, "reading": "the formula with the TIME the shader saw predicts every probe while the sprite turns"})
			"c15":
				var b := await at(3.0)
				var names := ["red", "yellow", "green", "cyan", "blue", "magenta"]
				var sw: Dictionary = {}
				for k in 6:
					sw[names[k]] = Common.rgb(b.get_pixel(140 + k * 170 + 80, 330 + 80))
				var strip: Dictionary = {}
				for k in 6:
					strip["hue %d/6" % k] = Common.rgb(b.get_pixel(140 + int(round(k / 6.0 * 1000.0)) + (1 if k == 0 else (-1 if k == 6 else 0)), 90 + 65))
				Common.out("c15-hue-strip-and-swatches", {"six_swatches_exact_hue": sw, "strip_pixels_at_the_same_hues": strip, "reading": "swatches are exact (1,0,0) (1,1,0) (0,1,0) (0,1,1) (0,0,1) (1,0,1); the strip passes through the same colours"})
			"c16":
				var b := await at(4.0)
				var T := Common.time_of(b)
				var pic := vp_of("blob").get_texture().get_image()
				var worst := 0.0
				var n := 0
				for py in range(130, 390, 3):
					for px in range(130, 390, 3):
						if pic.get_pixel(px, py).a < 0.99:
							continue
						var d := ((px + 0.5) + (py + 0.5)) / 512.0 - T * 0.12
						var s := d * 6.0 - floorf(d * 6.0)
						if s < 0.44 and s > 0.04:
							worst = maxf(worst, Common.diff(Color.from_hsv(d - floorf(d), 1.0, 1.0), b.get_pixel(384 + px, 104 + py)))
							n += 1
				Common.out("c16-rainbow-stripes", {"TIME_read": snappedf(T, 0.001), "stripe_pixels_compared": n, "largest_channel_difference_to_hsv_of_the_diagonal": snappedf(worst, 0.0001)})
			"c17", "c18":
				var b := await at(4.0)
				var T := Common.time_of(b)
				var res := {}
				var xs := [10, 60, 110, 160, 210, 260, 310, 360, 410, 460]
				var meshes: Array = [["right", 950.0, 480.0, 31]] if id == "c17" else [["right", 640.0, 512.0, 31]]
				if id == "c17":
					meshes.push_front(["left", 330.0, 480.0, 0])
				for mm: Array in meshes:
					var ys: Array = []
					var exp: Array = []
					var half: float = mm[2] / 2.0
					for dx: int in xs:
						var px: int = int(mm[1] - half) + dx
						ys.append(top_edge(b, px, 40))
						var u: float = (dx + 0.5) / mm[2]
						exp.append(snappedf((360.0 - half) + sin(u * 10.0 + T * 3.0) * 16.0, 0.1))
					var rms := 0.0
					if mm[3] == 31:
						for i in xs.size():
							rms += pow(float(ys[i]) - float(exp[i]), 2.0)
						rms = sqrt(rms / xs.size())
					res[mm[0]] = {"subdivide": mm[3], "top_edge_y": ys, "second_differences": second_diffs(ys), "span_px": ys.max() - ys.min(), "rms_error_vs_formula_px": snappedf(rms, 0.01) if mm[3] == 31 else "n/a"}
				Common.out(id + "-wobble", {"TIME_read": snappedf(T, 0.001), "meshes": res, "reading": "plain quad: straight edge (second differences 0 or 1). grid: the edge follows 360 - half + sin(UV.x * 10 + TIME * 3) * 16"})
			"c19":
				var a := await at(6.0)
				var upper_a := 0
				var lower_a := 0
				# the eyes are the lightest small spots on the gradient blob: count near-cream pixels above and below the blob's centre (screen y = 360)
				var eyeish := func(c: Color) -> bool: return c.r > 0.93 and c.g > 0.85 and c.b > 0.55 and c.b < 0.8
				for y in range(104, 616):
					for x in range(500, 780):
						if eyeish.call(a.get_pixel(x, y)):
							if y < 360: upper_a += 1
							else: lower_a += 1
				var b := await advance(6.0, 12.0)
				var upper_b := 0
				var lower_b := 0
				for y in range(104, 616):
					for x in range(500, 780):
						if eyeish.call(b.get_pixel(x, y)):
							if y < 360: upper_b += 1
							else: lower_b += 1
				Common.out("c19-upside-down", {"eye_pixels_above_and_below_the_centre_at_6_s_with_size_y_512": [upper_a, lower_a], "at_12_s_with_size_y_minus_512": [upper_b, lower_b], "reading": "at 6 s the eyes are below the centre (upside down); at 12 s, after the height goes negative at 9.5 s, above it (upright)"})
			"c20":
				var a := await at(0.0)
				var res := {}
				var panels := {"Sprite2D": 40, "interface panel": 340, "3D plane": 640, "shader sampler": 940}
				for k: String in panels:
					var x0: int = panels[k]
					var above := a.get_pixel(x0 + 140, 360 - 60 + (0 if k != "interface panel" else 0))
					var below := a.get_pixel(x0 + 140, 360 + 60)
					res[k] = {"red_60px_above_centre": snappedf(above.r, 0.001), "red_60px_below_centre": snappedf(below.r, 0.001), "card_corner": Common.rgb(a.get_pixel(x0 + 12, 232))}
				Common.out("c20-four-places", {"at_0_s": res, "reading": "gold (high red) is below the centre in every panel: the same picture, upright, in four places (the 3D plane faces the camera at 0 s)"})
			"c21":
				var b := await at(12.0)
				var live := first_teal(vp_of("blob0").get_texture().get_image())
				var frozen := first_teal(vp_of("blob1").get_texture().get_image())
				var left_edge := 0.30 * 448.0 * 0.6
				var px_live := 256.0 + 150.0 * sin(0.9 * 12.0) - left_edge
				var px_at_once := 256.0 + 150.0 * sin(0.9 * 8.5) - left_edge
				Common.out("c21-update-mode", {"left_picture_first_teal_x_at_12_s": live, "left_by_formula": snappedf(px_live, 1.0), "right_picture_first_teal_x_at_12_s": frozen, "right_frozen_at_8.5_s_by_formula": snappedf(px_at_once, 1.0), "reading": "the default viewport follows the sprite; the one set to Once at 8.5 s keeps the picture it drew then"})
		await finish()
	quit(0)

func first_teal(image: Image) -> int:
	for x in image.get_width():
		for y in image.get_height():
			var c := image.get_pixel(x, y)
			if c.a > 0.5 and Common.diff(c, TEAL) < 0.03:
				return x
	return -1

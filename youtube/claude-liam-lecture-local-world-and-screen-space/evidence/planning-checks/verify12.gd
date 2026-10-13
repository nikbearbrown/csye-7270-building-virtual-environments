extends SceneTree
# verify12.gd: the reference capture scenes (capture_scenes.gd, contract build() / at(t)) run end to end at 1280 x 720.
# For every capture C01 to C11b: build the scene, call at(t) at 0, 50 % and 85 % of the estimated audio, grab the frame, save the 50 % and 85 %
# frames and a contact sheet, and check the facts the film relies on (the same facts as verify5, verify6 and verify7, now through the real scene scripts).
# Every scene is built into the window (1280 x 720 logical canvas; its local and world numbers do not depend on the render size, verify8.gd R1),
# EXCEPT a scene whose route() says reads_window_pixels (C10): that one is built into a SubViewport of its own render size (1920 x 1080, scale 1) and its
# frames come from the SubViewport's texture, because the series rule is that shaders reading window pixels are captured at the size they are shown.
# Run: godot --path <project dir> --script res://verify12.gd -- <out dir>

const Lib := preload("res://probe_lib.gd")
const Scn := preload("res://scenes_lib.gd")
const CS := preload("res://capture_scenes.gd")
var lib
var out_dir := "/private/tmp/claude-501/godot-shaders-local-world-and-screen-space/scratch/out/cap/"
var thumbs: Array = []
var STAGE_RGB := [217, 213, 202]


func _initialize() -> void:
	call_deferred("run")


func rgb8(c: Color) -> Array:
	return [roundi(c.r * 255.0), roundi(c.g * 255.0), roundi(c.b * 255.0)]


var vp: SubViewport = null     # set while a scene that reads window pixels is built into its own SubViewport


func frame() -> Image:
	if vp != null:
		return vp.get_texture().get_image()
	return lib.grab()


func near(a: Array, b: Array, tol: int = 12) -> bool:
	return absi(a[0] - b[0]) <= tol and absi(a[1] - b[1]) <= tol and absi(a[2] - b[2]) <= tol


func nonstage_fraction(img: Image) -> float:
	var n := 0
	var tot := 0
	for y in range(0, img.get_height(), 4):
		for x in range(0, img.get_width(), 4):
			var c := rgb8(img.get_pixel(x, y))
			if absi(c[0] - STAGE_RGB[0]) > 6 or absi(c[1] - STAGE_RGB[1]) > 6 or absi(c[2] - STAGE_RGB[2]) > 6:
				n += 1
			tot += 1
	return snappedf(float(n) / float(tot), 0.001)


func clear_scene() -> void:
	for c in root.get_children():
		c.queue_free()


func set_t(sc, t: float) -> Image:
	sc.at(t)
	await lib.frames(3)
	return frame()


func stripe_bits(img: Image, screen_x: int) -> String:
	var bits := ""
	for dx in range(-70, 71, 2):
		var c := img.get_pixel(screen_x + dx, 360)
		bits += "1" if (c.r > 0.97 and c.g > 0.97 and c.b > 0.97) else "0"
	return bits


func tcount(img: Image, cx: int, cy: int) -> int:
	var transitions := 0
	var prev := ""
	for x in range(cx - 70, cx + 71):
		var c := img.get_pixel(x, cy)
		var cls := "cream" if c.r > 0.9 else "teal"
		if prev != "" and cls != prev:
			transitions += 1
		prev = cls
	return transitions


func run() -> void:
	lib = Lib.new(self)
	RenderingServer.set_default_clear_color(Scn.STAGE)
	root.size = Vector2i(1280, 720)
	await lib.frames(3)
	DirAccess.make_dir_recursive_absolute(out_dir)
	var results := {}
	for id in ["C01", "C02", "C03", "C04", "C05", "C06", "C07", "C08", "C09", "C10", "C11a", "C11b"]:
		clear_scene()
		await lib.frames(3)
		var sc = CS.make(id)
		var T: float = CS.EST[id]
		var rt: Dictionary = sc.route()
		vp = null
		var host: Node = root
		if rt["reads_window_pixels"]:
			vp = SubViewport.new()
			vp.size = rt["render"]
			vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
			root.add_child(vp)
			host = vp
		sc.build(host, T)
		await lib.frames(3)
		var r := {"audio_length_s": T, "route_canvas": [rt["canvas"].x, rt["canvas"].y], "route_render": [rt["render"].x, rt["render"].y],
			"reads_window_pixels": rt["reads_window_pixels"]}
		var img0: Image = await set_t(sc, 0.0)
		var img50: Image = await set_t(sc, 0.50 * T)
		var img85: Image = await set_t(sc, 0.85 * T)
		img50.save_png(out_dir + "capture-%s-50pct.png" % id)
		img85.save_png(out_dir + "capture-%s-85pct.png" % id)
		thumbs.append(img50)
		thumbs.append(img85)
		r["non_stage_fraction_at_0_50_85_pct"] = [nonstage_fraction(img0), nonstage_fraction(img50), nonstage_fraction(img85)]
		match id:
			"C01":
				# right (world) sprite: colours at six fixed screen pixels identical at 20 % and 30 % of the beat; left (local): sprite-relative pixels identical, fixed-screen pixels change
				var img20: Image = await set_t(sc, 0.20 * T)
				var xr20: float = sc.right.position.x
				var xl20: float = sc.left.position.x
				var img30: Image = await set_t(sc, 0.30 * T)
				var xr30: float = sc.right.position.x
				var xl30: float = sc.left.position.x
				var offs: Array[Vector2i] = [Vector2i(0, 0), Vector2i(-15, 10), Vector2i(20, -14), Vector2i(-30, -18), Vector2i(12, 40), Vector2i(-8, -40)]
				var fixed_same := 0
				var rel_same := 0
				var left_fixed_changed := 0
				for o in offs:
					var pw: Vector2i = Vector2i(int((xr20 + xr30) * 0.5), 240) + o
					if rgb8(img20.get_pixel(pw.x, pw.y)) == rgb8(img30.get_pixel(pw.x, pw.y)):
						fixed_same += 1
					if near(rgb8(img20.get_pixel(roundi(xl20) + o.x, 240 + o.y)), rgb8(img30.get_pixel(roundi(xl30) + o.x, 240 + o.y))):
						rel_same += 1
					var pl: Vector2i = Vector2i(int((xl20 + xl30) * 0.5), 240) + o
					if rgb8(img20.get_pixel(pl.x, pl.y)) != rgb8(img30.get_pixel(pl.x, pl.y)):
						left_fixed_changed += 1
				r["world_sprite_same_colour_at_fixed_screen_pixels_of_6"] = fixed_same
				r["local_sprite_same_colour_at_sprite_relative_pixels_of_6_within_12_levels_the_slide_is_fractional_in_pixels"] = rel_same
				r["local_sprite_fixed_screen_pixels_changed_of_6"] = left_fixed_changed
				r["sprite_x_at_20_30_pct"] = [snappedf(xr20, 0.1), snappedf(xr30, 0.1)]
			"C02":
				var cs: Array = []
				for im in [img0, img85]:
					var sx := 0.0
					var sy := 0.0
					var n := 0
					for y in range(150, 330):
						for x in range(120, 360):
							var c := rgb8(im.get_pixel(x, y))
							if absi(c[0] - 217) < 30 and absi(c[1] - 119) < 30 and absi(c[2] - 87) < 30:
								sx += x
								sy += y
								n += 1
					cs.append([snappedf(sx / maxf(n, 1.0), 0.1), snappedf(sy / maxf(n, 1.0), 0.1), n])
				r["terracotta_dot_centroid_and_pixels_at_0_and_85_pct"] = cs
				r["expected_dot_centre"] = "(286,236) at the start, (186,236) after the pan (pixel centres add 0.5)"
			"C03":
				r["sprite_centre_rgb_at_0_pct_x300"] = rgb8(img0.get_pixel(300, 360))
				r["expected_at_x300"] = rgb8(Color(300.5 / 1280.0, 360.5 / 720.0, 0.8))
				r["sprite_centre_rgb_at_85_pct_x980"] = rgb8(img85.get_pixel(980, 360))
				r["expected_at_x980"] = rgb8(Color(980.5 / 1280.0, 360.5 / 720.0, 0.8))
			"C04":
				r["pixel_800_100_at_50_pct_tiled"] = rgb8(img50.get_pixel(800, 100))
				r["pixels_800_and_1000_at_85_pct_smeared"] = [rgb8(img85.get_pixel(800, 100)), rgb8(img85.get_pixel(1000, 100))]
				r["pixels_800_and_1000_at_50_pct"] = [rgb8(img50.get_pixel(800, 100)), rgb8(img50.get_pixel(1000, 100))]
			"C05":
				r["sprite_x_at_50_pct"] = snappedf(sc.sprite.position.x, 0.1)
				r["pixel_852_240_at_85_pct_planet_cream_expected"] = rgb8(img85.get_pixel(852, 240))
				r["pixel_852_240_at_0_pct_faint_planet_expected_pale"] = rgb8(img0.get_pixel(852, 240))
			"C06":
				var pts := [Vector2i(852, 240), Vector2i(862, 250), Vector2i(842, 232), Vector2i(867, 228), Vector2i(840, 255)]
				var same := 0
				for p in pts:
					if rgb8(img0.get_pixel(p.x, p.y)) == rgb8(img85.get_pixel(p.x, p.y)):
						same += 1
				r["same_colour_at_five_screen_pixels_before_and_after_turn_and_stretch"] = same
				r["rotation_deg_and_scale_at_85_pct"] = [snappedf(rad_to_deg(sc.sprite.rotation), 0.1), [snappedf(sc.sprite.scale.x, 0.01), snappedf(sc.sprite.scale.y, 0.01)]]
			"C07":
				r["colour_changes_along_140_px_at_50_pct_128px_art"] = tcount(img50, 640, 360)
				r["colour_changes_along_140_px_at_85_pct_64px_art"] = tcount(img85, 640, 360)
			"C08":
				var img66: Image = await set_t(sc, 0.66 * T)
				img66.save_png(out_dir + "capture-C08-66pct-hole-inside-the-sprite.png")
				r["sprite_x_at_66_pct"] = snappedf(sc.sprite.position.x, 0.1)
				r["pixel_640_360_inside_the_hole_is_stage"] = rgb8(img66.get_pixel(640, 360))
				r["pixel_708_360_inside_the_sprite_outside_the_hole_is_teal"] = rgb8(img66.get_pixel(708, 360))
			"C09":
				var img78: Image = await set_t(sc, 0.78 * T)
				img78.save_png(out_dir + "capture-C09-78pct-window-over-the-planet.png")
				r["sprite_x_at_78_pct"] = snappedf(sc.sprite.position.x, 0.1)
				r["centre_pixel_of_the_planet_852_240_at_78_pct"] = rgb8(img78.get_pixel(852, 240))
				r["sprite_centre_rgb_at_50_pct_amount_0"] = rgb8(img50.get_pixel(int(560), 240))
			"C10":
				var w := img85.get_width()
				var h := img85.get_height()
				var worst := 0
				var n := 0
				for gy in range(9):
					for gx in range(16):
						var x := int((gx + 0.5) * w / 16.0)
						var y := int((gy + 0.5) * h / 9.0)
						if absi(y - h / 2) < 6 or absi(x - w / 2) < 6:
							continue   # the thin grey tile outline is drawn on the seam rows and columns
						var c := rgb8(img85.get_pixel(x, y))
						var e := rgb8(Color((x + 0.5) / float(w), (y + 0.5) / float(h), 0.8))
						worst = maxi(worst, maxi(maxi(absi(c[0] - e[0]), absi(c[1] - e[1])), absi(c[2] - e[2])))
						n += 1
				r["image_size"] = [w, h]
				r["final_frame_worst_8bit_difference_from_the_exact_gradient_over_%d_pixels_off_the_seams" % n] = worst
				# pixels either side of the two seams, just outside the 3 px outline strokes: each must equal the exact gradient at its own position
				var seam_worst := 0
				var seam_pts := [Vector2i(w / 2 - 12, h / 4), Vector2i(w / 2 + 12, h / 4), Vector2i(w / 2 - 12, 3 * h / 4), Vector2i(w / 2 + 12, 3 * h / 4),
					Vector2i(w / 4, h / 2 - 12), Vector2i(w / 4, h / 2 + 12), Vector2i(3 * w / 4, h / 2 - 12), Vector2i(3 * w / 4, h / 2 + 12)]
				var seam_vals: Array = []
				for sp in seam_pts:
					var c2 := rgb8(img85.get_pixel(sp.x, sp.y))
					var e2 := rgb8(Color((sp.x + 0.5) / float(w), (sp.y + 0.5) / float(h), 0.8))
					seam_worst = maxi(seam_worst, maxi(maxi(absi(c2[0] - e2[0]), absi(c2[1] - e2[1])), absi(c2[2] - e2[2])))
					seam_vals.append([sp.x, sp.y, c2])
				r["pixels_beside_the_seams_worst_difference_from_the_exact_gradient"] = seam_worst
				r["pixels_beside_the_seams"] = seam_vals
				r["bottom_right_tile_at_50_pct_is_flat_grey"] = rgb8(img50.get_pixel(3 * w / 4, 3 * h / 4))
				r["top_left_tile_at_50_pct_is_gradient"] = rgb8(img50.get_pixel(w / 4, h / 4))
				r["tile_outline_pixel_on_the_vertical_seam_is_grey"] = rgb8(img85.get_pixel(w / 2 - 1, h / 4))
			"C11a", "C11b":
				var xs := [256, 640, 1024]
				var bits0: Array = []
				var bits85: Array = []
				for i in 3:
					bits0.append(stripe_bits(img0, xs[i]))
				var sx85: Array = []
				for i in 3:
					var sxp := int((sc.sprites[i].position.x - sc.cam.position.x) + 640.0)
					sx85.append(sxp)
					bits85.append(stripe_bits(img85, sxp))
				r["start_patterns_identical_in_all_three"] = (bits0[0] == bits0[1] and bits0[1] == bits0[2])
				r["after_move_pattern_relative_to_sprite_unchanged_local_world_screen"] = [bits85[0] == bits0[0], bits85[1] == bits0[1], bits85[2] == bits0[2]]
				r["sprite_screen_x_at_85_pct"] = sx85
		results[id] = r
		lib.out("capture-" + id, r)
		if vp != null:
			vp.queue_free()
			vp = null
	# contact sheet: 4 columns x 6 rows of 320 x 180 thumbnails (each scene: its 50 % then its 85 % frame)
	var sheet := Image.create(1280, 1080, false, Image.FORMAT_RGBA8)
	for i in thumbs.size():
		var t: Image = thumbs[i].duplicate()
		t.convert(Image.FORMAT_RGBA8)
		t.resize(320, 180, Image.INTERPOLATE_LANCZOS)
		sheet.blit_rect(t, Rect2i(0, 0, 320, 180), Vector2i((i % 4) * 320, (i / 4) * 180))
	sheet.save_png(out_dir + "capture-scenes-contact-sheet.png")
	quit(0)

extends SceneTree
# SubViewports film, check 12: does the 3x SubViewport native-size capture route change anything this film shows?
# The route (COMPONENT-SPECS.md, "Capture harness"): a 3840 x 2160 SubViewport over a 1280 x 720 logical canvas (size_2d_override + stretch). It changes the numbers of shaders
# that read window pixels (FRAGCOORD, SCREEN_PIXEL_SIZE, LIGHT_*); this film's shaders read only UV, TIME, TEXTURE and VERTEX (grep in CHECKS-REPORT.md), and its own pictures
# are SubViewports NESTED inside the route's SubViewport. So the question is tested, not assumed:
# every capture scene is built twice in the same process: once in a 1280 x 720 SubViewport (scale 1) and once in the 3x route. Both are drawn in the same pass, so TIME is the
# same. At 12 %, 50 % and 85 % of the scene's length the centre of every logical pixel is compared: pixel (x, y) of the scale-1 picture against pixel (3x + 1, 3y + 1) of the 4K picture,
# which is the same point of the canvas. Equal drawing gives equal colours.
# Run: godot --path <project> --fixed-fps 30 --script res://verify12_route_equivalence.gd [-- c05 c06 ...]   (no ids = all)

const TOL := 0.04     # 10 of 255 in the largest channel

func _initialize() -> void: call_deferred("run")

func make_route(scale3: bool) -> SubViewport:
	var v := SubViewport.new()
	if scale3:
		v.size = Vector2i(3840, 2160)
		v.size_2d_override = Vector2i(1280, 720)
		v.size_2d_override_stretch = true
	else:
		v.size = Vector2i(1280, 720)
	v.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(v)
	return v

func compare(a: Image, b: Image) -> Dictionary:
	var over := 0
	var worst := 0.0
	var wx := 0
	var wy := 0
	var non_stage := 0
	var unmatched := 0
	var worst_unmatched := 0.0
	var diag: Dictionary = {}      # x + y + 1 of every differing pixel: diagonal stripes whose edge falls exactly on a pixel centre are decided by float rounding
	for y in 720:
		for x in 1280:
			var pa := a.get_pixel(x, y)
			var pb := b.get_pixel(3 * x + 1, 3 * y + 1)
			var d := Common.diff(pa, pb)
			if Common.diff(pa, Common.STAGE) > 0.03:
				non_stage += 1
			if d > TOL:
				over += 1
				diag[x + y + 1] = int(diag.get(x + y + 1, 0)) + 1
				# tolerant test: does ANY of the nine 4K pixels of this logical pixel show the scale-1 colour? (an edge that falls exactly on a pixel centre is decided by float rounding;
				# the neighbours then show both states). A real difference has no match anywhere in the block.
				var matched := false
				for dy in range(-1, 2):
					for dx in range(-1, 2):
						if Common.diff(pa, b.get_pixel(3 * x + 1 + dx, 3 * y + 1 + dy)) <= TOL:
							matched = true
				if not matched:
					unmatched += 1
					if d > worst_unmatched:
						worst_unmatched = d
			if d > worst:
				worst = d
				wx = x
				wy = y
	var keys: Array = diag.keys()
	keys.sort_custom(func(p: int, q: int) -> bool: return int(diag[p]) > int(diag[q]))
	var top: Dictionary = {}
	for i in mini(keys.size(), 6):
		top[str(keys[i])] = diag[keys[i]]
	return {"pixels_compared": 1280 * 720, "pixels_that_are_not_stage_colour": non_stage, "pixels_differing_by_more_than_10_of_255": over, "of_those_with_no_matching_pixel_in_their_3x3_block": unmatched, "largest_difference_with_no_match": snappedf(worst_unmatched, 0.001), "largest_difference": snappedf(worst, 0.001), "largest_difference_at_logical_xy": [wx, wy], "differing_pixels_by_x_plus_y_plus_1_top6": top, "distinct_x_plus_y_plus_1_values": keys.size()}

func run() -> void:
	root.size = Vector2i(1280, 720)
	var recipe_b := OS.get_environment("SV_RECIPE") == "B"      # SV_RECIPE=B: render_loop_enabled = false and force_draw(false, 1/30) per step
	if recipe_b:
		RenderingServer.render_loop_enabled = false
	var wanted: Array = OS.get_cmdline_user_args()
	var ids := ["c01", "c02", "c03", "c04a", "c04b", "c05", "c06", "c07", "c08", "c09", "c10", "c11", "c12", "c13", "c14", "c15", "c16", "c17", "c18", "c19", "c20", "c21"]
	Common.out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(), "tolerance": TOL, "recipe": "B" if recipe_b else "A", "reading": "scale-1 pixel (x, y) against 4K pixel (3x + 1, 3y + 1): the same point of the canvas"})
	for id: String in ids:
		if wanted.size() > 0 and not (id in wanted):
			continue
		var v1 := make_route(false)
		var v3 := make_route(true)
		var c1 := Node2D.new()
		v1.add_child(c1)
		var s1 := CaptureScene.new(id)
		s1.build(c1)
		var c3 := Node2D.new()
		v3.add_child(c3)
		var s3 := CaptureScene.new(id)
		s3.build(c3)
		await process_frame
		var dur := s1.duration
		var probes := {"12 percent": int(round(0.12 * dur * 30.0)), "50 percent": int(round(0.5 * dur * 30.0)), "85 percent": int(round(0.85 * dur * 30.0))}
		var f_last := int(probes["85 percent"])
		var res: Dictionary = {}
		for f in range(0, f_last + 1):
			s1.update(float(f) / 30.0)
			s3.update(float(f) / 30.0)
			await process_frame
			if recipe_b:
				RenderingServer.force_draw(false, 1.0 / 30.0)   # recipe B (verify13): the regular loop never draws, TIME advances by this draw's frame_step
			else:
				RenderingServer.force_draw(false)
			for k: String in probes:
				if probes[k] == f:
					var a := v1.get_texture().get_image()
					var b := v3.get_texture().get_image()
					var r := compare(a, b)
					r["t_seconds"] = snappedf(float(f) / 30.0, 0.01)
					res[k] = r
		Common.out("R-route-" + id, {"scene": id, "length_seconds": dur, "at": res})
		v1.queue_free()
		v3.queue_free()
		await process_frame
		await process_frame
	quit(0)

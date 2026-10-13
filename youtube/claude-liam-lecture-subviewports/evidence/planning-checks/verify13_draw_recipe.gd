extends SceneTree
# SubViewports film, check 13: a capture recipe that does not depend on the window being drawn.
# Shader TIME advances only in a DRAW, by that draw's frame_step: a regular loop draw passes 1/30 s under --fixed-fps 30, RenderingServer.force_draw(false) passes 0.
# So a script that saves SubViewport textures and relies on force_draw(false) sees TIME stand still on every frame the regular loop skipped (a covered window).
# Recipe B: RenderingServer.render_loop_enabled = false (the regular loop never draws), then per step: update, `await process_frame`, force_draw(false, 1.0 / 30.0), read.
#  T1  TIME read from a probe at steps 0, 30, 60, 90, 120: recipe A (regular draws plus force_draw(false)) and recipe B. Both should rise by 1.0 per 30 steps.
#  T2  scene c21 (Update Mode Once at 8.5 s) under recipe B: left follows (29 at 12 s), right frozen at 323 from frame 255.
# Run: godot --path <project> --fixed-fps 30 --script res://verify13_draw_recipe.gd -- A|B|c21
func _initialize() -> void: call_deferred("run")

func first_teal(image: Image) -> int:
	for x in image.get_width():
		for y in image.get_height():
			var c := image.get_pixel(x, y)
			if c.a > 0.5 and Common.diff(c, Common.TEAL) < 0.03:
				return x
	return -1

func run() -> void:
	var mode := OS.get_cmdline_user_args()[0] if OS.get_cmdline_user_args().size() > 0 else "A"
	root.size = Vector2i(1280, 720)
	Common.out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(), "mode": mode})
	if mode == "c21":
		await run_c21()
		quit(0)
		return
	var probe := ColorRect.new()
	probe.size = Vector2(12, 12)
	probe.material = Common.material_from_code(Common.TIME_PROBE_CODE)
	root.add_child(probe)
	if mode == "B":
		RenderingServer.render_loop_enabled = false
	var out: Array = []
	for i in 121:
		await process_frame
		if mode == "B":
			RenderingServer.force_draw(false, 1.0 / 30.0)
		else:
			RenderingServer.force_draw(false)
		if i % 30 == 0:
			if mode == "B":
				RenderingServer.force_draw(false)      # a read draw with frame_step 0: it does not advance TIME
			out.append(snappedf(Common.time_of(root.get_texture().get_image(), 5, 5), 0.001))
	Common.out("T1-time-per-step-recipe-" + mode, {"TIME_at_steps_0_30_60_90_120": out, "regular_frames_drawn": Engine.get_frames_drawn(), "reading": "TIME should rise by 1.0 per 30 steps in both recipes; recipe B draws no regular frame at all, so it cannot be changed by a covered window"})
	quit(0)

func run_c21() -> void:
	RenderingServer.render_loop_enabled = false
	var canvas := Node2D.new()
	root.add_child(canvas)
	var sc := CaptureScene.new("c21")
	sc.build(canvas)
	await process_frame
	var vp0 := (sc.n["blob0"] as Node).get_parent() as SubViewport
	var vp1 := (sc.n["blob1"] as Node).get_parent() as SubViewport
	var rows: Dictionary = {}
	for f in range(0, 361):
		sc.update(float(f) / 30.0)
		await process_frame
		RenderingServer.force_draw(false, 1.0 / 30.0)
		if f in [100, 254, 255, 256, 300, 360]:
			rows[str(f)] = {"left_first_teal_x": first_teal(vp0.get_texture().get_image()), "right_first_teal_x": first_teal(vp1.get_texture().get_image())}
	Common.out("T2-c21-once-under-recipe-B", {"by_frame": rows, "regular_frames_drawn": Engine.get_frames_drawn(), "reading": "frame 255 is 8.5 s: the right picture is 323 from there on (formula 322), the left keeps following (29 at frame 360, formula 28); no regular frame was drawn"})

extends SceneTree
# SubViewports film, check 11: Update Mode Once is spent by the first DRAW after it is set, not by the first frame.
# Scene c21 has two identical pictures; at 8.5 s the right one is set to Once. At 12 s the left follows the sprite (first teal pixel near x = 28) and the right
# keeps the picture it drew at 8.5 s (near x = 322).
#  O1  one forced draw per logical frame (what Movie Maker does): the right picture is frozen at x = 322 to 323, every run.
#  O2  the same scene stepped with `await process_frame` only, then read, then one forced draw, then read again. When the window was not drawn on the frames in between,
#      the first read shows a picture from a different moment, and the forced draw then spends the pending Once on the 12 s state (x = 29). Not asserted: it depends on
#      whether other windows cover this one. Printed so the failure mode stays on record.
# Run: godot --path <project> --fixed-fps 30 --script res://verify11_once_needs_a_draw.gd

func _initialize() -> void: call_deferred("run")

func first_teal(image: Image) -> int:
	for x in image.get_width():
		for y in image.get_height():
			var c := image.get_pixel(x, y)
			if c.a > 0.5 and Common.diff(c, Common.TEAL) < 0.03:
				return x
	return -1

func vp_of(sc: CaptureScene, node_name: String) -> SubViewport:
	return (sc.n[node_name] as Node).get_parent() as SubViewport

func run() -> void:
	root.size = Vector2i(1280, 720)
	Common.out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method()})
	var left_edge := 0.30 * 448.0 * 0.6
	var formula_live := 256.0 + 150.0 * sin(0.9 * 12.0) - left_edge
	var formula_once := 256.0 + 150.0 * sin(0.9 * 8.5) - left_edge
	# ---- O1
	var canvas := Node2D.new()
	root.add_child(canvas)
	var sc := CaptureScene.new("c21")
	sc.build(canvas)
	await process_frame
	var right_at: Dictionary = {}
	for f in range(0, 361):
		sc.update(float(f) / 30.0)
		await process_frame
		RenderingServer.force_draw(false)
		if f in [254, 255, 256, 300, 360]:
			right_at[str(f)] = first_teal(vp_of(sc, "blob1").get_texture().get_image())
	var left_end := first_teal(vp_of(sc, "blob0").get_texture().get_image())
	Common.out("O1-once-with-a-forced-draw-per-frame", {"right_first_teal_x_by_frame": right_at, "left_first_teal_x_at_12_s": left_end, "left_by_formula": snappedf(formula_live, 1.0), "right_frozen_by_formula": snappedf(formula_once, 1.0),
		"reading": "frame 255 is 8.5 s: the right picture takes the 8.5 s state and then stays; the left keeps following"})
	canvas.queue_free()
	await process_frame
	await process_frame
	# ---- O2
	canvas = Node2D.new()
	root.add_child(canvas)
	sc = CaptureScene.new("c21")
	sc.build(canvas)
	await process_frame
	for f in range(0, 361):
		sc.update(float(f) / 30.0)
		await process_frame
	var before := first_teal(vp_of(sc, "blob1").get_texture().get_image())
	RenderingServer.force_draw(false)
	var after := first_teal(vp_of(sc, "blob1").get_texture().get_image())
	Common.out("O2-once-with-regular-frames-only-NOT-ASSERTED", {"right_first_teal_x_before_any_forced_draw": before, "right_first_teal_x_after_one_forced_draw": after, "right_frozen_by_formula": snappedf(formula_once, 1.0), "left_by_formula": snappedf(formula_live, 1.0),
		"reading": "the first number can be anything between the frozen picture and the 12 s picture when the window was not drawn on every frame; a change after the forced draw means a pending Once was spent late"})
	quit(0)

extends SceneTree
# SubViewports film, check 10: are the main loop's frames really drawn when a script runs in a window?
# Found while chasing a Update Mode Once reading that changed from run to run (RESULTS.md, "the covered window"): on this Mac a Godot window that other windows cover
# is drawn on only about 4 of every 10 frames. A script that waits for "N frames" then gets about 0.4 N draws, and a viewport set to Once may not have drawn yet.
# RenderingServer.force_draw(false) is a draw that always happens. Movie Maker (--write-movie) writes one new picture per frame whatever the window does.
# Run it three ways (run-all-checks.sh does): no flag, --always-on-top, --position 0,0.   godot --path <project> --fixed-fps 30 [flag] --script res://verify10_draw_skipping.gd

var post := 0

func _initialize() -> void: call_deferred("run")

func count(steps: int, force: bool, r: ColorRect) -> Dictionary:
	post = 0
	var d0 := Engine.get_frames_drawn()
	var p0 := Engine.get_process_frames()
	for i in steps:
		r.position.x = i % 1000
		await process_frame
		if force:
			RenderingServer.force_draw(false)
	return {"process_frames": Engine.get_process_frames() - p0, "frames_drawn_by_the_regular_loop": Engine.get_frames_drawn() - d0, "frame_post_draw_signals": post}

func run() -> void:
	root.size = Vector2i(1280, 720)
	var flags: Array = []
	for a: String in OS.get_cmdline_args():
		if a.begins_with("--always-on-top") or a.begins_with("--position"):
			flags.append(a)
	RenderingServer.frame_post_draw.connect(func(): post += 1)
	var r := ColorRect.new()
	r.size = Vector2(100, 100)
	root.add_child(r)
	for i in 90:                      # warm-up: let the window settle (a window that another window covers is noticed a moment after it opens)
		await process_frame
	var a1: Dictionary = await count(300, false, r)
	var b: Dictionary = await count(300, true, r)
	var a2: Dictionary = await count(300, false, r)
	Common.out("D-draws-per-frame", {"window_flags": flags, "waiting_only_first": a1, "with_one_force_draw_per_step": b, "waiting_only_again": a2,
		"reading": "frames_drawn_by_the_regular_loop below process_frames means the window was not drawn on some frames. In the forced phase every step is drawn (frame_post_draw_signals counts the forced draws plus any regular ones)"})
	quit(0)

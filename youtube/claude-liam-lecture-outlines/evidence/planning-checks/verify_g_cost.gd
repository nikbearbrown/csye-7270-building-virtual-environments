extends SceneTree
# G: what does an outline cost?  Two attempts, both labelled in the log:
#  G1: ask the engine for the graphics card's time for a SIZE x SIZE SubViewport redrawn every frame (viewport_get_measured_render_time_gpu), the same call
#      the earlier planning runs used; 0.0 means the counter is not available on this setup.
#  G2: wall-clock time per frame with vsync off for the same SubViewport (4096: every variant read 8.3 ms, the display's pace, so nothing could be learned; 8192 is the heavier attempt) and shaders with 1, 5, 9, 10, 17, 26, 50 and 82 texture reads per pixel,
#      three interleaved rounds (other programs may share the graphics card: the spread between rounds is the honesty check).
# Run: godot --path <scratch project> --script res://verify_g_cost.gd
const Lib := preload("res://ol_lib.gd")
var N := 6                # how many identical render targets are redrawn every frame (so even the cheapest shader takes longer than the display's 8.33 ms)
var SIZE := 8192          # side of the square render target in pixels (4096 was display-paced at 8.33 ms per frame: inconclusive, see RESULTS.md)

func _initialize() -> void: call_deferred("run")
func frames(n: int) -> void:
	for i in range(n): await process_frame
func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func median(a: Array) -> float:
	var b := a.duplicate()
	b.sort()
	return b[b.size() / 2]

func run() -> void:
	root.size = Vector2i(640, 360)
	# A covered, hidden or minimized window stops drawing and every frame then takes the idle time (about 6.9 ms here): keep the window on top.
	DisplayServer.window_set_flag(DisplayServer.WINDOW_FLAG_ALWAYS_ON_TOP, true)
	DisplayServer.window_move_to_foreground()
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	RenderingServer.set_default_clear_color(Lib.STAGE)
	var subs: Array = []
	var sprites: Array = []
	for k in range(N):
		var sub := SubViewport.new()
		sub.size = Vector2i(SIZE, SIZE)
		sub.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		root.add_child(sub)
		var sp := Sprite2D.new()
		sp.texture = ImageTexture.create_from_image(Lib.blob(128))
		sp.centered = false
		sp.scale = Vector2(SIZE / 128.0, SIZE / 128.0)   # 128 image pixels -> SIZE render pixels: every render pixel runs the fragment shader
		sp.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		sub.add_child(sp)
		subs.append(sub)
		sprites.append(sp)
	var rid: RID = subs[0].get_viewport_rid()
	RenderingServer.viewport_set_measure_render_time(rid, true)
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(),
		"adapter": RenderingServer.get_video_adapter_name(), "viewport": [SIZE, SIZE], "render_targets_per_frame": N, "vsync": DisplayServer.window_get_vsync_mode()})

	var variants: Array = [
		["plain sprite, no shader", "", {}, 1],
		["06-pixel-steps (4 + 1 reads)", "06-pixel-steps.gdshader", {"thickness": 1.0}, 5],
		["07-eight-reads (8 + 1)", "07-eight-reads.gdshader", {"thickness": 1.0}, 9],
		["08-loop (9 + 1)", "08-loop.gdshader", {"thickness": 1.0}, 10],
		["10-ring (16 + 1), sine and cosine per read", "10-ring.gdshader", {"thickness": 1.0}, 17],
		["ring-const (16 + 1), directions as constants", "ring-const.gdshader", {"thickness": 1.0}, 17],
		["loop-5 constant bounds (25 + 1)", "loop-5.gdshader", {"thickness": 1.0}, 26],
		["loop-7 constant bounds (49 + 1)", "loop-7.gdshader", {"thickness": 1.0}, 50],
		["loop-9 constant bounds (81 + 1)", "loop-9.gdshader", {"thickness": 1.0}, 82],
		["loop-n r=1, runtime bounds (9 + 1)", "loop-n.gdshader", {"thickness": 1.0, "r": 1}, 10],
		["loop-n r=2, runtime bounds (25 + 1)", "loop-n.gdshader", {"thickness": 1.0, "r": 2}, 26],
		["09-guard at thickness 0 (1 read)", "09-guard.gdshader", {"thickness": 0.0}, 1],
	]
	var gpu_all: Array = []
	var results: Dictionary = {}
	for round in range(3):
		for v in variants:
			var mat: ShaderMaterial = null
			if v[1] != "":
				mat = Lib.material(v[1], v[2])
			for sp in sprites:
				sp.material = mat
			await frames(15)
			var times: Array = []
			var last := Time.get_ticks_usec()
			for i in range(60):
				await process_frame
				var now := Time.get_ticks_usec()
				times.append((now - last) / 1000.0)
				last = now
				gpu_all.append(RenderingServer.viewport_get_measured_render_time_gpu(rid))
			var key: String = v[0]
			if not results.has(key): results[key] = []
			results[key].append(snappedf(median(times), 0.01))
	var gmax := 0.0
	for g in gpu_all: gmax = maxf(gmax, g)
	out("G1-gpu-timer", {"samples": gpu_all.size(), "max_ms": gmax, "reading": "0.0 in every sample means the engine's GPU timer is not available on this setup"})
	for v in variants:
		out("G2-wallclock", {"variant": v[0], "reads_per_pixel": v[3], "median_ms_per_frame_by_round": results[v[0]], "min_ms": results[v[0]].min(), "max_ms": results[v[0]].max()})
	out("G2-note", {"pixels_shaded_per_frame": N * SIZE * SIZE})
	quit(0)

extends SceneTree
# verify9: does filter_nearest on the screen texture make a magnified edge hard? A 50x magnified tile edge read three ways (filter_nearest, filter_linear, no hint):
# a hard step is one jump between two neighbouring pixels, a ramp is many small steps. Saves the zoomed picture for each hint.
# Run: ./run-checks.sh verify9 [forward_plus|gl_compatibility]
const L = preload("res://rts_lib.gd")
const SIZE := Vector2(1280, 720)

func _initialize() -> void: call_deferred("run")

func frames(n: int) -> void:
	for i in range(n): await process_frame

func run() -> void:
	root.size = Vector2i(1280, 720)
	RenderingServer.set_default_clear_color(L.STAGE)
	L.out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method()})
	var code := "shader_type canvas_item;\nuniform sampler2D s : hint_screen_texture%s;\nvoid fragment() { COLOR.rgb = texture(s, vec2(0.5, 0.25) + (SCREEN_UV - vec2(0.5)) * 0.02).rgb; }\n"
	var main: Node2D = null
	for pair in [["nearest", ", filter_nearest"], ["linear", ", filter_linear"], ["none", ""]]:
		if main != null:
			main.queue_free()
			await frames(2)
		main = Node2D.new()
		root.add_child(main)
		L.build_world(main, SIZE)
		var r := L.rect(Vector2(0, 0), SIZE, Color.WHITE, "Zoom")
		r.material = L.mat_from(code % pair[1])
		main.add_child(r)
		await frames(4)
		var img := L.grab(root)
		# row across the magnified tile edge at the window centre; print 12 consecutive pixels around the middle
		var y := 360
		var row: Array = []
		for x in range(634, 646):
			row.append(snappedf(img.get_pixel(x, y).r, 0.001))
		L.out("zoom-" + pair[0], {"red_channel_x634_to_645": row, "renderer": RenderingServer.get_current_rendering_method()})
		img.save_png("/private/tmp/claude-501/rts-checks/shots/zoom-" + pair[0] + "-" + RenderingServer.get_current_rendering_method() + ".png")
	quit(0)

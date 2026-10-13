extends SceneTree
# verify_scene_file.gd: loads the editor project's pond.tscn (make-editor-project.sh) and checks it behaves like the scripted scene:
# the tree order, the Inspector values the narration names, the reflection over water at x = 300, and none over the sandbar at x = 880.
# Run: godot --path <editor project> --script res://verify_scene_file.gd   (copy this file into the editor project first)
func _initialize() -> void:
	call_deferred("run")

func frames(n: int) -> void:
	for i in range(n):
		await process_frame

func grab() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func count_diff(a: Image, b: Image, x: int) -> int:
	var n := 0
	for sy in range(302, 542):
		for sx in range(x - 120, x + 120):
			var pa := a.get_pixel(sx, sy)
			var pb := b.get_pixel(sx, sy)
			if absf(pa.r - pb.r) + absf(pa.g - pb.g) + absf(pa.b - pb.b) > 0.03:
				n += 1
	return n

func run() -> void:
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	root.size = Vector2i(1280, 720)
	var scene: Node = load("res://pond.tscn").instantiate()
	root.add_child(scene)
	var names := []
	for c in scene.get_children():
		names.append(c.name + (" > " + c.get_child(0).name if c.get_child_count() > 0 else ""))
	var bbc: BackBufferCopy = scene.get_node("BackBufferCopy")
	print("RESULT " + JSON.stringify({"tree_order": names, "copy_mode": bbc.copy_mode, "copy_mode_is_viewport": bbc.copy_mode == BackBufferCopy.COPY_MODE_VIEWPORT,
		"reflection_flip_v": scene.get_node("Reflection").flip_v, "remote_path": str(scene.get_node("Player/RemoteTransform2D").remote_path)}))
	for x in [300, 880]:
		scene.get_node("Player").position.x = x
		await frames(4)
		var a := grab()
		scene.get_node("Reflection").visible = false
		await frames(3)
		var b := grab()
		scene.get_node("Reflection").visible = true
		print("RESULT " + JSON.stringify({"player_x": x, "reflection_pixels_visible": count_diff(a, b, x), "expected": 16237 if x == 300 else 0, "renderer": RenderingServer.get_current_rendering_method()}))
	quit(0)

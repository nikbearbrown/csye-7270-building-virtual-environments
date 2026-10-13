extends SceneTree
# Check 11: how far is the drawn top edge of a rippled flag from the true sine, for 4, 10 and 32 straight pieces?
# Same shader as the film (04-ripple, 24 px high wave, 8 radians across a 288 px flag), but the node is scaled 3x so one screen pixel is a third of a logical pixel.
# The frames are saved; the measuring is done by analyze_densities.py (Pillow). Run: godot --path <proj> --script res://verify11.gd
const V = preload("res://vscene.gd")
const CS = preload("res://capture_scenes.gd")

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	V.setup(root, 1280, 720)
	var holder := Node2D.new()
	root.add_child(holder)
	var img := CS.flag_image(288, 144)
	var mat := V.material_from(V.lab_shader("04-ripple"))
	var out_dir := V.png_dir()
	for n in [3, 9, 31]:
		var m := V.quad(Vector2(288, -144), n, 0, img, Vector2(640, 360), mat)
		m.scale = Vector2(3, 3)
		holder.add_child(m)
		await V.frames(self, 4)
		var im := V.grab(root)
		im.save_png("%s/density-x3-subdivide-%d.png" % [out_dir, n])
		V.out("11-density-frame", {"subdivide_width": n, "pieces": n + 1, "node_scale": 3})
		holder.remove_child(m)
		m.queue_free()
		await V.frames(self, 2)
	quit(0)

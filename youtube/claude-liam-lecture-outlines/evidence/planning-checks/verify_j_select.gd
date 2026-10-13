extends SceneTree
# J: the game drives the dial.
#  J1: the exact script shown on screen (select_snippet.gd) on a node with a Sprite2D child named Sprite and 09-guard.gdshader: a pushed key event
#      turns the outline on (thickness 2), a second one turns it off; count line-coloured pixels before, after one press, after two.
#  J2: two instances of one packed scene share the material by default, so one set_shader_parameter outlines both;
#      with resource_local_to_scene = true on the material, each instance gets its own; material.duplicate() does the same by hand.
# Run: godot --path <scratch project> --script res://verify_j_select.gd -- --out <png dir>
const Lib := preload("res://ol_lib.gd")
var OUT := "/tmp"

func _initialize() -> void: call_deferred("run")
func frames(n: int) -> void:
	for i in range(n): await process_frame
func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func line_px(img: Image, x0: int, y0: int, x1: int, y1: int) -> int:
	var n := 0
	for y in range(y0, y1):
		for x in range(x0, x1):
			var c := img.get_pixel(x, y)
			if absf(c.r - 0.25) < 0.02 and absf(c.g - 0.25) < 0.02 and absf(c.b - 0.75) < 0.02:
				n += 1
	return n

func key() -> void:
	var ev := InputEventKey.new()
	ev.keycode = KEY_SPACE
	ev.physical_keycode = KEY_SPACE
	ev.pressed = true
	root.push_input(ev)
	var up := InputEventKey.new()
	up.keycode = KEY_SPACE
	up.physical_keycode = KEY_SPACE
	up.pressed = false
	root.push_input(up)

func make_unit(pos: Vector2, scale: float, shared_mat: ShaderMaterial = null) -> Node2D:
	var unit := Node2D.new()
	var sp := Sprite2D.new()
	sp.name = "Sprite"
	sp.texture = ImageTexture.create_from_image(Lib.blob(128))
	sp.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	sp.scale = Vector2(scale, scale)
	sp.material = shared_mat if shared_mat != null else Lib.material("09-guard.gdshader", {"line_color": Color(0.25, 0.25, 0.75, 1.0)})
	unit.add_child(sp)
	unit.position = pos
	return unit

func run() -> void:
	var a := OS.get_cmdline_user_args()
	for i in range(a.size()):
		if a[i] == "--out": OUT = a[i + 1]
	RenderingServer.set_default_clear_color(Lib.STAGE)
	root.size = Vector2i(640, 360)
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method()})

	# ---- J1
	var holder := Node.new()
	var scr := GDScript.new()
	scr.source_code = FileAccess.get_file_as_string(Lib.film_dir().path_join("evidence/planning-checks/select_snippet.gd"))
	var err := scr.reload()
	holder.set_script(scr)
	var spr := Sprite2D.new()                      # the script's $Sprite: a Sprite2D child with the guarded outline shader
	spr.name = "Sprite"
	spr.texture = ImageTexture.create_from_image(Lib.blob(128))
	spr.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	spr.position = Vector2(320, 180)
	spr.material = Lib.material("09-guard.gdshader", {"line_color": Color(0.25, 0.25, 0.75, 1.0)})
	holder.add_child(spr)
	root.add_child(holder)
	await frames(3)
	var before := line_px(Lib.snap(root), 0, 0, 640, 360)
	Lib.save(Lib.snap(root), OUT + "/select-0-unselected.png")
	key()
	await frames(3)
	var im1 := Lib.snap(root)
	Lib.save(im1, OUT + "/select-1-selected.png")
	var after_one := line_px(im1, 0, 0, 640, 360)
	key()
	await frames(3)
	var after_two := line_px(Lib.snap(root), 0, 0, 640, 360)
	out("J1-select-toggle", {"script_reload_error": err, "line_px_unselected": before, "line_px_after_first_key": after_one, "line_px_after_second_key": after_two,
		"thickness_now": spr.material.get_shader_parameter("thickness")})
	holder.queue_free()
	await frames(2)

	# ---- J2: two instances of one scene
	for mode in ["shared-by-default", "local-to-scene", "duplicate"]:
		var proto := Node2D.new()
		var sp := Sprite2D.new()
		sp.name = "Sprite"
		sp.texture = ImageTexture.create_from_image(Lib.blob(128))
		sp.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		var mat := Lib.material("09-guard.gdshader", {"thickness": 0.0, "line_color": Color(0.25, 0.25, 0.75, 1.0)})
		if mode == "local-to-scene":
			mat.resource_local_to_scene = true
		sp.material = mat
		proto.add_child(sp)
		sp.owner = proto
		var ps := PackedScene.new()
		ps.pack(proto)
		var u1: Node2D = ps.instantiate()
		var u2: Node2D = ps.instantiate()
		u1.position = Vector2(160, 180)
		u2.position = Vector2(480, 180)
		root.add_child(u1)
		root.add_child(u2)
		if mode == "duplicate":
			u2.get_node("Sprite").material = u2.get_node("Sprite").material.duplicate()
		await frames(3)
		u1.get_node("Sprite").material.set_shader_parameter("thickness", 3.0)
		await frames(3)
		var im := Lib.snap(root)
		Lib.save(im, OUT + "/shared-" + mode + ".png")
		out("J2-" + mode, {"same_material_object": u1.get_node("Sprite").material == u2.get_node("Sprite").material,
			"line_px_left_unit_set_to_3": line_px(im, 0, 0, 320, 360), "line_px_right_unit_never_set": line_px(im, 320, 0, 640, 360)})
		u1.queue_free(); u2.queue_free(); proto.queue_free()
		await frames(2)
	# ---- J3: per-instance uniform (instance uniform + CanvasItem.set_instance_shader_parameter): one shared material, a value per node
	var proto3 := Node2D.new()
	var sp3 := Sprite2D.new()
	sp3.name = "Sprite"
	sp3.texture = ImageTexture.create_from_image(Lib.blob(128))
	sp3.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	sp3.material = Lib.material("13-instance.gdshader", {"line_color": Color(0.25, 0.25, 0.75, 1.0)})
	proto3.add_child(sp3)
	sp3.owner = proto3
	var ps3 := PackedScene.new()
	ps3.pack(proto3)
	var v1: Node2D = ps3.instantiate()
	var v2: Node2D = ps3.instantiate()
	v1.position = Vector2(160, 180)
	v2.position = Vector2(480, 180)
	root.add_child(v1)
	root.add_child(v2)
	await frames(3)
	var im0 := Lib.snap(root)
	var before3 := [line_px(im0, 0, 0, 320, 360), line_px(im0, 320, 0, 640, 360)]
	v1.get_node("Sprite").set_instance_shader_parameter("thickness", 3.0)
	await frames(3)
	var im3 := Lib.snap(root)
	Lib.save(im3, OUT + "/shared-instance-uniform.png")
	out("J3-instance-uniform", {"same_material_object": v1.get_node("Sprite").material == v2.get_node("Sprite").material,
		"line_px_before_left_right": before3, "line_px_left_set_to_3": line_px(im3, 0, 0, 320, 360), "line_px_right_never_set": line_px(im3, 320, 0, 640, 360),
		"get_instance_shader_parameter_left": v1.get_node("Sprite").get_instance_shader_parameter("thickness")})
	quit(0)

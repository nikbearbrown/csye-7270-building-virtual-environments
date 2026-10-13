extends SceneTree
# Experiment F (Reflections layout): does the copy follow z index and canvas layers, not only tree order?
# Docs: "Canvas items are drawn in tree order on their canvas layer" (CanvasItem); z_index: "The order in which this node is drawn.
# A node with a higher Z index will display in front of others."; canvas layers: "Layers with a greater number will be drawn above
# those with a smaller number."  Question: does a BackBufferCopy take its copy at its place in THAT order?
#
#   Z1  tree order is wrong on purpose (Ground first), z_index puts the label map below it: Ground z=1, Player/Reflection z=2, label map and copy z=0
#   Z2  the label map lives on a CanvasLayer with layer -1; copy, ground, player and reflection on the default layer
#   Z3  label map and copy together on a CanvasLayer with layer -1; ground, player and reflection on the default layer
#   Z5  everything on one CanvasLayer (layer 1): mask, copy, ground, player, reflection
#   Z6  copy on layer 0 with the mask, but the reflection (the reader) on a higher CanvasLayer (layer 1)
#   Z4  control: the plain good tree order
# Run: godot --path <scratch project> --script res://exp_f_z_index_and_layers.gd
const P = preload("res://pond_common.gd")
const SHADERS := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-reflections/lab-shaders/"

var tex := {}
var holder: Node

func _initialize() -> void:
	call_deferred("run")

func frames(n: int) -> void:
	for i in range(n):
		await process_frame

func grab() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func out(id: String, d: Dictionary) -> void:
	d["case"] = id
	d["renderer"] = RenderingServer.get_current_rendering_method()
	print("RESULT " + JSON.stringify(d))

func make_nodes(x: float) -> Dictionary:
	var mask := Sprite2D.new()
	mask.name = "LabelMap"
	mask.texture = tex["mask"]
	mask.centered = false
	var ground := Sprite2D.new()
	ground.name = "Ground"
	ground.texture = tex["ground"]
	ground.centered = false
	var bbc := BackBufferCopy.new()
	bbc.name = "BackBufferCopy"
	bbc.copy_mode = BackBufferCopy.COPY_MODE_VIEWPORT
	var player := Sprite2D.new()
	player.name = "Player"
	player.texture = tex["char"]
	player.position = Vector2(x, P.PLAYER_Y)
	var rt := RemoteTransform2D.new()
	rt.position = Vector2(0, P.REFLECT_OFFSET)
	player.add_child(rt)
	var refl := Sprite2D.new()
	refl.name = "Reflection"
	refl.texture = tex["char"]
	refl.flip_v = true
	refl.material = P.load_shader("02-reflection.gdshader", SHADERS)
	return {"mask": mask, "ground": ground, "bbc": bbc, "player": player, "rt": rt, "refl": refl}

func count_visible(n: Dictionary, x: float) -> Dictionary:
	await frames(4)
	var a := grab()
	n["refl"].visible = false
	await frames(3)
	var b := grab()
	n["refl"].visible = true
	var vis := 0
	var leak := 0
	for y in range(P.H):
		for xx in range(P.W):
			var pa := a.get_pixel(xx, y)
			if y >= int(P.PLAYER_Y + P.REFLECT_OFFSET) - P.SPRITE_N / 2 and y < int(P.PLAYER_Y + P.REFLECT_OFFSET) + P.SPRITE_N / 2 and absi(xx - int(x)) < P.SPRITE_N / 2:
				var pb := b.get_pixel(xx, y)
				if absf(pa.r - pb.r) + absf(pa.g - pb.g) + absf(pa.b - pb.b) > 0.03:
					vis += 1
			if (y % 2 == 0 and xx % 2 == 0) and (Vector3(pa.r - 1.0, pa.g, pa.b).length() < 0.2 or Vector3(pa.r, pa.g - 1.0, pa.b).length() < 0.2):
				leak += 4
	return {"reflection_pixels_visible": vis, "reference_if_it_worked": 16237, "mask_coloured_pixels_in_final_frame": leak}

func fresh() -> void:
	if holder != null:
		holder.queue_free()
		await process_frame
	holder = Node2D.new()
	root.add_child(holder)

func run() -> void:
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	root.size = Vector2i(P.W, P.H)
	await frames(3)
	tex["mask"] = ImageTexture.create_from_image(P.make_mask_image())
	tex["ground"] = ImageTexture.create_from_image(P.make_ground_image())
	tex["char"] = ImageTexture.create_from_image(P.make_character_image())

	# Z4 control
	await fresh()
	var n := make_nodes(300.0)
	for k in ["mask", "bbc", "ground", "player", "refl"]:
		holder.add_child(n[k])
	n["rt"].remote_path = n["rt"].get_path_to(n["refl"])
	out("Z4-control-plain-tree-order", await count_visible(n, 300.0))

	# Z1 z_index does the ordering; the tree order alone would draw the label map on top
	await fresh()
	n = make_nodes(300.0)
	n["ground"].z_index = 1
	n["player"].z_index = 2
	n["refl"].z_index = 2
	for k in ["ground", "mask", "bbc", "player", "refl"]:
		holder.add_child(n[k])
	n["rt"].remote_path = n["rt"].get_path_to(n["refl"])
	out("Z1-z-index-puts-the-mask-below-the-ground-(tree-order-says-the-opposite)", await count_visible(n, 300.0))

	# Z2 mask on a lower canvas layer, copy on the default layer
	await fresh()
	n = make_nodes(300.0)
	var cl := CanvasLayer.new()
	cl.layer = -1
	holder.add_child(cl)
	cl.add_child(n["mask"])
	for k in ["bbc", "ground", "player", "refl"]:
		holder.add_child(n[k])
	n["rt"].remote_path = n["rt"].get_path_to(n["refl"])
	out("Z2-mask-on-canvas-layer-minus-1,-copy-on-layer-0", await count_visible(n, 300.0))

	# Z3 mask AND copy on the lower canvas layer
	await fresh()
	n = make_nodes(300.0)
	var cl3 := CanvasLayer.new()
	cl3.layer = -1
	holder.add_child(cl3)
	cl3.add_child(n["mask"])
	cl3.add_child(n["bbc"])
	for k in ["ground", "player", "refl"]:
		holder.add_child(n[k])
	n["rt"].remote_path = n["rt"].get_path_to(n["refl"])
	out("Z3-mask-and-copy-both-on-canvas-layer-minus-1", await count_visible(n, 300.0))
	# Z5 everything on one canvas layer
	await fresh()
	n = make_nodes(300.0)
	var cl5 := CanvasLayer.new()
	cl5.layer = 1
	holder.add_child(cl5)
	for k in ["mask", "bbc", "ground", "player", "refl"]:
		cl5.add_child(n[k])
	n["rt"].remote_path = n["rt"].get_path_to(n["refl"])
	out("Z5-everything-on-one-canvas-layer-(layer-1)", await count_visible(n, 300.0))

	# Z6 reader on a higher layer than the copy
	await fresh()
	n = make_nodes(300.0)
	for k in ["mask", "bbc", "ground", "player"]:
		holder.add_child(n[k])
	var cl6 := CanvasLayer.new()
	cl6.layer = 1
	holder.add_child(cl6)
	cl6.add_child(n["refl"])
	n["rt"].remote_path = n["rt"].get_path_to(n["refl"])
	out("Z6-copy-on-layer-0-but-the-reflection-on-layer-1", await count_visible(n, 300.0))
	quit(0)

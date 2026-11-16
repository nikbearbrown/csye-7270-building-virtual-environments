extends SceneTree
# tools/make_scene.gd: writes scenes/water.tscn, the finished cove, using the same builder as the film's captures (scripts/cove_builder.gd).
# Run once from the project folder:   godot --headless --path . --script tools/make_scene.gd
# The water is a PlaneMesh cut 127 x 127 wearing a ShaderMaterial of shaders/06-shore-foam.gdshader with two NoiseTexture2D normal maps; a driver
# node feeds the shader's wave clock and puts the buoy and the crate on the surface. Every shader of the film is in shaders/: assign any of them to the
# material's Shader slot to follow one stage at a time (the stages before the vertex waves have no wave_clock; the driver ignores what is missing).
const Builder = preload("res://scripts/cove_builder.gd")

func _initialize() -> void:
	var root := Node3D.new()
	root.name = "Cove"
	var mat := ShaderMaterial.new()
	mat.shader = load("res://shaders/06-shore-foam.gdshader")
	var made := Builder.feed_textures(mat)
	Builder.add_environment(root)
	var nodes := Builder.add_cove(root, mat, 127, false, true)
	Builder.add_camera(root, "iso")
	var driver := Node.new()
	driver.name = "WaterDriver"
	driver.set_script(load("res://scripts/water_driver.gd"))
	driver.water = nodes["water"]
	var fl: Array[Node3D] = [nodes["buoy"], nodes["crate"]]
	driver.floaters = fl
	root.add_child(driver)
	_own(root, root)
	var packed := PackedScene.new()
	var err := packed.pack(root)
	print("pack: ", error_string(err))
	err = ResourceSaver.save(packed, "res://scenes/water.tscn")
	print("save scenes/water.tscn: ", error_string(err))
	ResourceSaver.save(mat, "res://materials/water_final.tres")
	print("textures: ", made.keys())
	quit()

func _own(n: Node, owner_node: Node) -> void:
	for c in n.get_children():
		c.owner = owner_node
		_own(c, owner_node)

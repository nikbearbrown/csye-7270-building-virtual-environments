extends SceneTree
func dump_material(label: String, m: Material) -> void:
	print("== ", label, " class=", m.get_class())
	if m is BaseMaterial3D:
		var b: BaseMaterial3D = m
		print("albedo_texture=", b.albedo_texture.resource_path if b.albedo_texture else "none")
		print("normal_enabled=", b.normal_enabled, " normal_texture=", b.normal_texture.resource_path if b.normal_texture else "none")
		print("roughness_texture=", b.roughness_texture.resource_path if b.roughness_texture else "none", " channel=", b.roughness_texture_channel)
		print("metallic_texture=", b.metallic_texture.resource_path if b.metallic_texture else "none", " channel=", b.metallic_texture_channel, " metallic=", b.metallic)
		print("ao_enabled=", b.ao_enabled, " ao_texture=", b.ao_texture.resource_path if b.ao_texture else "none")
		print("transparency=", b.transparency, " alpha_scissor=", b.alpha_scissor_threshold, " cull=", b.cull_mode)
		var sh_rid: RID = b.get_shader_rid()
		var src := RenderingServer.shader_get_code(sh_rid)
		print("GENERATED_SHADER_LEN=", src.length())
		for line in src.split("\n"):
			if line.begins_with("uniform sampler2D") or line.begins_with("render_mode"):
				print("   ", line)
func _initialize() -> void:
	var ps: PackedScene = load("res://polyhaven/dutch_ship_medium_1k.gltf")
	var ship := ps.instantiate()
	root.add_child(ship)
	var seen := {}
	for mi in ship.find_children("*", "MeshInstance3D", true, false):
		var mesh: Mesh = mi.mesh
		for s in mesh.get_surface_count():
			var m := mesh.surface_get_material(s)
			if m and not seen.has(m):
				seen[m] = true
				dump_material(str(mi.name) + " surface " + str(s) + " " + m.resource_name, m)
	var orm := ORMMaterial3D.new()
	dump_material("fresh ORMMaterial3D (no textures)", orm)
	orm.albedo_texture = load("res://polyhaven/textures/dutch_ship_medium_hull_diff_1k.jpg")
	orm.orm_texture = load("res://polyhaven/textures/dutch_ship_medium_hull_arm_1k.jpg")
	orm.normal_enabled = true
	orm.normal_texture = load("res://polyhaven/textures/dutch_ship_medium_hull_nor_gl_1k.jpg")
	var src := RenderingServer.shader_get_code(orm.get_shader_rid())
	print("== ORM with textures GENERATED_SHADER_LEN=", src.length())
	for line in src.split("\n"):
		if line.begins_with("uniform sampler2D") or line.begins_with("render_mode"):
			print("   ", line)
	quit(0)

# check_colours.gd - headless: the albedo colour Godot gives each surface of each imported .glb.
#   godot --headless --path <project> --script res://tests/check_colours.gd --fixed-fps 60 -- res://assets/crate.glb ...
extends SceneTree


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	if args.is_empty():
		args = PackedStringArray(["res://assets/crate.glb", "res://assets/lantern.glb", "res://assets/coin.glb"])
	for path in args:
		var inst: Node = (load(path) as PackedScene).instantiate()
		print(path.get_file())
		for mi in inst.find_children("*", "MeshInstance3D", true, false):
			var mesh: Mesh = (mi as MeshInstance3D).mesh
			for s in mesh.get_surface_count():
				var mat := mesh.surface_get_material(s) as StandardMaterial3D
				print("  surface %d  material %-12s albedo %s  metallic %s roughness %s" % [s, mat.resource_name, "#" + mat.albedo_color.to_html(false).to_upper(), snappedf(mat.metallic, 0.001), snappedf(mat.roughness, 0.001)])
		inst.free()
	quit()

extends SceneTree
## Loads hint_experiment.tscn as the game does and prints what decides the look:
## the environment's tonemap, exposure, glow, fog and adjustments, which the
## scene file leaves out when they are at their defaults; each quad's mesh,
## material and shader parameters; and the camera. It reads the scene and
## writes nothing.
##
## From assignment-5/, against the godot/ project:
##   timeout 120 godot --headless --path godot --script "$PWD/evidence/headless-probe/probe_hint_scene.gd"


func _init() -> void:
	var scene := (load("res://scenes/hint_experiment.tscn") as PackedScene).instantiate()
	var tonemappers := ClassDB.class_get_enum_constants(&"Environment", &"ToneMapper")
	var e := (scene.get_node("WorldEnvironment") as WorldEnvironment).environment
	print("PROBE environment: tonemap %s, exposure %s, glow %s, fog %s, adjustments %s, background %s" % [
		tonemappers[e.tonemap_mode], e.tonemap_exposure, e.glow_enabled, e.fog_enabled, e.adjustment_enabled, e.background_color.to_html(false)])
	for quad_name: String in ["QuadA", "QuadB"]:
		var quad := scene.get_node(quad_name) as MeshInstance3D
		var m := quad.material_override as ShaderMaterial
		var parts: PackedStringArray = []
		for u: Dictionary in m.shader.get_shader_uniform_list():
			var v: Variant = m.get_shader_parameter(u.name)
			parts.append("%s = %s" % [u.name, (v as Resource).resource_path if v is Resource else str(v)])
		print("PROBE %s: %s %s at %s; material %s; shader %s; %s" % [
			quad_name, quad.mesh.get_class(), (quad.mesh as QuadMesh).size, quad.position, m.resource_path, m.shader.resource_path, ", ".join(parts)])
	var camera := scene.get_node("Camera") as Camera3D
	print("PROBE camera: current %s, at %s, looking along %s, fov %s" % [camera.current, camera.position, -camera.transform.basis.z, camera.fov])
	scene.free()
	quit(0)

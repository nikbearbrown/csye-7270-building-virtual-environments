# Written for the film (B52): what happens if the colour line is moved into vertex(), and the corner arithmetic.
# Run: godot --headless --path <any empty project folder> --script res://vertex_albedo_check.gd
extends SceneTree
func try_shader(label: String, code: String) -> void:
	print("CASE ", label)
	var shader := Shader.new()
	shader.code = code
	print("UNIFORMS ", shader.get_shader_uniform_list().size())
func _initialize() -> void:
	# 1. the colour line written literally inside vertex(): ALBEDO is a fragment output
	try_shader("ALBEDO written in vertex()", "shader_type spatial;\nvoid vertex() {\n\tALBEDO = vec3(1.0);\n}\n")
	# 2. the legal way to compute at the corners: a varying written in vertex(), read in fragment()
	try_shader("varying computed in vertex()", "shader_type spatial;\nvarying vec3 c;\nvoid vertex() {\n\tc = vec3(step(0.5, fract(UV.x * 8.0)));\n}\nvoid fragment() {\n\tALBEDO = c;\n}\n")
	# 3. the corner arithmetic of B52: stripe_count 8.0 (signal.gdshader line 6); corner UV.x is 0 or 1
	for u in [0.0, 1.0]:
		print("CORNER UV.x=", u, " fract(UV.x * 8) = ", fposmod(u * 8.0, 1.0), " step(0.5, that) = ", 1.0 if fposmod(u * 8.0, 1.0) >= 0.5 else 0.0)
	# 4. QuadMesh(3, 2), the pad quad of render-material-evidence.gd:29: corner UVs from the mesh arrays
	var mesh := QuadMesh.new()
	mesh.size = Vector2(3, 2)
	var arrays := mesh.get_mesh_arrays()
	print("QUAD VERTICES ", arrays[Mesh.ARRAY_VERTEX].size(), " UVs ", arrays[Mesh.ARRAY_TEX_UV])
	quit()

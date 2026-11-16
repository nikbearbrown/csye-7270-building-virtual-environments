extends SceneTree
# facts1: what Godot 4.7.2 itself says about the classes the water film leans on (no GPU needed). Run: godot --headless --script facts1_classdb.gd
func _initialize() -> void:
	print("ENGINE ", Engine.get_version_info()["string"])
	var vs: Array = []
	for c in ClassDB.get_inheriters_from_class("VisualShaderNode"):
		vs.append(c)
	vs.sort()
	var noisy: Array = []
	for c in vs:
		var s := String(c).to_lower()
		if s.contains("noise") or s.contains("voronoi") or s.contains("random") or s.contains("cellular") or s.contains("worley") or s.contains("fresnel"):
			noisy.append(c)
	print("VISUALSHADER NODES TOTAL ", vs.size(), "  noise/random/voronoi/fresnel-ish: ", noisy)
	print("class_exists VisualShaderNodeVoronoi*: ", ClassDB.class_exists("VisualShaderNodeVoronoiNoise"), ClassDB.class_exists("VisualShaderNodeVoronoi"))
	print("class_exists NoiseTexture2D/3D: ", ClassDB.class_exists("NoiseTexture2D"), ClassDB.class_exists("NoiseTexture3D"))
	for k in ["FastNoiseLite", "NoiseTexture2D", "PlaneMesh", "MeshInstance3D"]:
		var props: Array = []
		for p in ClassDB.class_get_property_list(k, true):
			if int(p["usage"]) & PROPERTY_USAGE_EDITOR:
				props.append(String(p["name"]))
		print("PROPS ", k, ": ", props)
	for e in ["NoiseType", "CellularReturnType", "CellularDistanceFunction"]:
		var consts: Array = []
		for c in ClassDB.class_get_enum_constants("FastNoiseLite", e):
			consts.append("%s=%d" % [c, ClassDB.class_get_integer_constant("FastNoiseLite", c)])
		print("ENUM FastNoiseLite.", e, " ", consts)
	var pm := PlaneMesh.new()
	print("PlaneMesh defaults: size=", pm.size, " subdivide_width=", pm.subdivide_width, " subdivide_depth=", pm.subdivide_depth, " orientation=", pm.orientation)
	for sw in [0, 1, 3, 31, 63, 127]:
		pm.subdivide_width = sw
		pm.subdivide_depth = sw
		var arr := pm.get_mesh_arrays()
		var verts: PackedVector3Array = arr[Mesh.ARRAY_VERTEX]
		var idx: PackedInt32Array = arr[Mesh.ARRAY_INDEX]
		print("PlaneMesh cuts %d x %d -> %d vertices, %d triangles" % [sw, sw, verts.size(), idx.size() / 3])
	var vn := pm.get_mesh_arrays()[Mesh.ARRAY_NORMAL] as PackedVector3Array
	print("PlaneMesh normal[0] = ", vn[0], "  (flat in the xz plane, +y up)")
	var n2 := NoiseTexture2D.new()
	print("NoiseTexture2D defaults: ", n2.width, "x", n2.height, " seamless=", n2.seamless, " as_normal_map=", n2.as_normal_map, " bump_strength=", n2.bump_strength, " generate_mipmaps=", n2.generate_mipmaps, " normalize=", n2.normalize)
	var fn := FastNoiseLite.new()
	print("FastNoiseLite defaults: type=", fn.noise_type, " frequency=", fn.frequency, " seed=", fn.seed, " fractal_type=", fn.fractal_type, " octaves=", fn.fractal_octaves)
	quit()

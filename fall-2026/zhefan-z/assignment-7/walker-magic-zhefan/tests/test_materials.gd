extends SceneTree
## Assignment 5 headless check of the material audit in MATERIALS.md (CHANGE-BRIEF.md sections 3 and 4, and the
## revision 2026-10-27): both scenes' materials, lights and environments, every sampler's hints read from the
## shader source, every material's uniform values and textures, each texture's import settings and imported
## format, both shaders' uniform lists, and the curl check on the bound normal map.
## From fall-2026/zhefan-z/assignment-5/:
##   ./scripts/run-test.sh test_materials.gd 60
## Prints one JSON line per check and "WALKER TESTS: N checks / F failures"; exit code 1 on any failure.
## Lines with "observation" instead of "status" are printed, not asserted.
## Headless uses a dummy renderer: nothing here looks at a pixel on screen. Image.load_from_file prints an engine
## WARNING ("will not work on export") for each normal map; it is expected here.

const NormalMapCheck := preload("res://tests/normal_map_check.gd")

const ROCK_SHADER := "res://shaders/rock_frost.gdshader"
const HINT_SHADER := "res://shaders/hint_experiment.gdshader"
const DIFF := "res://assets/textures/rock_01/rock_01_diff_1k.png"
const NOR_GL := "res://assets/textures/rock_01/rock_01_nor_gl_1k.png"
const NOR_DX := "res://assets/textures/rock_01/rock_01_nor_dx_1k.png"
const ROUGH := "res://assets/textures/rock_01/rock_01_rough_1k.png"
const GREYS := "res://assets/textures/hint/greys_3x1.png"
const MAT_DRY := "res://assets/materials/mat_rock_dry.tres"
const MAT_FROSTED := "res://assets/materials/mat_rock_frosted.tres"
const MAT_SRC := "res://assets/materials/mat_hint_source_color.tres"
const MAT_RAW := "res://assets/materials/mat_hint_raw_data.tres"
const COMPARE_SCENE := "res://showcase3d/material_compare.tscn"
const HINT_SCENE := "res://showcase3d/hint_experiment.tscn"
const PROP_ROOM := "res://showcase3d/prop_room.tscn"

## MATERIALS.md "Materials": every uniform each material sets, and every texture it binds.
const MATERIALS := {
	MAT_DRY: {"shader": ROCK_SHADER,
		"values": {"base_tint": Color(1, 1, 1, 1), "normal_scale": 1.0, "roughness_scale": 1.0,
			"frost_color": Color(0.85, 0.92, 1, 1), "frost_amount": 0.0},
		"textures": {"texture_albedo": DIFF, "texture_normal": NOR_GL, "texture_roughness": ROUGH}},
	MAT_FROSTED: {"shader": ROCK_SHADER,
		"values": {"base_tint": Color(0.92, 0.95, 1, 1), "normal_scale": 1.0, "roughness_scale": 1.0,
			"frost_color": Color(0.85, 0.92, 1, 1), "frost_amount": 0.65},
		"textures": {"texture_albedo": DIFF, "texture_normal": NOR_GL, "texture_roughness": ROUGH}},
	MAT_SRC: {"shader": HINT_SHADER, "values": {"use_source_color": true},
		"textures": {"source_color_tex": GREYS, "raw_data_tex": GREYS}},
	MAT_RAW: {"shader": HINT_SHADER, "values": {"use_source_color": false},
		"textures": {"source_color_tex": GREYS, "raw_data_tex": GREYS}},
}

## MATERIALS.md "Samplers": hints in the order they are written in the source.
const SAMPLERS := {
	ROCK_SHADER: {"texture_albedo": ["source_color", "filter_linear_mipmap"],
		"texture_normal": ["hint_normal", "filter_linear_mipmap"],
		"texture_roughness": ["hint_default_white", "filter_linear_mipmap"]},
	HINT_SHADER: {"source_color_tex": ["source_color", "filter_nearest"], "raw_data_tex": ["filter_nearest"]},
}

## Uniform name -> [type, range hint as floats or []], as get_shader_uniform_list() reports it.
const UNIFORMS := {
	ROCK_SHADER: {"base_tint": [TYPE_COLOR, []], "normal_scale": [TYPE_FLOAT, [0.0, 2.0, 0.05]],
		"roughness_scale": [TYPE_FLOAT, [0.0, 2.0, 0.05]], "frost_color": [TYPE_COLOR, []],
		"frost_amount": [TYPE_FLOAT, [0.0, 1.0, 0.01]], "texture_albedo": [TYPE_OBJECT, []],
		"texture_normal": [TYPE_OBJECT, []], "texture_roughness": [TYPE_OBJECT, []]},
	HINT_SHADER: {"source_color_tex": [TYPE_OBJECT, []], "raw_data_tex": [TYPE_OBJECT, []],
		"use_source_color": [TYPE_BOOL, []]},
}

## MATERIALS.md "Textures": [params] of each .import file, and the imported format on this machine (s3tc_bptc).
const IMPORTS := {
	DIFF: {"compress/mode": 2, "compress/normal_map": 2, "mipmaps/generate": true, "detect_3d/compress_to": 0,
		"format": Image.FORMAT_DXT1},
	NOR_GL: {"compress/mode": 2, "compress/normal_map": 1, "mipmaps/generate": true, "detect_3d/compress_to": 0,
		"format": Image.FORMAT_RGTC_RG},
	ROUGH: {"compress/mode": 2, "compress/normal_map": 2, "mipmaps/generate": true, "detect_3d/compress_to": 0,
		"format": Image.FORMAT_DXT1},
	NOR_DX: {"compress/mode": 2, "compress/normal_map": 1, "mipmaps/generate": true, "detect_3d/compress_to": 0,
		"format": Image.FORMAT_RGTC_RG},
	GREYS: {"compress/mode": 0, "compress/normal_map": 2, "mipmaps/generate": false, "detect_3d/compress_to": 0,
		"format": Image.FORMAT_RGB8},
}

## Thresholds from logs/calibrate_normal_check_60fps.log (lines 7-8, 13-14): 0.1444 in the file's own
## convention, 1.8556 in the other one.
const CURL_OWN_MAX := 0.5
const CURL_OTHER_MIN := 1.5

var results: Array[Dictionary] = []
var failures := 0


func _initialize() -> void:
	call_deferred("run")


func check(id: String, passed: bool, observed: Dictionary) -> void:
	results.append({"id": id, "status": "PASS" if passed else "FAIL", "observed": observed})
	if not passed:
		failures += 1
	print(JSON.stringify(results.back()))


func observe(id: String, observed: Dictionary) -> void:
	print(JSON.stringify({"id": id, "observation": observed}))


func same(a: Variant, b: Variant) -> bool:
	if typeof(a) != typeof(b):
		return false
	if a is float:
		return is_equal_approx(a, b)
	if a is Color:
		return (a as Color).is_equal_approx(b)
	return a == b


func path_of(r: Resource) -> String:
	return r.resource_path if r != null else ""


## Sampler name -> hints as written, from `uniform sampler2D name : hint, hint;` lines.
func sampler_hints(src: String) -> Dictionary:
	var out := {}
	var re := RegEx.create_from_string("uniform\\s+sampler2D\\s+(\\w+)\\s*(?::\\s*([^;=]+))?;")
	for m in re.search_all(src):
		var hints: Array[String] = []
		for h in m.get_string(2).split(",", false):
			hints.append(h.strip_edges())
		out[m.get_string(1)] = hints
	return out


func env_row(env: Environment) -> Dictionary:
	return {"background_mode": env.background_mode, "background_color": env.background_color.to_html(),
		"ambient_light_source": env.ambient_light_source, "tonemap_mode": env.tonemap_mode,
		"tonemap_exposure": env.tonemap_exposure, "glow": env.glow_enabled, "fog": env.fog_enabled,
		"volumetric_fog": env.volumetric_fog_enabled, "ssao": env.ssao_enabled, "ssil": env.ssil_enabled,
		"ssr": env.ssr_enabled, "sdfgi": env.sdfgi_enabled, "adjustments": env.adjustment_enabled}


func lights_of(scene: Node) -> Array[Dictionary]:
	var out: Array[Dictionary] = []
	for l: Light3D in scene.find_children("*", "Light3D", true, false):
		out.append({"name": l.name, "class": l.get_class(), "energy": l.light_energy, "shadow": l.shadow_enabled,
			"color": l.light_color.to_html(), "transform": l.transform})
	return out


func run() -> void:
	await process_frame   # get_shader_uniform_list() needs the main loop running

	# --- Materials: shader, every uniform value, every texture. ---
	var mats := {}
	for p: String in MATERIALS:
		mats[p] = load(p) as ShaderMaterial
	check("rock-materials-share-shader", mats[MAT_DRY] != null and mats[MAT_FROSTED] != null
		and path_of(mats[MAT_DRY].shader) == ROCK_SHADER and path_of(mats[MAT_FROSTED].shader) == ROCK_SHADER,
		{"dry": path_of(mats[MAT_DRY].shader), "frosted": path_of(mats[MAT_FROSTED].shader)})
	check("hint-materials-share-shader", path_of(mats[MAT_SRC].shader) == HINT_SHADER
		and path_of(mats[MAT_RAW].shader) == HINT_SHADER,
		{"source_color": path_of(mats[MAT_SRC].shader), "raw_data": path_of(mats[MAT_RAW].shader)})

	for p: String in MATERIALS:
		var want: Dictionary = MATERIALS[p]
		var mat: ShaderMaterial = mats[p]
		var values := {}
		var textures := {}
		var ok: bool = path_of(mat.shader) == want.shader
		# Every uniform the shader declares must be set in the material (unset reads back as null).
		for u: Dictionary in mat.shader.get_shader_uniform_list():
			var v: Variant = mat.get_shader_parameter(u.name)
			if v is Texture2D:
				textures[u.name] = path_of(v)
				ok = ok and want.textures.get(u.name, "<none>") == textures[u.name]
			else:
				values[u.name] = v
				ok = ok and want.values.has(u.name) and same(v, want.values[u.name])
		ok = ok and values.size() == want.values.size() and textures.size() == want.textures.size()
		check("material-values-and-textures:" + p.get_file(), ok, {"values": values, "textures": textures})

	# --- Samplers: hints as written in the source. ---
	for shader_path: String in SAMPLERS:
		var found := sampler_hints(FileAccess.get_file_as_string(shader_path))
		check("sampler-set:" + shader_path.get_file(), found.keys() == SAMPLERS[shader_path].keys(),
			{"samplers_in_source": found.keys()})
		for s: String in SAMPLERS[shader_path]:
			var bound := {}
			for p: String in MATERIALS:
				if MATERIALS[p].shader == shader_path:
					bound[p.get_file()] = path_of(mats[p].get_shader_parameter(s))
			check("sampler-hints:%s:%s" % [shader_path.get_file(), s],
				found.get(s, []) == SAMPLERS[shader_path][s], {"hints": found.get(s, null), "bound": bound})

	# --- Uniform lists, as the engine parses each shader. ---
	for shader_path: String in UNIFORMS:
		var listed := {}
		var ok := true
		for u: Dictionary in (load(shader_path) as Shader).get_shader_uniform_list():
			listed[u.name] = {"type": type_string(u.type), "hint": u.hint, "hint_string": u.hint_string}
			var want: Array = UNIFORMS[shader_path].get(u.name, [])
			ok = ok and want.size() == 2 and u.type == want[0]
			if ok and not want[1].is_empty():
				var parts: PackedStringArray = String(u.hint_string).split(",")
				ok = u.hint == PROPERTY_HINT_RANGE and parts.size() >= 3
				for i in 3:
					ok = ok and is_equal_approx(parts[i].to_float(), want[1][i])
			if ok and u.type == TYPE_OBJECT:
				ok = u.hint_string == "Texture2D"
		check("uniform-list:" + shader_path.get_file(), ok and listed.size() == UNIFORMS[shader_path].size(),
			{"uniforms": listed})

	# --- Textures: import settings from the .import file, and the imported format. ---
	for tex_path: String in IMPORTS:
		var want: Dictionary = IMPORTS[tex_path]
		var cfg := ConfigFile.new()
		var err := cfg.load(tex_path + ".import")
		var params := {}
		var ok: bool = err == OK and cfg.get_value("remap", "importer", "") == "texture"
		for key: String in ["compress/mode", "compress/normal_map", "mipmaps/generate", "detect_3d/compress_to"]:
			params[key] = cfg.get_value("params", key, null)
			ok = ok and same(params[key], want[key])
		check("import-settings:" + tex_path.get_file(), ok, {"load": error_string(err), "params": params})

		var img := (load(tex_path) as Texture2D).get_image()
		var row := {"format": img.get_format(), "size": [img.get_width(), img.get_height()],
			"mipmaps": img.has_mipmaps()}
		ok = img.get_format() == want.format and img.has_mipmaps() == want["mipmaps/generate"]
		if tex_path == GREYS:
			var texels := []
			for x in img.get_width():
				texels.append(img.get_pixel(x, 0).to_html(false))
			row["texels"] = texels
			ok = ok and texels == ["404040", "808080", "c0c0c0"]
		check("imported-format:" + tex_path.get_file(), ok, row)

	# Roughness precision (MATERIALS.md finding 1): the imported texture against its 16-bit source, which
	# Image.load_from_file reads as 8-bit. The shader reads .r; DXT1 stores red with 5 endpoint bits, green with 6.
	var rough_src := Image.load_from_file(ROUGH)
	var rough_imp := (load(ROUGH) as Texture2D).get_image().duplicate() as Image
	rough_imp.decompress()
	var err_r := []
	var err_g := []
	for v in range(0, rough_src.get_height(), 2):
		for u in range(0, rough_src.get_width(), 2):
			var s := rough_src.get_pixel(u, v).r
			var c := rough_imp.get_pixel(u, v)
			err_r.append(absf(c.r - s) * 255.0)
			err_g.append(absf(c.g - s) * 255.0)
	observe("roughness-import-error-in-8bit-steps", {"source_format": rough_src.get_format(),
		"imported_format": (load(ROUGH) as Texture2D).get_image().get_format(),
		"red_mean": snappedf(err_r.reduce(func(a, b): return a + b, 0.0) / err_r.size(), 0.01), "red_max": err_r.max(),
		"green_mean": snappedf(err_g.reduce(func(a, b): return a + b, 0.0) / err_g.size(), 0.01),
		"green_max": err_g.max(), "samples": err_r.size()})

	# --- Normal maps: curl_ratio from the source files; asserted for the bound map only. ---
	for nor_path: String in [NOR_GL, NOR_DX]:
		var img := Image.load_from_file(nor_path)
		var gl := NormalMapCheck.curl_ratio(img, false, 4)
		var dx := NormalMapCheck.curl_ratio(img, true, 4)
		var row := {"file": nor_path.get_file(), "opengl": snappedf(gl, 0.0001), "directx": snappedf(dx, 0.0001),
			"bound_to": MATERIALS.keys().filter(func(p: String) -> bool:
				return nor_path in MATERIALS[p].textures.values()).map(func(p: String) -> String: return p.get_file())}
		if nor_path == NOR_GL:
			check("normal-map-convention:" + nor_path.get_file(), gl < CURL_OWN_MAX and dx > CURL_OTHER_MIN, row)
		else:
			observe("normal-map-convention:" + nor_path.get_file(), row)

	# --- material_compare.tscn: overrides, mesh, lights and environment. ---
	var compare: Node = (load(COMPARE_SCENE) as PackedScene).instantiate()
	for rock: Array in [["RockDry", MAT_DRY], ["RockFrosted", MAT_FROSTED]]:
		var mi := compare.get_node("%s/Rock" % rock[0]) as MeshInstance3D
		var mesh := mi.mesh
		var row := {"surface_0": mesh.surface_get_name(0), "override_0": path_of(mi.get_surface_override_material(0)),
			"surface_1": mesh.surface_get_name(1), "override_1": path_of(mi.get_surface_override_material(1)),
			"active_1": mi.get_active_material(1).get_class(),
			"tangents_0": bool(mesh.surface_get_format(0) & Mesh.ARRAY_FORMAT_TANGENT)}
		check("compare-scene-rock:" + rock[0], mesh.get_surface_count() == 2 and row.surface_0 == "Rock_Main"
			and row.override_0 == rock[1] and row.surface_1 == "Rock_Top" and row.override_1 == ""
			and mi.get_active_material(1) is StandardMaterial3D and row.tangents_0, row)

	# The lighting is a copy of the prop room's (CHANGE-BRIEF section 4); compared against that scene, and its
	# defaults pinned (tonemap Linear at exposure 1.0, no glow, fog, SSAO, SSIL, SSR or SDFGI).
	var prop: Node = (load(PROP_ROOM) as PackedScene).instantiate()
	var env_c := env_row((compare.get_node("WorldEnvironment") as WorldEnvironment).environment)
	var env_p := env_row((prop.get_node("WorldEnvironment") as WorldEnvironment).environment)
	var lights_c := lights_of(compare)
	var lights_p := lights_of(prop)
	check("compare-scene-environment", env_c == env_p and env_c.background_mode == Environment.BG_COLOR
		and env_c.background_color == "0f1119ff" and env_c.ambient_light_source == Environment.AMBIENT_SOURCE_BG
		and env_c.tonemap_mode == Environment.TONE_MAPPER_LINEAR and env_c.tonemap_exposure == 1.0
		and not (env_c.glow or env_c.fog or env_c.volumetric_fog or env_c.ssao or env_c.ssil or env_c.ssr
		or env_c.sdfgi or env_c.adjustments), {"material_compare": env_c, "same_as_prop_room": env_c == env_p})
	check("compare-scene-lights", lights_c.size() == 1 and lights_c == lights_p
		and lights_c[0].class == "DirectionalLight3D" and lights_c[0].energy == 1.0 and lights_c[0].shadow,
		{"material_compare": lights_c, "same_as_prop_room": lights_c == lights_p})
	prop.free()
	compare.free()

	# --- hint_experiment.tscn: quads, environment set explicitly, no light. ---
	var hint: Node = (load(HINT_SCENE) as PackedScene).instantiate()
	var quads := {}
	for q: String in ["QuadSourceColor", "QuadRawData"]:
		var mi := hint.get_node(q) as MeshInstance3D
		quads[q] = {"x": mi.position.x, "override_0": path_of(mi.get_surface_override_material(0)),
			"mesh": mi.mesh.get_class()}
	check("hint-scene-quads", quads.QuadSourceColor.override_0 == MAT_SRC and quads.QuadRawData.override_0 == MAT_RAW
		and quads.QuadSourceColor.x < 0.0 and quads.QuadRawData.x > 0.0, {"quads": quads})
	var env_h := env_row((hint.get_node("WorldEnvironment") as WorldEnvironment).environment)
	var lights_h := lights_of(hint)
	check("hint-scene-environment", env_h.tonemap_mode == Environment.TONE_MAPPER_LINEAR
		and env_h.tonemap_exposure == 1.0 and not (env_h.glow or env_h.fog or env_h.adjustments)
		and lights_h.is_empty(), {"environment": env_h, "lights": lights_h})
	hint.free()

	print("WALKER TESTS: %d checks / %d failures" % [results.size(), failures])
	quit(1 if failures else 0)

extends SceneTree
## Headless audit of the materials in CHANGE-BRIEF.md (revision 1, with
## revision 2 for the circle's albedo_tint). It pins the tables in
## godot/MATERIALS.md: each shader's uniform list and sampler hints, each
## material's values and textures, each texture's import settings, the surface
## or quad each material is on, and the lights and environment of both scenes.
## For each normal map it prints normal_map_check.gd's curl ratio under both
## green conventions. Prints one PASS or FAIL line per check and exits 1 if any
## fails. Run from assignment-5/:
##   scripts/run-test.sh godot test_materials.gd 60
##
## What it cannot show: anything drawn. The headless renderer is a dummy, so the
## hint experiment's displayed values (brief section 4) and how the stone looks
## under the Sun (section 5) are human checks.

const NormalMapCheck := preload("res://tests/normal_map_check.gd")

const STONE_SHADER := "res://shaders/weathered_stone.gdshader"
const HINT_SHADER := "res://shaders/hint_experiment.gdshader"
const DIFF := "res://assets/textures/rock_01/rock_01_diff_1k.png"
const NOR_GL := "res://assets/textures/rock_01/rock_01_nor_gl_1k.png"
const NOR_DX := "res://assets/textures/rock_01/rock_01_nor_dx_1k.png"
const ROUGH := "res://assets/textures/rock_01/rock_01_rough_1k.png"
const STRIP := "res://assets/hint_experiment/grey_strip_3x1.png"

## Each shader's uniform list as get_shader_uniform_list(true) reports it, in
## order. A group is [name]; a sampler is [name, TYPE_OBJECT]; a range is
## [name, TYPE_FLOAT, min, max, step].
const UNIFORMS := {
	STONE_SHADER: [
		["albedo_tex", TYPE_OBJECT], ["normal_tex", TYPE_OBJECT], ["roughness_tex", TYPE_OBJECT],
		["surface"],
		["albedo_tint", TYPE_COLOR], ["uv_scale", TYPE_FLOAT, 0.25, 4.0, 0.05],
		["relief"],
		["normal_strength", TYPE_FLOAT, 0.0, 2.0, 0.05], ["roughness_offset", TYPE_FLOAT, -0.5, 0.5, 0.01],
	],
	HINT_SHADER: [
		["source_color_tex", TYPE_OBJECT], ["plain_tex", TYPE_OBJECT], ["use_source_color", TYPE_BOOL],
	],
}

## Each sampler's hints, as written after the colon in the source.
const SAMPLER_HINTS := {
	STONE_SHADER: {
		"albedo_tex": ["source_color", "filter_linear_mipmap", "repeat_enable"],
		"normal_tex": ["hint_normal", "filter_linear_mipmap", "repeat_enable"],
		"roughness_tex": ["filter_linear_mipmap", "repeat_enable"],
	},
	HINT_SHADER: {
		"source_color_tex": ["source_color", "filter_nearest"],
		"plain_tex": ["filter_nearest"],
	},
}

## Every value each material sets. A Color is its 8-bit hex; a texture is its path.
const MATERIALS := {
	"res://materials/waystone_stone.tres": [STONE_SHADER, {
		"albedo_tex": DIFF, "normal_tex": NOR_GL, "roughness_tex": ROUGH,
		"albedo_tint": "FFFFFF", "uv_scale": 1.0, "normal_strength": 1.0, "roughness_offset": 0.0,
	}],
	"res://materials/circle_darkstone.tres": [STONE_SHADER, {
		"albedo_tex": DIFF, "normal_tex": NOR_GL, "roughness_tex": ROUGH,
		"albedo_tint": "A4A7B4", "uv_scale": 1.0, "normal_strength": 0.35, "roughness_offset": -0.25,
	}],
	"res://materials/hint_source_color.tres": [HINT_SHADER, {
		"source_color_tex": STRIP, "plain_tex": STRIP, "use_source_color": true,
	}],
	"res://materials/hint_plain.tres": [HINT_SHADER, {
		"source_color_tex": STRIP, "plain_tex": STRIP, "use_source_color": false,
	}],
}

## Every [params] value the brief sets for each texture (sections 4 and 5).
## The integers are the importer's enums (Godot 4.7.2,
## editor/import/resource_importer_texture.cpp): compress/mode 0 Lossless,
## 2 VRAM Compressed; compress/normal_map 1 Enable, 2 Disabled;
## detect_3d/compress_to 0 Disabled; roughness/mode 1 Disabled.
const IMPORTS := {
	DIFF: {"compress/mode": 2, "compress/normal_map": 2, "mipmaps/generate": true,
		"detect_3d/compress_to": 0},
	NOR_GL: {"compress/mode": 2, "compress/normal_map": 1, "mipmaps/generate": true,
		"detect_3d/compress_to": 0, "process/normal_map_invert_y": false},
	ROUGH: {"compress/mode": 2, "compress/normal_map": 2, "mipmaps/generate": true,
		"detect_3d/compress_to": 0, "roughness/mode": 1},
	NOR_DX: {"compress/mode": 0, "compress/normal_map": 2, "mipmaps/generate": false,
		"detect_3d/compress_to": 0},
	STRIP: {"compress/mode": 0, "compress/normal_map": 2, "mipmaps/generate": false,
		"detect_3d/compress_to": 0},
}

## [mesh node, surface, imported material name, override] in props_room.tscn.
## An override of "" means the surface keeps its imported material.
const SURFACES := [
	["Waystone/Waystone", 0, "Stone", "res://materials/waystone_stone.tres"],
	["Waystone/Waystone", 1, "Moss", ""],
	["Waystone/Waystone", 2, "Rune", ""],
	["TeleportCircle/TeleportCircle", 0, "Gold", ""],
	["TeleportCircle/TeleportCircle", 1, "DarkStone", "res://materials/circle_darkstone.tres"],
	["TeleportCircle/TeleportCircle", 2, "PaleGold", ""],
]

var _failures := 0


func _init() -> void:
	print("== Shaders: uniform list and sampler hints")
	for path: String in UNIFORMS:
		_check_shader(path)
	print("\n== Materials: shader, values, textures")
	for path: String in MATERIALS:
		_check_material(path)
	var stone_a := load("res://materials/waystone_stone.tres") as ShaderMaterial
	var stone_b := load("res://materials/circle_darkstone.tres") as ShaderMaterial
	_check("both stone materials use the same Shader resource",
		stone_a.shader == stone_b.shader and stone_a.shader.resource_path == STONE_SHADER,
		"%s, %s" % [stone_a.shader.resource_path, stone_b.shader.resource_path])
	print("\n== Import settings, from the .import files")
	for path: String in IMPORTS:
		_check_import(path)
	print("\n== Where each material is")
	_check_props_room()
	_check_hint_scene()
	print("\n== Normal maps: curl ratio of the source file")
	_check_normal_maps()
	print("\nall checks passed" if _failures == 0 else "\n%d check(s) FAILED" % _failures)
	quit(1 if _failures > 0 else 0)


func _check_shader(path: String) -> void:
	var shader := load(path) as Shader
	_check("%s loads as a Shader" % path.get_file(), shader != null)
	if shader == null:
		return
	_check("%s is spatial" % path.get_file(), shader.get_mode() == Shader.MODE_SPATIAL)
	# The uniform list is empty if the shader failed to parse.
	var got := shader.get_shader_uniform_list(true)
	var want: Array = UNIFORMS[path]
	_check("%s reports %d entries" % [path.get_file(), want.size()], got.size() == want.size(),
		"%d" % got.size())
	for i in mini(got.size(), want.size()):
		var u: Dictionary = got[i]
		var w: Array = want[i]
		if w.size() == 1:
			_check("%s entry %d is the group '%s'" % [path.get_file(), i, w[0]],
				u.type == TYPE_NIL and u.name == w[0], "%s %s" % [type_string(u.type), u.name])
			continue
		var ok: bool = u.name == w[0] and u.type == w[1]
		var what := "%s entry %d is %s: %s" % [path.get_file(), i, w[0], type_string(w[1])]
		if w[1] == TYPE_OBJECT:
			ok = ok and u.hint == PROPERTY_HINT_RESOURCE_TYPE and u.hint_string == "Texture2D"
			what += " (Texture2D)"
		elif w.size() == 5:
			var r: PackedStringArray = (u.hint_string as String).split(",")
			ok = ok and u.hint == PROPERTY_HINT_RANGE and r.size() >= 3
			for k in 3:
				ok = ok and r.size() >= 3 and is_equal_approx(r[k].to_float(), w[2 + k])
			what += " range %s, %s, %s" % [w[2], w[3], w[4]]
		_check(what, ok, "%s %s '%s'" % [u.name, type_string(u.type), u.hint_string])

	# The engine reports no sampler hints, so read them from the source text.
	var hints := _sampler_hints(shader.code)
	var want_hints: Dictionary = SAMPLER_HINTS[path]
	_check("%s declares exactly the samplers %s" % [path.get_file(), want_hints.keys()],
		hints.keys() == want_hints.keys(), "%s" % [hints.keys()])
	for s: String in want_hints:
		_check("%s: %s hints are %s" % [path.get_file(), s, ", ".join(want_hints[s])],
			hints.get(s, []) == want_hints[s], ", ".join(hints.get(s, [])))


## {sampler name: [hints as written]} for every sampler2D declared in `code`.
func _sampler_hints(code: String) -> Dictionary:
	var out := {}
	var re := RegEx.create_from_string("(?m)^\\s*uniform\\s+sampler2D\\s+(\\w+)\\s*(?::\\s*([^;=]*))?;")
	for m in re.search_all(code):
		var list: Array = []
		for h in m.get_string(2).split(",", false):
			list.append(h.strip_edges())
		out[m.get_string(1)] = list
	return out


func _check_material(path: String) -> void:
	var mat := load(path) as ShaderMaterial
	_check("%s loads as a ShaderMaterial" % path.get_file(), mat != null)
	if mat == null:
		return
	var want_shader: String = MATERIALS[path][0]
	_check("%s uses %s" % [path.get_file(), want_shader.get_file()],
		mat.shader != null and mat.shader.resource_path == want_shader,
		mat.shader.resource_path if mat.shader else "no shader")
	var values: Dictionary = MATERIALS[path][1]
	for name: String in values:
		var got: Variant = mat.get_shader_parameter(name)
		var want: Variant = values[name]
		var ok := false
		var shown := str(got)
		if got is Texture2D:
			shown = (got as Texture2D).resource_path
			ok = shown == want
		elif got is Color:
			shown = (got as Color).to_html(false).to_upper()
			ok = shown == want
		elif got is float and want is float:
			ok = is_equal_approx(got, want)
		elif got is bool:
			ok = got == want
		_check("%s: %s = %s" % [path.get_file(), name, want], ok, shown)
	# Nothing else is set: every value the file stores is one listed above.
	var stored: Array = []
	for p: Dictionary in mat.get_property_list():
		var n: String = p.name
		if n.begins_with("shader_parameter/") and mat.get(n) != null:
			stored.append(n.trim_prefix("shader_parameter/"))
	stored.sort()
	var listed: Array = values.keys()
	listed.sort()
	_check("%s sets exactly %d uniforms" % [path.get_file(), listed.size()], stored == listed,
		", ".join(stored))


func _check_import(path: String) -> void:
	var cf := ConfigFile.new()
	var err := cf.load(path + ".import")
	_check("%s.import reads" % path.get_file(), err == OK, error_string(err))
	if err != OK:
		return
	_check("%s imports as a texture" % path.get_file(),
		cf.get_value("remap", "importer", "") == "texture", str(cf.get_value("remap", "importer", "")))
	var want: Dictionary = IMPORTS[path]
	for key: String in want:
		var got: Variant = cf.get_value("params", key, null)
		_check("%s: %s = %s" % [path.get_file(), key, want[key]], got == want[key], str(got))
	# What the import produced on this machine: printed, not asserted, because
	# the VRAM format depends on the platform.
	var tex := load(path) as Texture2D
	var image := tex.get_image() if tex else null
	if image:
		print("INFO  %s imported: %dx%d, format %d, %d mipmap level(s)" % [path.get_file(),
			image.get_width(), image.get_height(), image.get_format(), image.get_mipmap_count()])


func _check_props_room() -> void:
	var scene: Node = (load("res://scenes/props_room.tscn") as PackedScene).instantiate()
	for s: Array in SURFACES:
		var mi := scene.get_node_or_null(s[0]) as MeshInstance3D
		if mi == null:
			_check("props_room: %s is a MeshInstance3D" % s[0], false)
			continue
		var imported := mi.mesh.surface_get_material(s[1])
		_check("props_room: %s surface %d is imported as %s" % [s[0], s[1], s[2]],
			imported is BaseMaterial3D and imported.resource_name == s[2],
			imported.resource_name if imported else "none")
		var override := mi.get_surface_override_material(s[1])
		var got := override.resource_path if override else ""
		var want: String = s[3] if s[3] != "" else "no override"
		_check("props_room: %s surface %d: %s" % [s[0], s[1], want], got == s[3],
			got if got != "" else "no override")
	# No other mesh in the room carries the textured shader.
	var users: Array = []
	for mi: MeshInstance3D in _of_type(scene, "MeshInstance3D"):
		var mats: Array = [mi.material_override]
		for i in mi.get_surface_override_material_count():
			mats.append(mi.get_surface_override_material(i))
		for i in (mi.mesh.get_surface_count() if mi.mesh else 0):
			mats.append(mi.mesh.surface_get_material(i))
		for m in mats:
			if m is ShaderMaterial and m.shader and m.shader.resource_path == STONE_SHADER:
				users.append(str(scene.get_path_to(mi)))
	_check("props_room: only the waystone and the circle use the textured shader",
		users == ["Waystone/Waystone", "TeleportCircle/TeleportCircle"], ", ".join(users))

	var lights := _of_type(scene, "Light3D")
	_check("props_room: one light, the DirectionalLight3D Sun",
		lights.size() == 1 and lights[0] is DirectionalLight3D and lights[0].name == "Sun",
		", ".join(lights.map(func(l): return "%s %s" % [l.get_class(), l.name])))
	var sun := scene.get_node("Sun") as DirectionalLight3D
	_check("props_room: Sun energy 1.1", is_equal_approx(sun.light_energy, 1.1), "%s" % sun.light_energy)
	_check("props_room: Sun casts shadows", sun.shadow_enabled)
	_check("props_room: Sun colour white", sun.light_color == Color.WHITE, sun.light_color.to_html(false))
	var env := (scene.get_node("WorldEnvironment") as WorldEnvironment).environment
	_check("props_room: background Custom Color #9DB8CF", env.background_mode == Environment.BG_COLOR
		and env.background_color.to_html(false).to_upper() == "9DB8CF",
		"mode %d, #%s" % [env.background_mode, env.background_color.to_html(false).to_upper()])
	_check("props_room: ambient from Color (1, 0.957, 0.878) at 0.45",
		env.ambient_light_source == Environment.AMBIENT_SOURCE_COLOR
		and env.ambient_light_color.is_equal_approx(Color(1, 0.95686275, 0.8784314))
		and is_equal_approx(env.ambient_light_energy, 0.45),
		"source %d, %s, %s" % [env.ambient_light_source, env.ambient_light_color, env.ambient_light_energy])
	_check_environment("props_room", env, Environment.TONE_MAPPER_FILMIC)
	scene.free()


func _check_hint_scene() -> void:
	var scene: Node = (load("res://scenes/hint_experiment.tscn") as PackedScene).instantiate()
	for q: Array in [["QuadA", "res://materials/hint_source_color.tres"],
			["QuadB", "res://materials/hint_plain.tres"]]:
		var mi := scene.get_node_or_null(q[0]) as MeshInstance3D
		var m := mi.material_override if mi else null
		_check("hint_experiment: %s has material_override %s" % [q[0], (q[1] as String).get_file()],
			m != null and m.resource_path == q[1], m.resource_path if m else "none")
		_check("hint_experiment: %s is a QuadMesh with no surface material" % q[0],
			mi != null and mi.mesh is QuadMesh and mi.mesh.surface_get_material(0) == null)
	var cam := scene.get_node("Camera") as Camera3D
	_check("hint_experiment: the camera faces the quads (no rotation)",
		cam.transform.basis.is_equal_approx(Basis.IDENTITY))
	_check("hint_experiment: no lights (both quads are unshaded)",
		_of_type(scene, "Light3D").is_empty())
	var env := (scene.get_node("WorldEnvironment") as WorldEnvironment).environment
	_check_environment("hint_experiment", env, Environment.TONE_MAPPER_LINEAR)
	scene.free()


## The settings that change the look in both scenes: the tonemapper, exposure
## and white, and every post effect, which must be off.
func _check_environment(scene: String, env: Environment, tonemap: int) -> void:
	_check("%s: tonemap_mode %d" % [scene, tonemap], env.tonemap_mode == tonemap, "%d" % env.tonemap_mode)
	_check("%s: tonemap_exposure 1.0" % scene, is_equal_approx(env.tonemap_exposure, 1.0),
		"%s" % env.tonemap_exposure)
	print("INFO  %s: tonemap_white %s" % [scene, env.tonemap_white])
	var on: Array = []
	for p in ["glow_enabled", "fog_enabled", "volumetric_fog_enabled", "adjustment_enabled",
			"ssao_enabled", "ssil_enabled", "ssr_enabled", "sdfgi_enabled"]:
		if env.get(p):
			on.append(p)
	_check("%s: glow, fog, adjustments, SSAO, SSIL, SSR and SDFGI off" % scene, on.is_empty(),
		", ".join(on) if on else "all off")


func _check_normal_maps() -> void:
	var ratio := {}
	for path: String in [NOR_GL, NOR_DX]:
		# The source file, decoded as it is on disk, not the compressed import.
		var image := Image.load_from_file(ProjectSettings.globalize_path(path))
		_check("%s decodes" % path.get_file(), image != null)
		if image == null:
			continue
		for directx: bool in [false, true]:
			ratio[[path, directx]] = NormalMapCheck.curl_ratio(image, directx)
			print("RATIO %s, directx = %s: %.4f" % [path.get_file(), directx, ratio[[path, directx]]])
	if ratio.size() == 4:
		_check("the bound map, %s, is OpenGL: lower with directx = false" % NOR_GL.get_file(),
			ratio[[NOR_GL, false]] < ratio[[NOR_GL, true]])
		_check("the calibration map, %s, is DirectX: lower with directx = true" % NOR_DX.get_file(),
			ratio[[NOR_DX, true]] < ratio[[NOR_DX, false]])


func _of_type(node: Node, type: String) -> Array:
	var out: Array = []
	for c in node.get_children():
		if c.is_class(type):
			out.append(c)
		out.append_array(_of_type(c, type))
	return out


func _check(what: String, ok: bool, got := "") -> void:
	print("%s  %s%s" % ["PASS" if ok else "FAIL", what, "  (%s)" % got if got != "" else ""])
	if not ok:
		_failures += 1

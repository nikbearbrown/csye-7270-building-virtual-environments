# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
extends SceneTree  # Extends SceneTree: runs directly with --script, no scene needed; it loads the scenes and resources to check by itself
## Headless test for the A5 material audit: pins the tables in MATERIALS.md.
## Checks: both shaders' sampler hints (read from the source text), the uniform list (get_shader_uniform_list()), the defaults and constants in the shaders (read from the source),
##       which values the four materials store and which textures they bind, each texture's import settings in its .import (ConfigFile), Use External in both .glb files,
##       the materials actually attached to the crates and quads in the scenes, the lights and environment. Normal maps: decode the source files and print curl_ratio under both conventions.
## Run: ./scripts/run-test.sh test_materials.gd 60
## What it cannot prove: what colour the screen shows or where the rust appears (headless mode renders nothing); what format the imported textures have on the GPU (only the CPU-side Image can be read);
##           whether the shaders compile on a real GPU (headless uses a dummy renderer).

# ============================================================
# Constants: the file paths to check, and the expected values copied from the CHANGE-BRIEF 2026-11-01 revisions and the sources
# ============================================================
const NormalMapCheck := preload("res://tests/normal_map_check.gd")  # The curl check given in the assignment (static function curl_ratio)

const CRATE_SHADER := "res://shaders/crate_wear.gdshader"  # The crate wear shader (the textured shader)
const HINT_SHADER := "res://shaders/hint_experiment.gdshader"  # The hint-experiment shader
const CRATE_LONG_MAT := "res://assets/furniture/materials/crate_long_wear.tres"  # The long crate material
const CRATE_CUBE_MAT := "res://assets/furniture/materials/crate_cube_wear.tres"  # The small crate material
const HINT_SRC_MAT := "res://experiments/hint/hint_source_color.tres"  # Hint experiment: use_source_color = true
const HINT_RAW_MAT := "res://experiments/hint/hint_raw.tres"  # Hint experiment: use_source_color = false
const COLOR_TEX := "res://assets/shader/metal041c/Metal041C_1K-PNG_Color.png"  # The rust colour
const DISP_TEX := "res://assets/shader/metal041c/Metal041C_1K-PNG_Displacement.png"  # The wear mask
const ROUGH_TEX := "res://assets/shader/metal041c/Metal041C_1K-PNG_Roughness.png"  # Used only for Step 4
const NORMAL_GL_TEX := "res://assets/shader/metal041c/Metal041C_1K-PNG_NormalGL.png"  # Normals (OpenGL convention)
const NORMAL_DX_TEX := "res://assets/shader/metal041c/Metal041C_1K-PNG_NormalDX.png"  # Normals (DirectX convention, calibration only)
const GREYS_TEX := "res://experiments/hint/hint_greys_3x1.png"  # The 3x1 grey image of the hint experiment
const BASE_SCENE := "res://base.tscn"  # The scene with the crates
const HINT_SCENE := "res://experiments/hint/hint_experiment.tscn"  # The hint-experiment scene
const CRATE_LONG_GLB := "res://assets/furniture/crate_long.glb"  # The long crate model
const CRATE_CUBE_GLB := "res://assets/furniture/crate_cube.glb"  # The small crate model
const PAINT_MATERIAL_NAME := "Crate_OliveDrab"  # The shell material in the .glb that is replaced
const HARDWARE_MATERIAL_NAME := "Crate_Hardware"  # The hardware material in the .glb that is kept
const CURL_STRIDE := 4  # curl sampling stride: 4 for 1K textures (the same as normal_map_check.gd)
const AXIS_ALIGNED := 0.99  # A normal whose largest component exceeds this counts as "pointing along an axis" (normals are compressed on import, so leave a little margin)
const EPS := 0.0001  # Tolerance when comparing decimals

## Each sampler's hints in each shader, in the order written in the source (CHANGE-BRIEF lines 197-198, 238)
const SAMPLER_HINTS := {
	CRATE_SHADER: {
		"rust_albedo": ["source_color", "filter_linear_mipmap", "repeat_enable"],
		"wear_mask": ["filter_linear_mipmap", "repeat_enable"],
	},
	HINT_SHADER: {
		"greys_source_color": ["source_color", "filter_nearest"],
		"greys_raw": ["filter_nearest"],
	},
}

## Each shader's uniforms: name -> [type, its group_uniforms group ("" = not in a group), hint_range minimum and maximum (null = not checked)]
const UNIFORMS := {
	CRATE_SHADER: {
		"rust_albedo": [TYPE_OBJECT, "", null],
		"wear_mask": [TYPE_OBJECT, "", null],
		"paint_color": [TYPE_COLOR, "paint", null],
		"paint_roughness": [TYPE_FLOAT, "paint", Vector2(0.0, 1.0)],
		"wear_amount": [TYPE_FLOAT, "wear", Vector2(0.0, 1.0)],
		"wear_softness": [TYPE_FLOAT, "wear", Vector2(0.0, 0.2)],
		"texture_scale": [TYPE_FLOAT, "mapping", Vector2(0.1, 10.0)],
	},
	HINT_SHADER: {
		"greys_source_color": [TYPE_OBJECT, "", null],
		"greys_raw": [TYPE_OBJECT, "", null],
		"use_source_color": [TYPE_BOOL, "", null],
	},
}

## What must appear in the source (defaults, constants, render_mode): [regex, description]. Headless mode cannot read uniform defaults, so the source text is read
const SOURCE_PATTERNS := {
	CRATE_SHADER: [
		["^shader_type\\s+spatial\\s*;", "crate shader is spatial"],
		["uniform\\s+vec4\\s+paint_color\\s*:\\s*source_color\\s*=\\s*vec4\\(\\s*0\\.260\\s*,\\s*0\\.283\\s*,\\s*0\\.190\\s*,\\s*1\\.0\\s*\\)\\s*;", "paint_color default vec4(0.260, 0.283, 0.190, 1.0), source_color"],
		["uniform\\s+float\\s+paint_roughness\\s*:\\s*hint_range\\(\\s*0\\.0\\s*,\\s*1\\.0\\s*\\)\\s*=\\s*0\\.85\\s*;", "paint_roughness default 0.85"],
		["uniform\\s+float\\s+wear_amount\\s*:\\s*hint_range\\(\\s*0\\.0\\s*,\\s*1\\.0\\s*\\)\\s*=\\s*0\\.1\\s*;", "wear_amount default 0.1"],
		["uniform\\s+float\\s+wear_softness\\s*:\\s*hint_range\\(\\s*0\\.0\\s*,\\s*0\\.2\\s*\\)\\s*=\\s*0\\.0\\s*;", "wear_softness default 0.0"],
		["uniform\\s+float\\s+texture_scale\\s*:\\s*hint_range\\(\\s*0\\.1\\s*,\\s*10\\.0\\s*\\)\\s*=\\s*2\\.0\\s*;", "texture_scale default 2.0"],
		["const\\s+float\\s+RUST_ROUGHNESS\\s*=\\s*0\\.79\\s*;", "const RUST_ROUGHNESS = 0.79"],
		["const\\s+float\\s+MIN_WEAR_SOFTNESS\\s*=\\s*0\\.001\\s*;", "const MIN_WEAR_SOFTNESS = 0.001"],
	],
	HINT_SHADER: [
		["^shader_type\\s+spatial\\s*;", "hint shader is spatial"],
		["render_mode\\s+unshaded\\s*;", "hint shader is unshaded"],
		["uniform\\s+bool\\s+use_source_color\\s*=\\s*true\\s*;", "use_source_color default true"],
	],
}

## Each material: shader, stored values, bound textures, parameters not stored (shader default applies) (CHANGE-BRIEF lines 213-216, 239)
const MATERIALS := {
	CRATE_LONG_MAT: {
		"shader": CRATE_SHADER,
		"values": {"wear_amount": 0.2, "paint_roughness": 0.95},
		"textures": {"rust_albedo": COLOR_TEX, "wear_mask": DISP_TEX},
		"unset": ["paint_color", "wear_softness", "texture_scale"],
	},
	CRATE_CUBE_MAT: {
		"shader": CRATE_SHADER,
		"values": {"wear_amount": 0.1, "paint_roughness": 0.85},
		"textures": {"rust_albedo": COLOR_TEX, "wear_mask": DISP_TEX},
		"unset": ["paint_color", "wear_softness", "texture_scale"],
	},
	HINT_SRC_MAT: {
		"shader": HINT_SHADER,
		"values": {"use_source_color": true},
		"textures": {"greys_source_color": GREYS_TEX, "greys_raw": GREYS_TEX},
		"unset": [],
	},
	HINT_RAW_MAT: {
		"shader": HINT_SHADER,
		"values": {"use_source_color": false},
		"textures": {"greys_source_color": GREYS_TEX, "greys_raw": GREYS_TEX},
		"unset": [],
	},
}

## Each texture's import settings: [compress/mode, compress/normal_map, mipmaps/generate, detect_3d/compress_to]
## (CHANGE-BRIEF lines 183-187, 237; detect_3d/compress_to = 0 means the editor will not change the compression by itself, failure case 10)
const IMPORTS := {
	COLOR_TEX: [2, 2, true, 0],
	DISP_TEX: [0, 2, true, 0],
	ROUGH_TEX: [2, 2, true, 0],
	NORMAL_GL_TEX: [2, 1, true, 0],
	NORMAL_DX_TEX: [2, 1, true, 0],
	GREYS_TEX: [0, 2, false, 0],
}

## The Image.Format that get_image() reads back on the CPU side after import (measured on this Windows computer the first time this test ran on 2026-11-01,
## not a value from CHANGE-BRIEF; which format VRAM compression picks depends on the platform, here desktop s3tc)
const IMPORTED_FORMATS := {
	COLOR_TEX: Image.FORMAT_DXT1,
	DISP_TEX: Image.FORMAT_L8,
	ROUGH_TEX: Image.FORMAT_DXT1,
	NORMAL_GL_TEX: Image.FORMAT_RGTC_RG,
	NORMAL_DX_TEX: Image.FORMAT_RGTC_RG,
	GREYS_TEX: Image.FORMAT_RGB8,
}

## The two crates: node name in the scene -> [model, the material it should carry]
const CRATES := {
	"crate_long": [CRATE_LONG_GLB, CRATE_LONG_MAT],
	"crate_cube": [CRATE_CUBE_GLB, CRATE_CUBE_MAT],
}

## Hint scene: quad node name -> the material it should carry
const HINT_QUADS := {
	"QuadSourceColor": HINT_SRC_MAT,
	"QuadRaw": HINT_RAW_MAT,
}

## The three ceiling lights in base.tscn (CHANGE-BRIEF line 162; colour, energy, range and shadow read from base.tscn lines 156-182)
const CEILING_LIGHTS := ["ceiling_light_1", "ceiling_light_2", "ceiling_light_3"]
const CEILING_LIGHT_COLOR := Color(0.78, 0.86, 1.0, 1.0)
const CEILING_LIGHT_ENERGY := 1.5
const CEILING_LIGHT_RANGE := 8.0
const BASE_AMBIENT_COLOR := Color(0.45, 0.5, 0.6, 1.0)  # CHANGE-BRIEF line 162
const BASE_AMBIENT_ENERGY := 0.35  # CHANGE-BRIEF line 162
const BASE_BACKGROUND_COLOR := Color(0.03, 0.035, 0.045, 1.0)  # base.tscn line 13
const EXPOSURE := 1.0  # Exposure of both scenes (CHANGE-BRIEF lines 162, 239)

# ============================================================
# Member variables: what the test records while it runs
# ============================================================
var failures := 0  # How many checks failed

# ============================================================
# Engine callbacks: functions Godot calls automatically at set times (the entry points)
# ============================================================
## Called by Godot automatically: once, when the script starts as the SceneTree. Runs every check in order, prints the results and quits.
func _initialize() -> void:
	_check_project()
	for shader_path in [CRATE_SHADER, HINT_SHADER]:
		_check_sampler_hints(shader_path)
		_check_source_patterns(shader_path)
		_check_uniform_list(shader_path)
	for mat_path in MATERIALS:
		_check_material(mat_path)
	_check_same_crate_shader()
	for tex_path in IMPORTS:
		_check_import(tex_path)
	_check_use_external()
	_check_base_scene()
	_check_hint_scene()
	_check_formats()
	_check_normal_maps()
	print("== %s: %d failure(s) ==" % ["ALL PASS" if failures == 0 else "FAILED", failures])
	quit(1 if failures > 0 else 0)

# ============================================================
# Feature functions: the parts of the test
# ============================================================
## Records one check: prints PASS if it passed, otherwise prints FAIL and counts it. Called by every check function below.
func _check(ok: bool, what: String) -> void:
	print(("  PASS  " if ok else "  FAIL  ") + what)
	if not ok:
		failures += 1


## Project settings: the renderer is Forward+ and HDR 2D is off (the predictions in CHANGE-BRIEF lines 85 and 240 depend on both).
func _check_project() -> void:
	_check(ProjectSettings.get_setting("rendering/renderer/rendering_method") == "forward_plus",
		"project: rendering_method is forward_plus")
	_check(ProjectSettings.get_setting("rendering/viewport/hdr_2d") == false, "project: hdr_2d is off")


## Reads the shader source text, finds every sampler2D and the hints after its colon, and compares them in order with the expected table.
## An extra or missing sampler also fails. Deleting source_color from rust_albedo (the mutation the assignment requires) fails here.
func _check_sampler_hints(shader_path: String) -> void:
	var source := FileAccess.get_file_as_string(shader_path)
	var re := RegEx.create_from_string("uniform\\s+sampler2D\\s+(\\w+)\\s*(?::\\s*([^;=]*))?\\s*;")
	var found := {}
	for m in re.search_all(source):
		var hints: Array = []
		for h in m.get_string(2).split(",", false):
			hints.append(h.strip_edges())
		found[m.get_string(1)] = hints
	var expected: Dictionary = SAMPLER_HINTS[shader_path]
	_check(found.keys().size() == expected.keys().size(),
		"%s: %d sampler(s) in source (found %s)" % [shader_path.get_file(), expected.size(), found.keys()])
	for sampler_name in expected:
		_check(found.has(sampler_name) and found[sampler_name] == expected[sampler_name],
			"%s: %s hints are %s (source: %s)" % [shader_path.get_file(), sampler_name,
			", ".join(expected[sampler_name]), ", ".join(found.get(sampler_name, ["<missing>"]))])


## Reads the shader source text and checks how the defaults, constants and render_mode are written (headless mode cannot read uniform defaults).
func _check_source_patterns(shader_path: String) -> void:
	var source := FileAccess.get_file_as_string(shader_path)
	for pattern in SOURCE_PATTERNS[shader_path]:
		var re := RegEx.create_from_string("(?m)" + pattern[0])
		_check(re.search(source) != null, "%s: source: %s" % [shader_path.get_file(), pattern[1]])
	if shader_path == CRATE_SHADER:
		_check(source.find("unshaded") == -1, "%s: source: no render_mode unshaded (lit by the scene)" % shader_path.get_file())


## Reads the uniforms the shader actually parsed with get_shader_uniform_list(true): name, type, group, hint_range.
## If the shader fails to parse the list is empty, so this also catches syntax errors.
func _check_uniform_list(shader_path: String) -> void:
	var shader: Shader = load(shader_path)
	var group := ""
	var parsed := {}  # name -> {"type", "group", "hint", "hint_string"}
	for u in shader.get_shader_uniform_list(true):
		if u["usage"] & PROPERTY_USAGE_GROUP:
			group = u["name"]
			continue
		parsed[u["name"]] = {"type": u["type"], "group": group, "hint": u["hint"], "hint_string": u["hint_string"]}
	var expected: Dictionary = UNIFORMS[shader_path]
	_check(parsed.size() == expected.size(),
		"%s: uniform list has %d entries (got %s)" % [shader_path.get_file(), expected.size(), parsed.keys()])
	for uniform_name in expected:
		var want: Array = expected[uniform_name]
		var got: Dictionary = parsed.get(uniform_name, {})
		_check(not got.is_empty() and got["type"] == want[0],
			"%s: uniform %s has type %s" % [shader_path.get_file(), uniform_name, type_string(want[0])])
		_check(not got.is_empty() and got["group"] == want[1],
			"%s: uniform %s is in group '%s' (got '%s')" % [shader_path.get_file(), uniform_name, want[1], got.get("group", "<missing>")])
		if want[0] == TYPE_OBJECT:
			_check(not got.is_empty() and got["hint"] == PROPERTY_HINT_RESOURCE_TYPE and got["hint_string"] == "Texture2D",
				"%s: uniform %s is a Texture2D sampler" % [shader_path.get_file(), uniform_name])
		if want[2] != null:
			# hint_string is "min,max,step", with numbers turned into text as 32-bit floats (0.1 -> 0.10000000149012), so compare them as numbers
			var parts := String(got.get("hint_string", "")).split(",")
			var ok: bool = not got.is_empty() and got["hint"] == PROPERTY_HINT_RANGE and parts.size() >= 2 \
				and absf(parts[0].to_float() - want[2].x) < EPS and absf(parts[1].to_float() - want[2].y) < EPS
			_check(ok, "%s: uniform %s has hint_range(%s, %s) (got '%s')" % [shader_path.get_file(), uniform_name,
				snappedf(want[2].x, EPS), snappedf(want[2].y, EPS), got.get("hint_string", "")])


## One material: the shader it uses, the stored values, the bound textures, which parameters are not stored (shader default applies).
## Also reads the shader_parameter/ lines in the .tres text to confirm the material stores exactly the parameters in the table, no more and no fewer.
func _check_material(mat_path: String) -> void:
	var want: Dictionary = MATERIALS[mat_path]
	var tag := mat_path.get_file()
	var mat := load(mat_path) as ShaderMaterial
	_check(mat != null, "%s: loads as ShaderMaterial" % tag)
	if mat == null:
		return
	_check(mat.shader != null and mat.shader.resource_path == want["shader"], "%s: shader is %s" % [tag, want["shader"]])
	for p in want["values"]:
		var v = mat.get_shader_parameter(p)
		var ok: bool = v != null and (v == want["values"][p] if typeof(want["values"][p]) == TYPE_BOOL else absf(float(v) - want["values"][p]) < EPS)
		_check(ok, "%s: %s = %s (got %s)" % [tag, p, want["values"][p], v])
	for p in want["textures"]:
		var t = mat.get_shader_parameter(p)
		_check(t is Texture2D and t.resource_path == want["textures"][p],
			"%s: %s binds %s" % [tag, p, String(want["textures"][p]).get_file()])
	for p in want["unset"]:
		_check(mat.get_shader_parameter(p) == null, "%s: %s not stored (shader default applies)" % [tag, p])
	var stored: Array = []
	for line in FileAccess.get_file_as_string(mat_path).split("\n"):
		if line.begins_with("shader_parameter/"):
			stored.append(line.substr("shader_parameter/".length()).get_slice(" ", 0))
	var expected_stored: Array = want["values"].keys() + want["textures"].keys()
	stored.sort()
	expected_stored.sort()
	_check(stored == expected_stored, "%s: .tres stores exactly %s (got %s)" % [tag, expected_stored, stored])


## Both crate materials use the same shader file (same path, and it loads as the same Shader object).
func _check_same_crate_shader() -> void:
	var a := load(CRATE_LONG_MAT) as ShaderMaterial
	var b := load(CRATE_CUBE_MAT) as ShaderMaterial
	_check(a != null and b != null and a.shader.resource_path == b.shader.resource_path and a.shader == b.shader,
		"both crate materials reference the same shader (%s)" % CRATE_SHADER)


## Reads one texture's .import with ConfigFile and compares the four import settings.
func _check_import(tex_path: String) -> void:
	var cf := ConfigFile.new()
	var err := cf.load(tex_path + ".import")
	_check(err == OK, "%s.import: readable" % tex_path.get_file())
	if err != OK:
		return
	var want: Array = IMPORTS[tex_path]
	var got := [cf.get_value("params", "compress/mode"), cf.get_value("params", "compress/normal_map"),
		cf.get_value("params", "mipmaps/generate"), cf.get_value("params", "detect_3d/compress_to")]
	var keys := ["compress/mode", "compress/normal_map", "mipmaps/generate", "detect_3d/compress_to"]
	for i in keys.size():
		_check(got[i] == want[i], "%s.import: %s = %s (got %s)" % [tex_path.get_file(), keys[i], want[i], got[i]])


## Reads _subresources in both .glb.import files with ConfigFile: only the shell material is behind Use External and its path points to the right .tres; the hardware is untouched.
func _check_use_external() -> void:
	for node_name in CRATES:
		var glb: String = CRATES[node_name][0]
		var mat_path: String = CRATES[node_name][1]
		var tag := glb.get_file() + ".import"
		var cf := ConfigFile.new()
		_check(cf.load(glb + ".import") == OK, "%s: readable" % tag)
		var sub: Dictionary = cf.get_value("params", "_subresources", {})
		var mats: Dictionary = sub.get("materials", {})
		_check(mats.keys() == [PAINT_MATERIAL_NAME], "%s: only %s is overridden (got %s)" % [tag, PAINT_MATERIAL_NAME, mats.keys()])
		var entry: Dictionary = mats.get(PAINT_MATERIAL_NAME, {})
		_check(entry.get("use_external/enabled", false) == true, "%s: %s use_external/enabled = true" % [tag, PAINT_MATERIAL_NAME])
		_check(entry.get("use_external/fallback_path", "") == mat_path, "%s: fallback_path = %s" % [tag, mat_path])
		var uid_text: String = entry.get("use_external/path", "")
		var id := ResourceUID.text_to_id(uid_text)
		var resolved := ResourceUID.get_id_path(id) if ResourceUID.has_id(id) else "<unknown uid>"
		_check(resolved == mat_path, "%s: use_external/path %s resolves to %s (got %s)" % [tag, uid_text, mat_path, resolved])


## Loads base.tscn (instantiated only, not added to the scene tree, so the player scripts do not run):
## the crates' shell surfaces carry the right .tres, the hardware still has its original material, all shell normals point along an axis; the three ceiling lights; the environment settings.
func _check_base_scene() -> void:
	var base: Node = load(BASE_SCENE).instantiate()
	for node_name in CRATES:
		var crate := base.get_node_or_null(node_name)
		_check(crate != null, "base.tscn: %s exists" % node_name)
		if crate == null:
			continue
		var wear_surfaces := 0
		var hardware_surfaces := 0
		var normals := 0
		var off_axis := 0
		for mi in crate.find_children("*", "MeshInstance3D", true, false):
			for s in mi.mesh.get_surface_count():
				var m: Material = mi.get_active_material(s)
				if m != null and m.resource_path == CRATES[node_name][1]:
					wear_surfaces += 1
					for n in mi.mesh.surface_get_arrays(s)[Mesh.ARRAY_NORMAL]:
						normals += 1
						if maxf(absf(n.x), maxf(absf(n.y), absf(n.z))) < AXIS_ALIGNED:
							off_axis += 1
				elif m is BaseMaterial3D and m.resource_name == HARDWARE_MATERIAL_NAME:
					hardware_surfaces += 1
		_check(wear_surfaces >= 1, "base.tscn: %s paint surface uses %s (%d surface(s))" % [node_name, CRATES[node_name][1].get_file(), wear_surfaces])
		_check(hardware_surfaces >= 1, "base.tscn: %s keeps the .glb's %s material (%d surface(s))" % [node_name, HARDWARE_MATERIAL_NAME, hardware_surfaces])
		_check(normals > 0 and off_axis == 0, "base.tscn: %s paint-surface normals all axis-aligned (%d normals, %d off-axis)" % [node_name, normals, off_axis])
	var lights: Array = base.find_children("*", "Light3D", true, false)
	_check(lights.size() == CEILING_LIGHTS.size(), "base.tscn: %d Light3D nodes (got %d)" % [CEILING_LIGHTS.size(), lights.size()])
	for light_name in CEILING_LIGHTS:
		var l := base.get_node_or_null(light_name) as OmniLight3D
		_check(l != null and l.light_color.is_equal_approx(CEILING_LIGHT_COLOR) and is_equal_approx(l.light_energy, CEILING_LIGHT_ENERGY)
			and is_equal_approx(l.omni_range, CEILING_LIGHT_RANGE) and l.shadow_enabled,
			"base.tscn: %s is an OmniLight3D, colour %s, energy %s, range %s, shadows on" % [light_name, CEILING_LIGHT_COLOR, CEILING_LIGHT_ENERGY, CEILING_LIGHT_RANGE])
	var env := _find_environment(base)
	_check(env != null, "base.tscn: WorldEnvironment has an Environment")
	if env != null:
		_check(env.background_mode == Environment.BG_COLOR and env.background_color.is_equal_approx(BASE_BACKGROUND_COLOR),
			"base.tscn: background is a custom colour %s" % BASE_BACKGROUND_COLOR)
		_check(env.ambient_light_source == Environment.AMBIENT_SOURCE_COLOR and env.ambient_light_color.is_equal_approx(BASE_AMBIENT_COLOR)
			and is_equal_approx(env.ambient_light_energy, BASE_AMBIENT_ENERGY),
			"base.tscn: ambient light colour %s, energy %s" % [BASE_AMBIENT_COLOR, BASE_AMBIENT_ENERGY])
		_check_post_effects(env, "base.tscn")
	base.free()


## Loads the hint-experiment scene (instantiated only): both quads carry the right material and face the camera; no lights; the environment is Linear, exposure 1.0, glow/fog/adjustments off.
func _check_hint_scene() -> void:
	var scene: Node = load(HINT_SCENE).instantiate()
	var cam := scene.get_node_or_null("Camera3D") as Camera3D
	_check(cam != null and cam.current, "hint_experiment.tscn: Camera3D is current")
	for quad_name in HINT_QUADS:
		var q := scene.get_node_or_null(quad_name) as MeshInstance3D
		_check(q != null and q.material_override != null and q.material_override.resource_path == HINT_QUADS[quad_name],
			"hint_experiment.tscn: %s material_override is %s" % [quad_name, String(HINT_QUADS[quad_name]).get_file()])
		if q != null and cam != null:
			var to_cam := cam.transform.origin - q.transform.origin
			_check(q.mesh is QuadMesh and to_cam.dot(q.transform.basis.z) > 0.0, "hint_experiment.tscn: %s is a QuadMesh facing the camera" % quad_name)
	_check(scene.find_children("*", "Light3D", true, false).is_empty(), "hint_experiment.tscn: no Light3D (shader is unshaded)")
	var env := _find_environment(scene)
	_check(env != null, "hint_experiment.tscn: WorldEnvironment has an Environment")
	if env != null:
		_check_post_effects(env, "hint_experiment.tscn")
	scene.free()


## Shared by both scenes: tonemap Linear, exposure 1.0; glow, fog, volumetric fog, adjustments, SSAO, SSIL, SDFGI and SSR all off.
## Neither .tscn writes these values; they rely on the Environment defaults, so they are pinned here.
func _check_post_effects(env: Environment, tag: String) -> void:
	_check(env.tonemap_mode == Environment.TONE_MAPPER_LINEAR, "%s: tonemap is Linear (got %d)" % [tag, env.tonemap_mode])
	_check(is_equal_approx(env.tonemap_exposure, EXPOSURE), "%s: exposure %s (got %s)" % [tag, EXPOSURE, env.tonemap_exposure])
	_check(not env.glow_enabled and not env.fog_enabled and not env.volumetric_fog_enabled and not env.adjustment_enabled,
		"%s: glow, fog, volumetric fog and adjustments off" % tag)
	_check(not env.ssao_enabled and not env.ssil_enabled and not env.sdfgi_enabled and not env.ssr_enabled,
		"%s: SSAO, SSIL, SDFGI and SSR off" % tag)


## Finds the Environment of the first WorldEnvironment in a scene. Called by both scene checks.
func _find_environment(scene: Node) -> Environment:
	for we in scene.find_children("*", "WorldEnvironment", true, false):
		return (we as WorldEnvironment).environment
	return null


## Each texture: prints the decoded source file's format and size; checks the format get_image() reads back after import and whether it has mipmaps.
## The format numbers are the Image.Format enum (L8 = 0, RGB8 = 4, DXT1 = 17, RGTC_RG = 21). The format the GPU actually uses cannot be seen in headless mode.
func _check_formats() -> void:
	for tex_path in IMPORTS:
		var src := Image.load_from_file(ProjectSettings.globalize_path(tex_path))
		print("  INFO  %s: source file decodes to Image.Format %d, size %s" % [
			tex_path.get_file(), src.get_format() if src != null else -1, src.get_size() if src != null else Vector2i.ZERO])
		var tex := load(tex_path) as Texture2D
		var img: Image = tex.get_image() if tex != null else null
		_check(img != null and img.get_format() == IMPORTED_FORMATS[tex_path],
			"%s: imported get_image() format is %d (got %s)" % [tex_path.get_file(), IMPORTED_FORMATS[tex_path], str(img.get_format()) if img != null else "<null>"])
		_check(img != null and img.has_mipmaps() == IMPORTS[tex_path][2],
			"%s: imported image has mipmaps = %s" % [tex_path.get_file(), IMPORTS[tex_path][2]])


## Normal maps: decodes the source files (not through the importer), computes curl_ratio from normal_map_check.gd under both conventions and prints it.
## Checks: each map is lower under its own convention than under the other (GL with directx=false, DX with directx=true); the NormalGL the game would use is lower under the GL convention.
func _check_normal_maps() -> void:
	for pair in [[NORMAL_GL_TEX, false], [NORMAL_DX_TEX, true]]:
		var img := Image.load_from_file(ProjectSettings.globalize_path(pair[0]))
		_check(img != null and not img.is_empty(), "%s: source decodes" % String(pair[0]).get_file())
		if img == null or img.is_empty():
			continue
		var as_gl: float = NormalMapCheck.curl_ratio(img, false, CURL_STRIDE)
		var as_dx: float = NormalMapCheck.curl_ratio(img, true, CURL_STRIDE)
		print("  INFO  curl_ratio %s directx=false: %.4f" % [String(pair[0]).get_file(), as_gl])
		print("  INFO  curl_ratio %s directx=true : %.4f" % [String(pair[0]).get_file(), as_dx])
		var own: float = as_dx if pair[1] else as_gl
		var other: float = as_gl if pair[1] else as_dx
		_check(own < other, "%s: lower under its own (%s) convention" % [String(pair[0]).get_file(), "DX" if pair[1] else "GL"])

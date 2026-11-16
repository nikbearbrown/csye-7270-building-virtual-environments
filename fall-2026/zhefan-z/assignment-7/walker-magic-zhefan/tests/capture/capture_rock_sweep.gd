extends "res://tests/capture/capture_common.gd"
## Rock captures (CHANGE-BRIEF section 4). Open tests/capture/capture_rock_sweep.tscn, F6, press a key.
## "default" in the sweep is the value mat_rock_frosted.tres sets (what F9 shows), and it is restored after each
## uniform; the shader's own default is in the source text and is printed alongside where it differs.
## F12: the shader is loaded when the scene starts, so after editing rock_frost.gdshader, save it and run the
## scene again with F6 before pressing F12. The printed hashes show whether the running code is the edited text.

const SHADER_PATH := "res://shaders/rock_frost.gdshader"
const DRY := "res://assets/materials/mat_rock_dry.tres"
const FROSTED := "res://assets/materials/mat_rock_frosted.tres"

@onready var dry_rock: MeshInstance3D = $MaterialCompare/RockDry/Rock
@onready var frosted_rock: MeshInstance3D = $MaterialCompare/RockFrosted/Rock
@onready var mat_dry := dry_rock.get_surface_override_material(0) as ShaderMaterial
@onready var mat_frosted := frosted_rock.get_surface_override_material(0) as ShaderMaterial

var md5_at_start := ""


func _ready() -> void:
	md5_at_start = FileAccess.get_md5(SHADER_PATH)
	super()
	print(JSON.stringify({"dry": mat_dry.resource_path, "frosted": mat_frosted.resource_path,
		"separate_objects": mat_dry != mat_frosted, "shader_md5_on_disk_at_start": md5_at_start}))


func bindings() -> Dictionary:
	return {"F9": "rock_compare_default.png",
		"F10": "mat_rock_frosted only: each non-texture uniform at min, default, max (colours black, default, "
			+ "white), rock_sweep_<uniform>_<min|default|max>.png, default restored after each uniform",
		"F11": "mat_rock_dry only: normal_scale 0.0, rock_one_material_changed.png, restored",
		"F12": "rock_compare_after_shader_edit.png (edit and save the shader, F6 again, then F12)"}


func on_key(keycode: Key) -> void:
	match keycode:
		KEY_F9:
			busy = true
			await capture("rock_compare_default.png")
			busy = false
		KEY_F10:
			sweep()
		KEY_F11:
			one_material_changed()
		KEY_F12:
			after_shader_edit()


func sweep() -> void:
	busy = true
	for u: Dictionary in mat_frosted.shader.get_shader_uniform_list():
		if u.type == TYPE_OBJECT:
			continue
		var original: Variant = mat_frosted.get_shader_parameter(u.name)
		var values := {}
		if u.type == TYPE_FLOAT and u.hint == PROPERTY_HINT_RANGE:
			var parts: PackedStringArray = String(u.hint_string).split(",")
			values = {"min": parts[0].to_float(), "default": original, "max": parts[1].to_float()}
		elif u.type == TYPE_COLOR:
			values = {"min": Color.BLACK, "default": original, "max": Color.WHITE}
		else:
			print(JSON.stringify({"skipped": u.name, "why": "no range to sweep", "type": type_string(u.type)}))
			continue
		for which: String in ["min", "default", "max"]:
			mat_frosted.set_shader_parameter(u.name, values[which])
			await capture("rock_sweep_%s_%s.png" % [u.name, which], {"material": FROSTED.get_file(),
				"uniform": u.name, "value": var_to_str(values[which])})
		mat_frosted.set_shader_parameter(u.name, original)
		print(JSON.stringify({"restored": u.name, "value": var_to_str(mat_frosted.get_shader_parameter(u.name))}))
	busy = false


func one_material_changed() -> void:
	busy = true
	var original: Variant = mat_dry.get_shader_parameter("normal_scale")
	mat_dry.set_shader_parameter("normal_scale", 0.0)
	await capture("rock_one_material_changed.png", {"material": DRY.get_file(), "uniform": "normal_scale",
		"value": 0.0, "frosted_normal_scale": mat_frosted.get_shader_parameter("normal_scale")})
	mat_dry.set_shader_parameter("normal_scale", original)
	print(JSON.stringify({"restored": "normal_scale", "value": var_to_str(mat_dry.get_shader_parameter("normal_scale"))}))
	busy = false


func after_shader_edit() -> void:
	busy = true
	await capture("rock_compare_after_shader_edit.png", {"shader_md5_on_disk_at_start": md5_at_start,
		"shader_md5_on_disk_now": FileAccess.get_md5(SHADER_PATH),
		"running_code_md5": mat_frosted.shader.code.md5_text(),
		"on_disk_md5_of_text": FileAccess.get_file_as_string(SHADER_PATH).md5_text()})
	busy = false

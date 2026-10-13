extends SceneTree
# What does the Inspector get for each kind of uniform? The Inspector builds its widgets from ShaderMaterial.get_property_list():
# a Color property gets a color picker, a float with a range hint gets a slider, and the group label is a property of the list.
# Run (scratch project with this file in it):  godot --path <project dir> --script res://verify1.gd
const CODE := "shader_type canvas_item;\nuniform vec4 tint : source_color = vec4(0.37, 0.64, 0.57, 1.0);\nuniform vec4 plain = vec4(0.1, 0.2, 0.3, 0.4);\nuniform float amount : hint_range(0.0, 1.0) = 0.5;\nuniform float speed = 2.0;\nuniform int count : hint_range(0, 10) = 3;\nvoid fragment() { COLOR = tint * amount; }\n"

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func run() -> void:
	var sh := Shader.new()
	sh.code = CODE
	var mat := ShaderMaterial.new()
	mat.shader = sh
	var rows: Array = []
	var groups: Array = []
	for p in mat.get_property_list():
		var n := String(p["name"])
		var usage: int = p["usage"]
		if usage & PROPERTY_USAGE_GROUP:
			groups.append({"group": n, "prefix": p.get("hint_string", "")})
		elif n.begins_with("shader_parameter/"):
			rows.append({"name": n, "type": p["type"], "type_name": type_string(p["type"]), "hint": p["hint"], "hint_string": p["hint_string"]})
	out("L-inspector-properties", {"engine": Engine.get_version_info()["string"], "groups": groups, "uniform_properties": rows,
		"reading": "type_name Color = the Inspector shows a color picker; float/int with hint 1 (PROPERTY_HINT_RANGE) = a slider; plain vec4 is not a Color."})
	quit(0)

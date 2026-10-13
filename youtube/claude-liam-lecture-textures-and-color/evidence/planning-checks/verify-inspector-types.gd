extends SceneTree
# What does the Inspector get to work with? Shader.get_shader_uniform_list() describes each uniform like Object.get_property_list():
# a Variant type and a property hint. The Inspector picks its widget from that pair (TYPE_COLOR -> colour picker, a Vector4 -> four number boxes,
# a float with PROPERTY_HINT_RANGE -> slider). This script prints the pair for the uniforms the film shows. Run: godot --path <dir> --script res://verify-inspector-types.gd

const CODE := """shader_type canvas_item;
uniform vec4 tint : source_color = vec4(1.0);
uniform vec4 plain_vec4 = vec4(1.0);
uniform vec3 rgb_tint : source_color;
uniform float progress : hint_range(0.0, 1.0) = 0.0;
uniform sampler2D noise_tex;
uniform sampler2D ramp_tex : source_color;
uniform sampler2D tex_nearest : filter_nearest, repeat_disable;
void fragment() { COLOR = tint * plain_vec4 * vec4(rgb_tint, 1.0) * texture(noise_tex, UV) * texture(ramp_tex, UV) * texture(tex_nearest, UV) * progress; }
"""

func _initialize() -> void: call_deferred("run")

func run() -> void:
	var sh := Shader.new()
	sh.code = CODE
	for u in sh.get_shader_uniform_list():
		print("RESULT " + JSON.stringify({"name": u["name"], "type": u["type"], "type_name": type_string(u["type"]), "hint": u["hint"], "hint_string": u["hint_string"], "usage": u["usage"]}))
	print("PROPERTY_HINT_RANGE=", PROPERTY_HINT_RANGE, " PROPERTY_HINT_COLOR_NO_ALPHA=", PROPERTY_HINT_COLOR_NO_ALPHA, " PROPERTY_HINT_RESOURCE_TYPE=", PROPERTY_HINT_RESOURCE_TYPE)
	# The picked colour is stored as typed (sRGB numbers), not converted.
	var mat := ShaderMaterial.new()
	mat.shader = sh
	mat.set_shader_parameter("tint", Color("#336699"))
	var back: Color = mat.get_shader_parameter("tint")
	print("RESULT " + JSON.stringify({"id": "picked-color-stored-as-typed", "picked_hex": "#336699", "stored": [snappedf(back.r, 0.0001), snappedf(back.g, 0.0001), snappedf(back.b, 0.0001)]}))
	quit(0)

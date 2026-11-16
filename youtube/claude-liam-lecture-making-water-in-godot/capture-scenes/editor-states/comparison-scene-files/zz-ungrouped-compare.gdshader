shader_type spatial;
render_mode blend_mix, depth_draw_opaque, cull_back;
// scratch comparison only (not a film shader): the same two uniforms as the film's Color and Clarity folders, but with NO group_uniforms line
uniform vec3 water_color : source_color = vec3(0.10, 0.45, 0.70);
uniform float roughness : hint_range(0.0, 1.0) = 0.15;
uniform float opacity : hint_range(0.0, 1.0) = 0.7;
void fragment() {
	ALBEDO = water_color;
	ROUGHNESS = roughness;
	ALPHA = opacity;
}

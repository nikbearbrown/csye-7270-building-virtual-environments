shader_type spatial;
render_mode blend_mix, depth_draw_always, cull_back;

group_uniforms Color;
uniform vec3 water_color : source_color = vec3(0.10, 0.45, 0.70);
uniform float roughness : hint_range(0.0, 1.0) = 0.15;
group_uniforms Clarity;
uniform float opacity : hint_range(0.0, 1.0) = 0.7;
group_uniforms;

void fragment() {
	ALBEDO = water_color;
	ROUGHNESS = roughness;
	ALPHA = opacity;
}

shader_type spatial;
render_mode blend_mix, depth_draw_opaque, cull_back;

uniform vec3 water_color : source_color = vec3(0.10, 0.45, 0.70);
uniform vec3 foam_color : source_color = vec3(0.92, 0.97, 1.0);
uniform float roughness : hint_range(0.0, 1.0) = 0.15;
uniform float foam_roughness : hint_range(0.0, 1.0) = 0.9;
uniform float opacity : hint_range(0.0, 1.0) = 0.7;
uniform float edge_width : hint_range(0.01, 0.5) = 0.1;
uniform sampler2D cell_tex : filter_linear_mipmap, repeat_enable;
uniform float cell_scale : hint_range(0.5, 8.0) = 1.0;
uniform float scroll_speed : hint_range(0.0, 0.2) = 0.02;

void fragment() {
	float edge = texture(cell_tex, UV * cell_scale + vec2(1.0, 0.4) * TIME * scroll_speed).r;
	float foam = 1.0 - smoothstep(0.0, edge_width, edge);
	ALBEDO = mix(water_color, foam_color, foam);
	ALPHA = mix(opacity, 1.0, foam);
	ROUGHNESS = mix(roughness, foam_roughness, foam);
}

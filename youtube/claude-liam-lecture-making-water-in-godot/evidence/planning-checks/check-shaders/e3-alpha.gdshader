shader_type spatial;
render_mode unshaded, blend_mix, depth_draw_opaque, cull_back;
uniform vec3 water_color : source_color = vec3(0.10, 0.45, 0.70);
uniform float opacity : hint_range(0.0, 1.0) = 0.7;
void fragment() {
	ALBEDO = water_color;
	ALPHA = opacity;
}

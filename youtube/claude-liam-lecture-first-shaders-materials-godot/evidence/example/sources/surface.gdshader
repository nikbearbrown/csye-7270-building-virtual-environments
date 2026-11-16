shader_type spatial;
group_uniforms Surface;
uniform sampler2D color_map : source_color, filter_nearest;
uniform sampler2D roughness_map : filter_nearest;
uniform vec4 tint : source_color = vec4(1.0);
uniform float roughness_gain : hint_range(0.0, 1.0) = 0.8;
group_uniforms Pattern;
uniform float uv_scale : hint_range(0.25, 4.0) = 1.0;
uniform float metallic_gain : hint_range(0.0, 1.0) = 0.0;
void fragment() {
	ALBEDO = texture(color_map, UV * uv_scale).rgb * tint.rgb;
	ROUGHNESS = clamp(texture(roughness_map, UV * uv_scale).r * roughness_gain, 0.05, 1.0);
	METALLIC = metallic_gain;
}

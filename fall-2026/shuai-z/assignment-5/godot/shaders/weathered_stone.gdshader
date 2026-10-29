shader_type spatial;

uniform sampler2D albedo_tex : source_color, filter_linear_mipmap, repeat_enable;
uniform sampler2D normal_tex : hint_normal, filter_linear_mipmap, repeat_enable;
uniform sampler2D roughness_tex : filter_linear_mipmap, repeat_enable;

group_uniforms surface;
uniform vec4 albedo_tint : source_color = vec4(1.0);
uniform float uv_scale : hint_range(0.25, 4.0, 0.05) = 1.0;

group_uniforms relief;
uniform float normal_strength : hint_range(0.0, 2.0, 0.05) = 1.0;
uniform float roughness_offset : hint_range(-0.5, 0.5, 0.01) = 0.0;
group_uniforms;

void fragment() {
	vec2 scaled_uv = UV * uv_scale;
	ALBEDO = texture(albedo_tex, scaled_uv).rgb * albedo_tint.rgb;
	NORMAL_MAP = texture(normal_tex, scaled_uv).rgb;
	NORMAL_MAP_DEPTH = normal_strength;
	ROUGHNESS = clamp(texture(roughness_tex, scaled_uv).r + roughness_offset, 0.0, 1.0);
}

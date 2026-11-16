shader_type spatial;
render_mode blend_mix, depth_draw_opaque, cull_back;

group_uniforms Color;
uniform vec3 water_color : source_color = vec3(0.10, 0.45, 0.70);
uniform float roughness : hint_range(0.0, 1.0) = 0.15;
group_uniforms Clarity;
uniform float opacity : hint_range(0.0, 1.0) = 0.7;
group_uniforms Ripples;
uniform sampler2D normal_a : hint_normal, filter_linear_mipmap, repeat_disable;
uniform float ripple_scale : hint_range(0.5, 8.0) = 3.0;
uniform float ripple_speed : hint_range(0.0, 0.2) = 0.03;
uniform float ripple_strength : hint_range(0.0, 2.0) = 0.8;
group_uniforms;

void fragment() {
	ALBEDO = water_color;
	ROUGHNESS = roughness;
	ALPHA = opacity;
	vec2 uv = UV * ripple_scale + vec2(1.0, 0.4) * TIME * ripple_speed;
	NORMAL_MAP = texture(normal_a, uv).rgb;
	NORMAL_MAP_DEPTH = ripple_strength;
}

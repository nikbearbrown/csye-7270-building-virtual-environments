shader_type spatial;
render_mode unshaded, blend_add, cull_disabled, depth_draw_never, shadows_disabled, fog_disabled;

uniform float fire_remaining : hint_range(0.0, 1.0, 0.01) = 1.0;
uniform vec4 hot_color : source_color = vec4(1.0, 1.0, 0.0, 1.0);
uniform vec4 ember_color : source_color = vec4(1.0, 0.0, 0.0, 1.0);
uniform float intensity : hint_range(0.0, 1.0, 0.01) = 0.6;
uniform float flicker_amount : hint_range(0.0, 0.2, 0.01) = 0.08;

void fragment() {
	vec2 p = 2.0 * UV - 1.0;
	p.x *= 1.0 + 1.5 * max(-p.y, 0.0);
	p.x += flicker_amount * sin(8.0 * UV.y + 7.0 * TIME) * (1.0 - UV.y);
	float shape = clamp(1.0 - dot(p, p), 0.0, 1.0);
	float flicker = 1.0 + flicker_amount * sin(11.0 * TIME);

	ALBEDO = mix(ember_color.rgb, hot_color.rgb, fire_remaining) * intensity;
	ALPHA = clamp(shape * clamp(fire_remaining, 0.0, 1.0) * flicker, 0.0, 1.0);
}

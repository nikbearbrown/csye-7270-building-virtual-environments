shader_type spatial;
render_mode unshaded;
uniform float activation : hint_range(0.0, 1.0) = 0.0;
uniform vec4 quiet_color : source_color = vec4(0.40, 0.16, 0.09, 1.0);
uniform vec4 active_color : source_color = vec4(0.12, 0.72, 0.52, 1.0);
uniform float stripe_count : hint_range(1.0, 16.0, 1.0) = 8.0;
void fragment() {
	float stripe = step(0.5, fract(UV.x * stripe_count));
	vec3 base = quiet_color.rgb * mix(0.65, 1.0, stripe);
	ALBEDO = mix(base, active_color.rgb, activation);
}

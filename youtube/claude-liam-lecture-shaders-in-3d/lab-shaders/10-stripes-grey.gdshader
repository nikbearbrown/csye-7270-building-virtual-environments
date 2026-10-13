shader_type spatial;
render_mode unshaded;

void fragment() {
	float stripe = step(0.5, fract(UV.x * 8.0));
	ALBEDO = vec3(0.3 + 0.6 * stripe);
}

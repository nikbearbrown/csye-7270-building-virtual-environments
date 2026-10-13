shader_type canvas_item;
// Calculator, not shown in the film: step with the arguments the "wrong" way round, step(radius, d): one OUTSIDE, zero inside.
void fragment() {
	float d = distance(UV, vec2(0.5));
	COLOR = vec4(0.37, 0.64, 0.57, step(0.3, d));
}

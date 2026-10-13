shader_type canvas_item;
float make_ring(float r) {
	float d = distance(UV, vec2(0.5));
	return step(d, r + 0.05) - step(d, r);
}
void fragment() {
	COLOR = vec4(0.37, 0.64, 0.57, make_ring(0.3));
}

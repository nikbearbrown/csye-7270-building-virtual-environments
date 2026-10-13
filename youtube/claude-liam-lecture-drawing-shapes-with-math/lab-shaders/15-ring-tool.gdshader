shader_type canvas_item;

float make_ring(vec2 uv, float r, float w) {
	float d = distance(uv, vec2(0.5));
	return step(d, r + w) - step(d, r);
}

void fragment() {
	float ring = make_ring(UV, 0.3, 0.05);
	COLOR = vec4(0.37, 0.64, 0.57, ring);
}

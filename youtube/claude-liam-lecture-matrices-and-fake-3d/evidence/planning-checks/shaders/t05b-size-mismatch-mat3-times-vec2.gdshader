shader_type canvas_item;

// EXPECTED TO FAIL TO COMPILE: a three-by-three table cannot multiply a two-number point.
void fragment() {
	vec2 bad = mat3(1.0) * vec2(1.0, 2.0);
	COLOR = vec4(bad, 0.0, 1.0);
}

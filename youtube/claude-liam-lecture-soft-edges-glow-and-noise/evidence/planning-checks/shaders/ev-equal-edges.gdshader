shader_type canvas_item;

// Evidence only (not shown on screen): smoothstep with EQUAL edges. The docs say "Results are undefined if a >= b."
void fragment() {
	float d = distance(UV, vec2(0.5));
	float body = 1.0 - smoothstep(0.4, 0.4, d);
	COLOR = vec4(0.37, 0.64, 0.57, body);
}

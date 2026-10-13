shader_type canvas_item;

// Evidence only (not shown on screen): smoothstep with REVERSED edges (a > b), written as people often write it.
void fragment() {
	float d = distance(UV, vec2(0.5));
	float body = smoothstep(0.4, 0.25, d);
	COLOR = vec4(0.37, 0.64, 0.57, body);
}

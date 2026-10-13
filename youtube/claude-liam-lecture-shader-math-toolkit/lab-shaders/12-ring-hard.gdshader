shader_type canvas_item;

void fragment() {
	float d = distance(UV, vec2(0.5));
	float ring = step(0.3, d) - step(0.38, d);
	COLOR = vec4(vec3(ring), 1.0);
}

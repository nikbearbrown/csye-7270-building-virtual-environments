shader_type canvas_item;

void fragment() {
	float d = distance(UV, vec2(0.5));
	float ring = step(0.3, d) - step(0.38, d);
	vec3 cream = vec3(0.98, 0.96, 0.92);
	vec3 teal = vec3(0.37, 0.64, 0.57);
	COLOR = vec4(mix(cream, teal, ring), 1.0);
}

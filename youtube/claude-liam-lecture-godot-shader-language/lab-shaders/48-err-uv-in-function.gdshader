shader_type canvas_item;

vec3 soften() {
	return 0.4 + 0.6 * vec3(UV, 0.5);
}

void fragment() {
	COLOR = vec4(soften(), 1.0);
}

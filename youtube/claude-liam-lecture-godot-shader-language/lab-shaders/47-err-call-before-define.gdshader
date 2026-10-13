shader_type canvas_item;

void fragment() {
	COLOR = vec4(soften(vec3(UV, 0.5)), 1.0);
}

vec3 soften(vec3 c) {
	return 0.4 + 0.6 * c;
}

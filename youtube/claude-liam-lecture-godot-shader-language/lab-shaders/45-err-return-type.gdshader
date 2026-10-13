shader_type canvas_item;

vec3 soften(vec3 c) {
	return vec4(0.4 + 0.6 * c, 1.0);
}

void fragment() {
	COLOR = vec4(soften(vec3(UV, 0.5)), 1.0);
}

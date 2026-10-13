shader_type canvas_item;

vec3 soften(vec3 c) {
	return 0.4 + 0.6 * c;
}

void fragment() {
	COLOR = vec4(soften(UV), 1.0);
}

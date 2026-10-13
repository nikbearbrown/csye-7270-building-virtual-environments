shader_type canvas_item;

vec3 soften(vec2 address) {
	return 0.4 + 0.6 * vec3(address, 0.5);
}

void fragment() {
	COLOR = vec4(soften(UV), 1.0);
}

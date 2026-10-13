shader_type canvas_item;

void fragment() {
	COLOR = vec4(
		0.4 + 0.6 * UV,
		0.7, 1.0);
}

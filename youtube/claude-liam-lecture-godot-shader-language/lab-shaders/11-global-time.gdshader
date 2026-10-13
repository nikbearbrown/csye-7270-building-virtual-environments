shader_type canvas_item;

float wave() {
	return 0.5 + 0.5 * sin(TIME);
}

void fragment() {
	COLOR = vec4(vec3(wave()), 1.0);
}

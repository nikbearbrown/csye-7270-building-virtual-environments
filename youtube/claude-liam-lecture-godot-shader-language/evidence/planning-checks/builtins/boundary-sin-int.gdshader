shader_type canvas_item;

void fragment() {
	float wave = sin(1);
	COLOR = vec4(vec3(wave), 1.0);
}

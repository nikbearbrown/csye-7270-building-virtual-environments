shader_type canvas_item;

void fragment() {
	float pulse = 0.5 + 0.5 * sin(TIME * 3.0);
	COLOR = vec4(1.0, pulse, 0.3, 1.0);
}

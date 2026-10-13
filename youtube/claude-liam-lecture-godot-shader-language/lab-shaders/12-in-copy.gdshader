shader_type canvas_item;

float bump(float x) {
	x = x + 0.5;
	return x;
}

void fragment() {
	float a = 0.25;
	float b = bump(a);
	COLOR = vec4(a, b, 0.0, 1.0);
}

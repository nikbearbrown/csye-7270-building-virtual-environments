shader_type canvas_item;

void bump(inout float x) {
	x += 0.5;
}

void fragment() {
	float a = 0.25;
	bump(a);
	COLOR = vec4(a, 0.0, 0.0, 1.0);
}

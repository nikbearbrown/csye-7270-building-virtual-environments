shader_type canvas_item;

vec4 f() {
	return COLOR;
}

void fragment() {
	COLOR = f();
}

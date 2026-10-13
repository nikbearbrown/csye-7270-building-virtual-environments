shader_type canvas_item;

vec4 f() {
	return FRAGCOORD / 1000.0;
}

void fragment() {
	COLOR = f();
}

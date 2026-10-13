shader_type canvas_item;

vec4 f() {
	return vec4(fract(TIME), 0.0, 0.0, 1.0);
}

void fragment() {
	COLOR = f();
}

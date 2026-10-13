shader_type canvas_item;

uniform float red : hint_range(0.0, 1.0) = 0.5;

void fragment() {
	COLOR = vec4(red, 0.45, 0.45, 1.0);
}

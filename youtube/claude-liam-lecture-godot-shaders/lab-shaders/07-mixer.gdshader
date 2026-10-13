shader_type canvas_item;

uniform float red : hint_range(0.0, 1.0) = 0.0;
uniform float green : hint_range(0.0, 1.0) = 0.0;
uniform float blue : hint_range(0.0, 1.0) = 0.0;

void fragment() {
	COLOR = vec4(red, green, blue, 1.0);
}

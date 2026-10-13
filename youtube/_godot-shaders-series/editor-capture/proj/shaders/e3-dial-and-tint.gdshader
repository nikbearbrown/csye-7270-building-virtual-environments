shader_type canvas_item;

uniform float red : hint_range(0.0, 1.0) = 0.5;
uniform vec4 tint : source_color = vec4(0.37, 0.64, 0.57, 1.0);

void fragment() {
	COLOR = vec4(red * tint.r, tint.g, tint.b, tint.a);
}

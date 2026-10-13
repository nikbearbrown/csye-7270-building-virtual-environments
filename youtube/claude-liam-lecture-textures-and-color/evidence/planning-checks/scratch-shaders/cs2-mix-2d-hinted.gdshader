shader_type canvas_item;

uniform vec4 a : source_color = vec4(0.2, 0.2, 0.2, 1.0);
uniform vec4 b : source_color = vec4(0.8, 0.8, 0.8, 1.0);
uniform float t = 0.5;

void fragment() {
	COLOR = mix(a, b, t);
}

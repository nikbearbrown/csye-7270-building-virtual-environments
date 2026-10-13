shader_type canvas_item;

uniform vec4 picked : source_color = vec4(0.2, 0.4, 0.6, 1.0);
uniform vec4 typed = vec4(0.2, 0.4, 0.6, 1.0);

void fragment() {
	COLOR = mix(picked, typed, 0.5);
}

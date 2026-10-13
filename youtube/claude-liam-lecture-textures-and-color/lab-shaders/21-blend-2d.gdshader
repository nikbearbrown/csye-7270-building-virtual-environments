shader_type canvas_item;

uniform vec4 from_color : source_color = vec4(0.2, 0.2, 0.2, 1.0);
uniform vec4 to_color : source_color = vec4(0.8, 0.8, 0.8, 1.0);

void fragment() {
	COLOR = mix(from_color, to_color, UV.x);
}

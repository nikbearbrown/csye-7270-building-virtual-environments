shader_type canvas_item;

uniform vec4 tint : source_color;

void fragment() {
	COLOR = tint;
}

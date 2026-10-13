shader_type canvas_item;

uniform sampler2D tex : filter_linear;

void fragment() {
	COLOR = texture(tex, UV);
}

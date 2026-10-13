shader_type canvas_item;

uniform sampler2D tex : filter_nearest;

void fragment() {
	COLOR = texture(tex, UV);
}

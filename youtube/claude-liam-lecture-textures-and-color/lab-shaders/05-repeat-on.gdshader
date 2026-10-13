shader_type canvas_item;

uniform sampler2D tex : filter_nearest, repeat_enable;

void fragment() {
	COLOR = texture(tex, UV * 2.0);
}

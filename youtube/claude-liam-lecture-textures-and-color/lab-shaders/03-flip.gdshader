shader_type canvas_item;

uniform sampler2D tex : filter_nearest;

void fragment() {
	vec2 address = vec2(1.0 - UV.x, UV.y);
	COLOR = texture(tex, address);
}

shader_type canvas_item;

uniform float look : hint_range(0.0, 0.5) = 0.1;

void fragment() {
	COLOR = texture(TEXTURE, UV + vec2(look, 0.0));
}

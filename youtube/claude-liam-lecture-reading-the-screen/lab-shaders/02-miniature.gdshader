shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture;

void fragment() {
	COLOR.rgb = texture(screen_texture, UV).rgb;
}

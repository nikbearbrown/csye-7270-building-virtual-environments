shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture;

void fragment() {
	vec3 behind = texture(screen_texture, SCREEN_UV).rgb;
	COLOR.rgb = 1.0 - behind;
}

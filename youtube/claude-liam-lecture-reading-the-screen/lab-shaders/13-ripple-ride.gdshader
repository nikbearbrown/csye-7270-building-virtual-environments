shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture;

void fragment() {
	float wave = sin(UV.y * 25.0);
	vec2 spot = SCREEN_UV + vec2(wave * 0.01, 0.0);
	COLOR.rgb = texture(screen_texture, spot).rgb;
}

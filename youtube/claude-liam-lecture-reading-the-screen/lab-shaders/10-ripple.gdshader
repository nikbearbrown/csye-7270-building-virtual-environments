shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture;
uniform float amount : hint_range(0.0, 0.05) = 0.01;

void fragment() {
	float wave = sin(SCREEN_UV.y * 60.0 + TIME * 4.0);
	vec2 spot = SCREEN_UV + vec2(wave * amount, 0.0);
	COLOR.rgb = texture(screen_texture, spot).rgb;
}

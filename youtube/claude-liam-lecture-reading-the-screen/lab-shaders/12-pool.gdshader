shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture;
uniform vec3 water : source_color = vec3(0.2, 0.5, 0.8);

void fragment() {
	if (UV.y < 0.1 + 0.03 * sin(UV.x * 30.0 + TIME * 2.0)) {
		discard;
	}
	float wave = sin(UV.y * 25.0 + TIME * 4.0);
	vec2 spot = SCREEN_UV + vec2(wave * 0.01, 0.0);
	vec3 behind = texture(screen_texture, spot).rgb;
	COLOR.rgb = mix(behind, water, 0.5);
}

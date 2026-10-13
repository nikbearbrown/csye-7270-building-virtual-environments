shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture;
uniform vec3 water : source_color = vec3(0.2, 0.5, 0.8);
uniform float amount : hint_range(0.0, 0.05) = 0.01;

void fragment() {
	float wave = sin(UV.y * 25.0 + TIME * 4.0);
	vec2 spot = SCREEN_UV + vec2(wave * amount, 0.0);
	vec3 behind = texture(screen_texture, spot).rgb;
	COLOR.rgb = mix(behind, water, 0.5);
}

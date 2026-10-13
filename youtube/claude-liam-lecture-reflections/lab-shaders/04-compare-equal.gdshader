shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture;

void fragment() {
	vec3 label = texture(screen_texture, SCREEN_UV).rgb;
	float water = float(label == vec3(0.5, 0.0, 0.0));
	COLOR.a *= water;
}

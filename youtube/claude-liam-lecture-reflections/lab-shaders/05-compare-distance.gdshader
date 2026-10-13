shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture;

void fragment() {
	vec3 label = texture(screen_texture, SCREEN_UV).rgb;
	float water = float(distance(label, vec3(0.5, 0.0, 0.0)) < 0.1);
	COLOR.a *= water;
}

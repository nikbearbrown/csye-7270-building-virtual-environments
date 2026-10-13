shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture;
const vec3 WATER = vec3(1.0, 0.0, 0.0);

void fragment() {
	vec3 label = texture(screen_texture, SCREEN_UV).rgb;
	float water = float(distance(label, WATER) < 0.1);
	COLOR.a *= water;
}

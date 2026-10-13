shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture;
uniform vec4 tint : source_color = vec4(0.2, 0.5, 1.0, 1.0);
const vec3 WATER = vec3(1.0, 0.0, 0.0);
const vec3 COAST = vec3(0.0, 1.0, 0.0);

void fragment() {
	vec3 label = texture(screen_texture, SCREEN_UV).rgb;
	float water = float(distance(label, WATER) < 0.1);
	float coast = float(distance(label, COAST) < 0.1);
	COLOR.a *= water * 0.5 + coast * 0.3;
	COLOR.rgb = mix(COLOR.rgb, tint.rgb, 0.5);
}

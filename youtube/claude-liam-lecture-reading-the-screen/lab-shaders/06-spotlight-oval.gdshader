shader_type canvas_item;
uniform sampler2D screen_texture : hint_screen_texture;
uniform vec2 player = vec2(0.5);
uniform float radius = 0.25;

void fragment() {
	vec3 c = texture(screen_texture, SCREEN_UV).rgb;
	if (distance(SCREEN_UV, player) > radius) {
		c = vec3(dot(c, vec3(0.299, 0.587, 0.114)));
	}
	COLOR.rgb = c;
}

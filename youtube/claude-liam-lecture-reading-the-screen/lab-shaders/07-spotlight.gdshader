shader_type canvas_item;
uniform sampler2D screen_texture : hint_screen_texture;
uniform vec2 player = vec2(0.5);
uniform float radius = 0.25;

void fragment() {
	vec3 c = texture(screen_texture, SCREEN_UV).rgb;
	vec2 px = SCREEN_PIXEL_SIZE;
	vec2 aspect = vec2(px.y / px.x, 1.0);
	if (distance(SCREEN_UV * aspect, player * aspect) > radius) {
		c = vec3(dot(c, vec3(0.299, 0.587, 0.114)));
	}
	COLOR.rgb = c;
}

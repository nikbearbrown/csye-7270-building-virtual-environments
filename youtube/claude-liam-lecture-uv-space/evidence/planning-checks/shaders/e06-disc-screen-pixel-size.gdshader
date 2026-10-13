shader_type canvas_item;

// the disc, with aspect taken from SCREEN_PIXEL_SIZE
void fragment() {
	float aspect = SCREEN_PIXEL_SIZE.y / SCREEN_PIXEL_SIZE.x;
	vec2 p = UV * 2.0 - 1.0;
	p.x *= aspect;
	vec4 col = vec4(0.0);
	if (length(p) < 0.8) col = vec4(0.37, 0.64, 0.57, 1.0);
	COLOR = col;
}

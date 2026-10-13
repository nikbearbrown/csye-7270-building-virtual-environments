shader_type canvas_item;
// check shader for the cost timing only: the loop outline of lab-shaders/08-loop.gdshader with a loop radius of 4 (constant bounds), so 9 x 9 = 81 reads plus one for the pixel's own colour
uniform vec4 line_color : source_color = vec4(0.25, 0.25, 0.75, 1.0);
uniform float thickness : hint_range(0.0, 8.0) = 1.0;
void fragment() {
	vec2 px = TEXTURE_PIXEL_SIZE * thickness;
	float around = 0.0;
	for (int y = -4; y <= 4; y++) {
		for (int x = -4; x <= 4; x++) {
			around += texture(TEXTURE, UV + vec2(float(x), float(y)) * px).a;
		}
	}
	vec4 color = texture(TEXTURE, UV);
	COLOR = mix(color, line_color, min(around, 1.0) * (1.0 - color.a));
}

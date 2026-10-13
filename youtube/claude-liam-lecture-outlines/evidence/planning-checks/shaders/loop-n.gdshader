shader_type canvas_item;
// check shader for the cost timing only: the loop outline with a loop radius r, so reads = (2r + 1)^2 plus one for the pixel's own colour
uniform vec4 line_color : source_color = vec4(0.25, 0.25, 0.75, 1.0);
uniform float thickness : hint_range(0.0, 8.0) = 1.0;
uniform int r = 1;

void fragment() {
	vec2 px = TEXTURE_PIXEL_SIZE * thickness;
	float around = 0.0;
	for (int y = -r; y <= r; y++) {
		for (int x = -r; x <= r; x++) {
			around += texture(TEXTURE, UV + vec2(float(x), float(y)) * px).a;
		}
	}
	vec4 color = texture(TEXTURE, UV);
	COLOR = mix(color, line_color, min(around, 1.0) * (1.0 - color.a));
}

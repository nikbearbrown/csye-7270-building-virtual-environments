shader_type canvas_item;
uniform vec4 line_color : source_color = vec4(0.25, 0.25, 0.75, 1.0);
uniform float thickness : hint_range(0.0, 8.0) = 1.0;

void fragment() {
	COLOR = texture(TEXTURE, UV);
	if (thickness > 0.0) {
		vec2 px = TEXTURE_PIXEL_SIZE * thickness;
		float around = 0.0;
		for (int y = -1; y <= 1; y++) {
			for (int x = -1; x <= 1; x++) {
				around += texture(TEXTURE, UV + vec2(float(x), float(y)) * px).a;
			}
		}
		COLOR = mix(COLOR, line_color, min(around, 1.0) * (1.0 - COLOR.a));
	}
}

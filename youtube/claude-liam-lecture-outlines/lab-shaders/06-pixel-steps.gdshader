shader_type canvas_item;
uniform vec4 line_color : source_color = vec4(0.25, 0.25, 0.75, 1.0);
uniform float thickness : hint_range(0.0, 8.0) = 1.0;

void fragment() {
	vec2 dx = vec2(TEXTURE_PIXEL_SIZE.x * thickness, 0.0);
	vec2 dy = vec2(0.0, TEXTURE_PIXEL_SIZE.y * thickness);
	vec4 color = texture(TEXTURE, UV);
	float around = texture(TEXTURE, UV + dx).a + texture(TEXTURE, UV - dx).a
		+ texture(TEXTURE, UV + dy).a + texture(TEXTURE, UV - dy).a;
	COLOR = mix(color, line_color, min(around, 1.0) * (1.0 - color.a));
}

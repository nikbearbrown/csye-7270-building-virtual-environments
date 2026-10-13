shader_type canvas_item;
uniform vec4 line_color : source_color = vec4(0.25, 0.25, 0.75, 1.0);

void fragment() {
	vec2 dx = vec2(0.02, 0.0);
	vec2 dy = vec2(0.0, 0.02);
	vec4 color = texture(TEXTURE, UV);
	float around = texture(TEXTURE, UV + dx).a + texture(TEXTURE, UV - dx).a
		+ texture(TEXTURE, UV + dy).a + texture(TEXTURE, UV - dy).a;
	COLOR = mix(color, line_color, min(around, 1.0) * (1.0 - color.a));
}

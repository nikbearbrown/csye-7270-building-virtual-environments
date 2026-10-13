shader_type canvas_item;
uniform vec4 line_color : source_color = vec4(0.25, 0.25, 0.75, 1.0);

void fragment() {
	vec2 dx = vec2(0.02, 0.0);
	vec4 color = texture(TEXTURE, UV);
	float around = texture(TEXTURE, UV + dx).a;
	COLOR = mix(color, line_color, around * (1.0 - color.a));
}

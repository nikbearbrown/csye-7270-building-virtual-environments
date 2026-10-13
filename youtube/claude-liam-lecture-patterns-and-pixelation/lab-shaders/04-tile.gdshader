shader_type canvas_item;

void fragment() {
	vec2 inside = fract(UV * 3.0);
	COLOR = texture(TEXTURE, inside);
}

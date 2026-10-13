shader_type canvas_item;

void fragment() {
	vec2 uv = UV;
	// bend uv here
	COLOR = texture(TEXTURE, uv);
}

shader_type canvas_item;

// scale the centered address by (-1, 1): left and right swap
void fragment() {
	vec2 uv = (UV - 0.5) * vec2(-1.0, 1.0) + 0.5;
	COLOR = texture(TEXTURE, uv);
}

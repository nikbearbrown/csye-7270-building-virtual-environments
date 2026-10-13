shader_type canvas_item;

void fragment() {
	vec2 uv = UV;
	uv.x += 0.03 * sin(TIME * 4.0 + UV.y * 24.0);
	COLOR = texture(TEXTURE, uv);
}

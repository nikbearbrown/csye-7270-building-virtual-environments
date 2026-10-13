shader_type canvas_item;
// check shader: red = TEXTURE_PIXEL_SIZE.x * 64, green = TEXTURE_PIXEL_SIZE.y * 64 (0.5 means one over 128)
void fragment() {
	COLOR = vec4(TEXTURE_PIXEL_SIZE.x * 64.0, TEXTURE_PIXEL_SIZE.y * 64.0, 0.0, 1.0);
}

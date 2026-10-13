shader_type canvas_item;

// reads the two pixel-size built-ins back as colours: red = SCREEN_PIXEL_SIZE.x * 200, green = SCREEN_PIXEL_SIZE.y * 200, blue = TEXTURE_PIXEL_SIZE.x * 0.2
void fragment() {
	COLOR = vec4(SCREEN_PIXEL_SIZE.x * 200.0, SCREEN_PIXEL_SIZE.y * 200.0, TEXTURE_PIXEL_SIZE.x * 0.2, 1.0);
}

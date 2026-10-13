shader_type canvas_item;

// Evidence only. R = (1 / TEXTURE_PIXEL_SIZE.x) / 256 and G = (1 / TEXTURE_PIXEL_SIZE.y) / 256 on a node WITH a texture
// (the Lab's 128 px sprite: expect 0.5, 0.5), and B = 1/TEXTURE_PIXEL_SIZE.x / 4 on a node WITHOUT one (a ColorRect: expect 0.25 if it is 1).
void fragment() {
	vec2 size = 1.0 / TEXTURE_PIXEL_SIZE;
	COLOR = vec4(size.x / 256.0, size.y / 256.0, size.x / 4.0, 1.0);
}

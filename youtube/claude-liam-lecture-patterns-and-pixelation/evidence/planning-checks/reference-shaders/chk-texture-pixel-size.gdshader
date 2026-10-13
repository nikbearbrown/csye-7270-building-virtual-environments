shader_type canvas_item;

// Evidence only. R = 1/(TEXTURE_PIXEL_SIZE.x * 256), G = 1/(TEXTURE_PIXEL_SIZE.y * 256).
// For the Lab's 128 px sprite texture the docs say TEXTURE_PIXEL_SIZE = (1/128, 1/128), so R = G = 0.5.
void fragment() {
	vec2 size = 1.0 / TEXTURE_PIXEL_SIZE;
	COLOR = vec4(size / 256.0, 0.0, 1.0);
}

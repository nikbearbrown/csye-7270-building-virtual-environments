shader_type canvas_item;

// Evidence only: a reference answer to the "Your turn" prompt. Dots along the SHORTER side = cells; the longer side gets
// proportionally more cells, so every cell is square and every dot is round, even on a wide texture.
uniform float cells : hint_range(4.0, 64.0) = 8.0;

void fragment() {
	vec2 size = 1.0 / TEXTURE_PIXEL_SIZE;
	vec2 grid = cells * size / min(size.x, size.y);
	vec2 p = UV * grid;
	vec2 middle = (floor(p) + 0.5) / grid;
	vec4 picture = texture(TEXTURE, middle);
	float d = length(fract(p) - 0.5);
	COLOR = vec4(picture.rgb, picture.a * (1.0 - step(0.4, d)));
}

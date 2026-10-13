shader_type canvas_item;

// Evidence only: the plausible WRONG answer. The cell number is rounded (floor(p + 0.5)), so each dot is centred on a grid line:
// the dots along the edges are cut in half. The picture lookup is the same as the reference otherwise.
uniform float cells : hint_range(4.0, 64.0) = 8.0;

void fragment() {
	vec2 size = 1.0 / TEXTURE_PIXEL_SIZE;
	vec2 grid = cells * size / min(size.x, size.y);
	vec2 p = UV * grid;
	vec2 id = floor(p + 0.5);
	vec4 picture = texture(TEXTURE, id / grid);
	float d = length(p - id);
	COLOR = vec4(picture.rgb, picture.a * (1.0 - step(0.4, d)));
}

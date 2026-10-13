shader_type canvas_item;

// Evidence only: the other plausible WRONG answer. The same count on both axes, so on a wide texture every cell is wide and
// every dot is an oval.
uniform float cells : hint_range(4.0, 64.0) = 8.0;

void fragment() {
	vec2 p = UV * cells;
	vec2 middle = (floor(p) + 0.5) / cells;
	vec4 picture = texture(TEXTURE, middle);
	float d = length(fract(p) - 0.5);
	COLOR = vec4(picture.rgb, picture.a * (1.0 - step(0.4, d)));
}

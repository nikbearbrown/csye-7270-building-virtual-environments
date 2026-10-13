shader_type canvas_item;
render_mode blend_premul_alpha;

uniform float count = 6.0;
uniform float width = 0.5;

void fragment() {
	float diagonal = UV.x + UV.y;
	float saw = fract(diagonal * count);
	float stripe = 1.0 - step(width, saw);
	COLOR = texture(TEXTURE, UV) * stripe;
}

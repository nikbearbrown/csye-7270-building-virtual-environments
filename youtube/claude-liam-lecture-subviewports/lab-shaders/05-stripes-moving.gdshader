shader_type canvas_item;
render_mode blend_premul_alpha;

uniform float count = 6.0;
uniform float width = 0.5;
uniform float speed = 0.12;

void fragment() {
	float diagonal = UV.x + UV.y - TIME * speed;
	float stripe = 1.0 - step(width, fract(diagonal * count));
	COLOR = texture(TEXTURE, UV) * stripe;
}

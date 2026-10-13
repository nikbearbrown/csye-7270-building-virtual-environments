shader_type canvas_item;
render_mode blend_premul_alpha;

void fragment() {
	float stripe = 1.0 - step(0.5, fract(UV.x * 8.0));
	COLOR = texture(TEXTURE, UV) * stripe;
}

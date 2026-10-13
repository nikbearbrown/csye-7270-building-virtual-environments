shader_type canvas_item;

void fragment() {
	float stripe = sin(UV.x * TAU * 6.0);
	COLOR.rgb *= 0.75 + 0.25 * stripe;
}

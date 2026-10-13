shader_type canvas_item;

varying float stripe;

void vertex() {
	stripe = sin(UV.x * TAU * 6.0);
}

void fragment() {
	COLOR.rgb *= 0.75 + 0.25 * stripe;
}

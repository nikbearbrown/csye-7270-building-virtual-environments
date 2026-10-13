shader_type canvas_item;

// Evidence only (not shown on screen): pow() with a NON-integer exponent on a negative base.
// Red = result is NaN, green = result is negative, blue = result is positive.
void fragment() {
	float x = UV.x * 2.0 - 1.0;
	float p = pow(x, 2.5);
	COLOR = vec4(isnan(p) ? 1.0 : 0.0, (p < 0.0) ? 1.0 : 0.0, (p > 0.0) ? 1.0 : 0.0, 1.0);
}

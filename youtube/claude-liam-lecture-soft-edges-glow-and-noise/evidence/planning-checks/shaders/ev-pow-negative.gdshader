shader_type canvas_item;

// Evidence only (not shown on screen): what pow() returns for a negative base on this machine.
// Red = result is NaN, green = result is negative, blue = result is positive.
void fragment() {
	float x = UV.x * 2.0 - 1.0;
	float p = pow(x, 3.0);
	COLOR = vec4(isnan(p) ? 1.0 : 0.0, (p < 0.0) ? 1.0 : 0.0, (p > 0.0) ? 1.0 : 0.0, 1.0);
}

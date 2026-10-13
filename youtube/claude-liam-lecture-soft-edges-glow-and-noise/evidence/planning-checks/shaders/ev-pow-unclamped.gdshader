shader_type canvas_item;

// Evidence only (not shown on screen): the spot WITHOUT the clamp, a fractional power, and a spot far in one corner so that
// 1.0 - distance goes negative in the opposite corner (distance beyond 1).
uniform float power = 2.5;

void fragment() {
	float spot = 1.0 - distance(UV, vec2(0.0));
	COLOR = vec4(0.37, 0.64, 0.57, pow(spot, power));
}

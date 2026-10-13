shader_type canvas_item;

// Evidence only (not shown on screen): the same spot WITH the clamp.
uniform float power = 2.5;

void fragment() {
	float spot = clamp(1.0 - distance(UV, vec2(0.0)), 0.0, 1.0);
	COLOR = vec4(0.37, 0.64, 0.57, pow(spot, power));
}

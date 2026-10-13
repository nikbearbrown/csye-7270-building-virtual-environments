shader_type canvas_item;

uniform float power : hint_range(1.0, 8.0) = 3.0;

void fragment() {
	float spot = clamp(1.0 - distance(UV, vec2(0.35)), 0.0, 1.0);
	COLOR = vec4(0.37, 0.64, 0.57, pow(spot, power));
}

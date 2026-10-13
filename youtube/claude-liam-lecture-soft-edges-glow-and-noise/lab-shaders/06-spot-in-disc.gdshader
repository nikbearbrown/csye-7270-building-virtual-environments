shader_type canvas_item;

void fragment() {
	float d = distance(UV, vec2(0.5));
	float disc = 1.0 - smoothstep(0.25, 0.4, d);
	float spot = clamp(1.0 - distance(UV, vec2(0.35)), 0.0, 1.0);
	COLOR = vec4(0.37, 0.64, 0.57, pow(spot, 3.0) * disc);
}

shader_type canvas_item;

void fragment() {
	float disc = step(distance(UV, vec2(0.5)), 0.3);
	float bite = step(distance(UV, vec2(0.8, 0.5)), 0.2);
	float spot = step(distance(UV, vec2(0.88, 0.5)), 0.08);
	float mask = disc - bite + spot;
	COLOR = vec4(0.37, 0.64, 0.57, mask);
}

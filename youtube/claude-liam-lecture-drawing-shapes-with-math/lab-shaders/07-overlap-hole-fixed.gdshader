shader_type canvas_item;

void fragment() {
	float a = step(distance(UV, vec2(0.38, 0.5)), 0.25);
	float b = step(distance(UV, vec2(0.62, 0.5)), 0.25);
	float hole = step(distance(UV, vec2(0.5)), 0.08);
	float mask = min(a + b, 1.0) - hole;
	COLOR = vec4(0.37, 0.64, 0.57, mask);
}

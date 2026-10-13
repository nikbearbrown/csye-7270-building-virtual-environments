shader_type canvas_item;
// Calculator, not shown in the film: |min(a + b, 1) - max(a, b)| for every pixel of the two-circle picture, drawn as red.
// Any red pixel is a disagreement between "add, then cap at one" and "take the max".
void fragment() {
	float a = step(distance(UV, vec2(0.38, 0.5)), 0.25);
	float b = step(distance(UV, vec2(0.62, 0.5)), 0.25);
	float capped = min(a + b, 1.0);
	float biggest = max(a, b);
	COLOR = vec4(abs(capped - biggest), 0.0, 0.0, 1.0);
}

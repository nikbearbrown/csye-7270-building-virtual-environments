shader_type canvas_item;
// Calculator, not shown in the film: distance(UV, vec2(0.5)) against distance(UV, vec2(0.5, 0.5)), red where they differ.
void fragment() {
	float a = distance(UV, vec2(0.5));
	float b = distance(UV, vec2(0.5, 0.5));
	COLOR = vec4(abs(a - b) > 0.0 ? 1.0 : 0.0, 0.0, 0.0, 1.0);
}

shader_type canvas_item;
// Calculator, not shown in the film: what does the screen do with a visibility (alpha) outside 0..1?
// Four columns: alpha 1.0, 2.0, 0.0, -1.0.
void fragment() {
	float a = UV.x < 0.25 ? 1.0 : (UV.x < 0.5 ? 2.0 : (UV.x < 0.75 ? 0.0 : -1.0));
	COLOR = vec4(0.37, 0.64, 0.57, a);
}

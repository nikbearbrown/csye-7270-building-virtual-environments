shader_type canvas_item;
// Calculator, not shown in the film: is COLOR (a fragment built-in) usable inside a user function? This is expected to FAIL.
void paint() {
	COLOR = vec4(0.37, 0.64, 0.57, 1.0);
}
void fragment() {
	paint();
}

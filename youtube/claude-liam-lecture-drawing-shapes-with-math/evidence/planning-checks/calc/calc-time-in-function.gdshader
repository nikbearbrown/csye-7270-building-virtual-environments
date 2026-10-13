shader_type canvas_item;
// Calculator, not shown in the film: is a GLOBAL built-in (TIME) usable inside a user function? (The docs say yes.) This must compile.
float pulse() {
	return 0.5 + 0.5 * sin(TIME);
}
void fragment() {
	COLOR = vec4(0.37, 0.64, 0.57, pulse());
}

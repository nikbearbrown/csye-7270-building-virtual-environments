shader_type canvas_item;

// Evidence only. What do fract and mod return for negative inputs?
// R = fract(-0.25)   (docs: x - floor(x) -> 0.75)
// G = mod(-1.0, 2.0) (docs: x - y*floor(x/y) -> 1.0)
// B = mod(-0.5, 1.0) (-> 0.5)
void fragment() {
	COLOR = vec4(fract(-0.25), mod(-1.0, 2.0), mod(-0.5, 1.0), 1.0);
}

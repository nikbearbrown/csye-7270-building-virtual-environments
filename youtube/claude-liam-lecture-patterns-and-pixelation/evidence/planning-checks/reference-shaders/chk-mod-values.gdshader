shader_type canvas_item;

// Evidence only. The remainders spoken in the film: three mod two is one; four mod two is zero; five mod two is one.
void fragment() {
	COLOR = vec4(mod(3.0, 2.0), mod(4.0, 2.0), mod(5.0, 2.0), 1.0);
}

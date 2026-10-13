shader_type canvas_item;

// Evidence only. The numbers spoken in the film: floor(2.9) = 2, fract(2.9) = 0.9, floor(0.7) = 0, fract(3.0) = 0.
// R = floor(2.9) / 4   (expect 0.5)
// G = fract(2.9)       (expect 0.9)
// B = floor(0.7) + fract(3.0)   (expect 0.0)
void fragment() {
	COLOR = vec4(floor(2.9) / 4.0, fract(2.9), floor(0.7) + fract(3.0), 1.0);
}

shader_type canvas_item;

// Evidence only. The worked example in the film: the pixel at address 0.6 with four blocks.
// R = 0.6 * 4 / 4        (2.4 / 4 = 0.6)
// G = floor(2.4) / 4     (2 / 4 = 0.5)
// B = (floor(2.4) + 0.5) / 4   (2.5 / 4 = 0.625: the middle of the third cell, which spans 0.5 to 0.75)
void fragment() {
	float scaled = 0.6 * 4.0;
	COLOR = vec4(scaled / 4.0, floor(scaled) / 4.0, (floor(scaled) + 0.5) / 4.0, 1.0);
}

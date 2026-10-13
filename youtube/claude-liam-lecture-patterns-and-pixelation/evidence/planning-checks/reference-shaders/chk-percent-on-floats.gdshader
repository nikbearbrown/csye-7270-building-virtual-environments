shader_type canvas_item;

// Evidence only. Does the percent operator work on floats in a shader? (Expected: a compile error.)
void fragment() {
	float a = 5.0 % 2.0;
	COLOR = vec4(a, 0.0, 0.0, 1.0);
}

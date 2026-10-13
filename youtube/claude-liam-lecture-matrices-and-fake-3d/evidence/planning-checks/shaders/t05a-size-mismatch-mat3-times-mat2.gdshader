shader_type canvas_item;

// EXPECTED TO FAIL TO COMPILE: two tables of different sizes cannot be multiplied.
void fragment() {
	mat3 bad = mat3(1.0) * mat2(1.0);
	COLOR = vec4(bad[0], 1.0);
}

shader_type canvas_item;

// Unit tests for how Godot reads a matrix. Row k of the picture is green when check k is true, red when it is false.
// Rows 10 and 11 are NEGATIVE CONTROLS: they are deliberately false and must be red.
bool check(int k) {
	mat2 m = mat2(vec2(1.0, 2.0), vec2(3.0, 4.0));
	vec2 p = vec2(5.0, 6.0);
	if (k == 0) return m * p == vec2(23.0, 34.0);          // the hand calculation
	if (k == 1) return m[0] == vec2(1.0, 2.0);             // m[0] is the first COLUMN
	if (k == 2) return m[1][0] == 3.0;                     // m[column][row]
	if (k == 3) return p * m == vec2(17.0, 39.0);          // point on the left: the table is read the other way round
	if (k == 4) return transpose(m) * p == vec2(17.0, 39.0);   // the table read as ROWS gives the same wrong answer
	if (k == 5) return mat2(1.0) * p == p;                 // mat2(1.0) is the identity
	if (k == 6) return mat2(1.0) == mat2(vec2(1.0, 0.0), vec2(0.0, 1.0));   // ... and it IS the table one, zero, zero, one
	if (k == 7) return mat2(vec2(2.0, 0.0), vec2(0.0, 2.0)) * p == vec2(10.0, 12.0);
	if (k == 8) return 5.0 * m[0] + 6.0 * m[1] == vec2(23.0, 34.0);   // the column view: five of the first column plus six of the second
	if (k == 9) return mat3(mat2(vec2(0.0, 1.0), vec2(-1.0, 0.0))) == mat3(vec3(0.0, 1.0, 0.0), vec3(-1.0, 0.0, 0.0), vec3(0.0, 0.0, 1.0));   // mat3 of a mat2 pads with the identity
	if (k == 10) return m * p == vec2(17.0, 39.0);         // CONTROL: must be false
	if (k == 11) return p * m == vec2(23.0, 34.0);         // CONTROL: must be false
	return false;
}

void fragment() {
	int k = int(floor(UV.y * 12.0));
	COLOR = check(k) ? vec4(0.0, 1.0, 0.0, 1.0) : vec4(1.0, 0.0, 0.0, 1.0);
}

shader_type canvas_item;

// Do PI, TAU, E and radians() exist in a canvas item shader, with the right values? Row k is green when check k is true.
// Row 7 is a NEGATIVE CONTROL (TAU is not 3): it must be red.
bool check(int k) {
	if (k == 0) return abs(TAU - 6.28318530718) < 0.00001;
	if (k == 1) return abs(PI - 3.14159265359) < 0.00001;
	if (k == 2) return abs(TAU - 2.0 * PI) < 0.00001;
	if (k == 3) return abs(radians(180.0) - PI) < 0.00001;
	if (k == 4) return abs(cos(TAU / 4.0)) < 0.00001;     // a quarter turn: cosine is zero
	if (k == 5) return abs(sin(TAU / 4.0) - 1.0) < 0.00001;
	if (k == 6) return abs(E - 2.718281828) < 0.00001;
	if (k == 7) return abs(TAU - 3.0) < 0.00001;          // CONTROL: must be false
	return false;
}

void fragment() {
	int k = int(floor(UV.y * 8.0));
	COLOR = check(k) ? vec4(0.0, 1.0, 0.0, 1.0) : vec4(1.0, 0.0, 0.0, 1.0);
}

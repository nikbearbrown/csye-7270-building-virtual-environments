shader_type canvas_item;

// Evidence only (not shown on screen). Are PI, TAU and E built in, and does radians() agree with PI?
// R: PI is within 1e-5 of 3.14159265; G: TAU is within 1e-5 of 6.28318531; B: E within 1e-5 of 2.71828183 -> 1.0 when true, 0.0 when false.
// The right half repeats the test for radians(45.0) == PI / 4.0 (green) and degrees(PI) == 180.0 (blue), red = TAU == 2.0 * PI.
void fragment() {
	bool pi_ok = abs(PI - 3.14159265) < 0.00001;
	bool tau_ok = abs(TAU - 6.28318531) < 0.00001;
	bool e_ok = abs(E - 2.71828183) < 0.00001;
	bool rad_ok = abs(radians(45.0) - PI / 4.0) < 0.00001;
	bool deg_ok = abs(degrees(PI) - 180.0) < 0.001;
	bool tau2_ok = abs(TAU - 2.0 * PI) < 0.00001;
	if (UV.x < 0.5) {
		COLOR = vec4(pi_ok ? 1.0 : 0.0, tau_ok ? 1.0 : 0.0, e_ok ? 1.0 : 0.0, 1.0);
	} else {
		COLOR = vec4(tau2_ok ? 1.0 : 0.0, rad_ok ? 1.0 : 0.0, deg_ok ? 1.0 : 0.0, 1.0);
	}
}

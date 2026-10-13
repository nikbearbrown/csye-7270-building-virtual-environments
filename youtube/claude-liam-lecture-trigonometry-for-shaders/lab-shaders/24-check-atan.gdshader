shader_type canvas_item;

// Evidence only (not shown on screen): the pixel's angle three ways, as numbers in the red, green and blue channels.
// R = atan(p.y, p.x) / TAU + 0.5            (seam at the left, 0 just above the left axis, 1 just below)
// G = fract(atan(p.y, p.x) / TAU + 0.25)    (seam at the top)
// B = atan(p.y, p.x) / (2.0 * PI) + 0.5     (same as R written with PI: they must agree)
void fragment() {
	vec2 p = UV * 2.0 - 1.0;
	float ang = atan(p.y, p.x);
	COLOR = vec4(ang / TAU + 0.5, fract(ang / TAU + 0.25), ang / (2.0 * PI) + 0.5, 1.0);
}

shader_type canvas_item;

// Evidence only (not shown on screen): 12-flower without time, with the petal count as a uniform, so edge radii can be probed exactly.
uniform float petals = 8.0;

void fragment() {
	vec2 p = UV * 2.0 - 1.0;
	float a = atan(p.y, p.x);
	float edge = 0.55 + 0.15 * cos(petals * a);
	if (length(p) < edge) {
		COLOR = vec4(0.37, 0.64, 0.57, 1.0);
	} else {
		COLOR = vec4(0.85, 0.84, 0.79, 1.0);
	}
}

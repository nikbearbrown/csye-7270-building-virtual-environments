shader_type canvas_item;

void fragment() {
	vec2 p = UV * 2.0 - 1.0;
	float a = atan(p.y, p.x);
	float edge = 0.55 + 0.15 * cos(8.0 * (a - TIME));
	if (length(p) < edge) {
		COLOR = vec4(0.37, 0.64, 0.57, 1.0);
	} else {
		COLOR = vec4(0.85, 0.84, 0.79, 1.0);
	}
}

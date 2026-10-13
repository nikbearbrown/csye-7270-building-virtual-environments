shader_type canvas_item;

uniform float eye_x = 0.3;

void fragment() {
	vec2 p = UV * 2.0 - 1.0;
	p.x = abs(p.x);
	vec4 col = vec4(0.0);
	if (length(p) < 0.8) col = vec4(0.37, 0.64, 0.57, 1.0);
	if (length(p - vec2(eye_x, -0.15)) < 0.12) col = vec4(1.0);
	COLOR = col;
}

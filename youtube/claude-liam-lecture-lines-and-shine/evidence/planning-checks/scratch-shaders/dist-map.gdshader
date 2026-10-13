shader_type canvas_item;
// Scratch evidence shader (not shown on screen): the test value v, the true distance d, or the raw |v| as a grey level, so a Lab probe can read it.
// what = 0: v / 2 + 0.5 | what = 1: d = |v| / sqrt(1 + slope * slope) | what = 2: |v|
uniform float slope = 0.5;
uniform int what = 1;
void fragment() {
	vec2 p = UV * 2.0 - 1.0;
	p.y = -p.y;
	float v = p.y - slope * p.x;
	float shown = v * 0.5 + 0.5;
	if (what == 1) { shown = abs(v) / sqrt(1.0 + slope * slope); }
	if (what == 2) { shown = abs(v); }
	COLOR = vec4(vec3(shown), 1.0);
}

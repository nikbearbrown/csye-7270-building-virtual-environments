shader_type spatial;
render_mode unshaded;

uniform float cell_density = 8.0;
uniform float cell_speed = 0.8;
uniform float show = 0.0;

vec2 hash22(vec2 p) {
	p = vec2(dot(p, vec2(127.1, 311.7)), dot(p, vec2(269.5, 183.3)));
	return fract(sin(p) * 43758.5453);
}

// x: distance to the nearest cell point, y: to the second nearest
vec2 cells(vec2 p, float t) {
	vec2 i = floor(p);
	vec2 f = fract(p);
	vec2 d = vec2(8.0);
	for (int y = -1; y <= 1; y++) {
		for (int x = -1; x <= 1; x++) {
			vec2 g = vec2(float(x), float(y));
			vec2 o = 0.5 + 0.5 * sin(t + TAU * hash22(i + g));
			float r = length(g + o - f);
			if (r < d.x) { d.y = d.x; d.x = r; } else if (r < d.y) { d.y = r; }
		}
	}
	return d;
}

void fragment() {
	vec2 p = UV * cell_density;
	vec2 c = cells(p, TIME * cell_speed);
	vec2 g = fract(p);
	float v = 1.0 - smoothstep(0.09, 0.13, c.x);
	if (show > 0.5) v = c.x;
	if (show > 1.5) v = c.y - c.x;
	float grid = step(min(g.x, g.y), 0.012) * step(show, 0.5);
	vec3 pale = vec3(0.93, 0.91, 0.85);
	vec3 deep = vec3(0.12, 0.38, 0.52);
	ALBEDO = mix(mix(pale, deep, v), vec3(0.45, 0.47, 0.50), grid);
}

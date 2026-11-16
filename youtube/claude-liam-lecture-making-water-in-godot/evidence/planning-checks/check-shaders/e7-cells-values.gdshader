shader_type spatial;
render_mode unshaded;
// E7: the film's cells() with a search reach (1 = the 3x3 block the film uses, 2 = 5x5), writing numbers into the red and green channels.
// red = nearest distance / 2, green = (second nearest - nearest) / 2, blue = the film's foam mask for edge_width.
uniform float cell_density = 8.0;
uniform float cell_speed = 0.8;
uniform float edge_width = 0.1;
uniform float reach = 1.0;

vec2 hash22(vec2 p) {
	p = vec2(dot(p, vec2(127.1, 311.7)), dot(p, vec2(269.5, 183.3)));
	return fract(sin(p) * 43758.5453);
}

vec2 cells(vec2 p, float t) {
	vec2 i = floor(p);
	vec2 f = fract(p);
	vec2 d = vec2(8.0);
	for (int y = -2; y <= 2; y++) {
		for (int x = -2; x <= 2; x++) {
			if (abs(float(x)) > reach || abs(float(y)) > reach) { continue; }
			vec2 g = vec2(float(x), float(y));
			vec2 o = 0.5 + 0.5 * sin(t + TAU * hash22(i + g));
			float r = length(g + o - f);
			if (r < d.x) { d.y = d.x; d.x = r; } else if (r < d.y) { d.y = r; }
		}
	}
	return d;
}

void fragment() {
	vec2 c = cells(UV * cell_density, TIME * cell_speed);
	float foam = 1.0 - smoothstep(0.0, edge_width, c.y - c.x);
	ALBEDO = vec3(c.x / 2.0, (c.y - c.x) / 2.0, foam);
}

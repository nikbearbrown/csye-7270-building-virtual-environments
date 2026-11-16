shader_type spatial;
render_mode unshaded;
// E9b (the film's final form: the clock is a uniform the script sets, so there is no TIME offset to fit): the film's wave() and vertex(), but the fragment writes the vertex-stage height h as a colour (green = 0.5 + h * 2): lets a script compare the GPU's height with the CPU's.
uniform float wave_height : hint_range(0.0, 0.4) = 0.12;
uniform float wave_length : hint_range(0.5, 8.0) = 3.0;
uniform float wave_speed : hint_range(0.0, 3.0) = 0.8;
uniform float wave_clock = 0.0;
varying float vh;

// x: height of the surface, y and z: its slope along x and along z
vec3 wave(vec2 p, float t) {
	vec2 d1 = normalize(vec2(1.0, 0.3));
	vec2 d2 = normalize(vec2(-0.4, 1.0));
	float k1 = TAU / wave_length;
	float k2 = TAU / (0.6 * wave_length);
	float p1 = k1 * (dot(d1, p) - wave_speed * t);
	float p2 = k2 * (dot(d2, p) - 0.8 * wave_speed * t);
	float h = wave_height * (sin(p1) + 0.6 * sin(p2));
	vec2 s = wave_height * (k1 * cos(p1) * d1 + 0.6 * k2 * cos(p2) * d2);
	return vec3(h, s);
}

void vertex() {
	vec3 w = wave(VERTEX.xz, wave_clock);
	VERTEX.y += w.x;
	vh = w.x;
}

void fragment() {
	ALBEDO = vec3(0.5 + vh * 2.0);
}

shader_type spatial;
render_mode blend_mix, depth_draw_opaque, cull_back;

uniform vec3 water_color : source_color = vec3(0.10, 0.45, 0.70);
uniform vec3 foam_color : source_color = vec3(0.92, 0.97, 1.0);
uniform float roughness : hint_range(0.0, 1.0) = 0.15;
uniform float opacity : hint_range(0.0, 1.0) = 0.7;
uniform float cell_density : hint_range(1.0, 40.0) = 10.0;
uniform float cell_speed : hint_range(0.0, 4.0) = 0.8;
uniform float sharpness : hint_range(1.0, 12.0) = 5.0;
uniform float clamped = 0.0;

vec2 hash22(vec2 p) {
	p = vec2(dot(p, vec2(127.1, 311.7)), dot(p, vec2(269.5, 183.3)));
	return fract(sin(p) * 43758.5453);
}

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
	vec2 c = cells(UV * cell_density, TIME * cell_speed);
	float glow = pow(1.0 - c.x, sharpness);
	if (clamped > 0.5) glow = pow(clamp(1.0 - c.x, 0.0, 1.0), sharpness);
	ALBEDO = mix(water_color, foam_color, glow);
	ALPHA = mix(opacity, 1.0, glow);
	ROUGHNESS = roughness;
}

shader_type spatial;
render_mode blend_mix, depth_draw_opaque, cull_back;

group_uniforms Color;
uniform vec3 water_color : source_color = vec3(0.10, 0.45, 0.70);
uniform float roughness : hint_range(0.0, 1.0) = 0.15;
group_uniforms Clarity;
uniform float opacity : hint_range(0.0, 1.0) = 0.7;
group_uniforms Foam;
uniform vec3 foam_color : source_color = vec3(0.92, 0.97, 1.0);
uniform float foam_roughness : hint_range(0.0, 1.0) = 0.9;
uniform float cell_density : hint_range(1.0, 40.0) = 10.0;
uniform float cell_speed : hint_range(0.0, 4.0) = 0.8;
uniform float edge_width : hint_range(0.01, 0.5) = 0.1;
group_uniforms Ripples;
uniform sampler2D normal_a : hint_normal, filter_linear_mipmap, repeat_enable;
uniform sampler2D normal_b : hint_normal, filter_linear_mipmap, repeat_enable;
uniform float ripple_scale : hint_range(0.5, 8.0) = 3.0;
uniform float ripple_speed : hint_range(0.0, 0.2) = 0.03;
uniform float ripple_strength : hint_range(0.0, 2.0) = 0.8;
uniform float warp_strength : hint_range(0.0, 1.0) = 0.15;
group_uniforms Waves;
uniform float wave_height : hint_range(0.0, 0.4) = 0.12;
uniform float wave_length : hint_range(0.5, 8.0) = 3.0;
uniform float wave_speed : hint_range(0.0, 3.0) = 0.8;
uniform float wave_clock = 0.0;
group_uniforms Shore;
uniform sampler2D depth_tex : hint_depth_texture, repeat_disable, filter_nearest;
uniform float shore_width : hint_range(0.05, 1.5) = 0.5;
group_uniforms;

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
	NORMAL = normalize(vec3(-w.y, 1.0, -w.z));
}

// distance from the camera to the opaque scene behind this pixel
float scene_depth(vec2 screen_uv, mat4 inv_projection) {
	float depth = texture(depth_tex, screen_uv).x;
#if CURRENT_RENDERER == RENDERER_COMPATIBILITY
	vec3 ndc = vec3(screen_uv, depth) * 2.0 - 1.0;
#else
	vec3 ndc = vec3(screen_uv * 2.0 - 1.0, depth);
#endif
	vec4 view = inv_projection * vec4(ndc, 1.0);
	return -view.z / view.w;
}

void fragment() {
	vec2 uv_a = UV * ripple_scale + vec2(1.0, 0.4) * TIME * ripple_speed;
	vec2 uv_b = UV * ripple_scale * 0.7 - vec2(0.3, 1.0) * TIME * ripple_speed * 1.3;
	vec3 n = mix(texture(normal_a, uv_a).rgb, texture(normal_b, uv_b).rgb, 0.5);
	vec2 warp = (n.xy - 0.5) * warp_strength;
	vec2 c = cells((UV + warp) * cell_density, TIME * cell_speed);
	float foam = 1.0 - smoothstep(0.0, edge_width, c.y - c.x);
	float reach = shore_width * (0.3 + 0.7 * c.x);
	float gap = scene_depth(SCREEN_UV, INV_PROJECTION_MATRIX) + VERTEX.z;
	float shore = 1.0 - smoothstep(0.5 * reach, reach, gap);
	foam = max(foam, shore);
	ALBEDO = mix(water_color, foam_color, foam);
	ALPHA = mix(opacity, 1.0, foam);
	ROUGHNESS = mix(roughness, foam_roughness, foam);
	NORMAL_MAP = n;
	NORMAL_MAP_DEPTH = ripple_strength;
}

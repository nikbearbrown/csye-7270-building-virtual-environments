shader_type canvas_item;

uniform float dot_size : hint_range(0, 1) = 0.5;
uniform float ring_distance : hint_range(0, 1) = 0.55;
uniform float ring_width : hint_range(0, 1) = 0.3;
uniform float arm_gap : hint_range(0, 1) = 0.35;
uniform float arm_length : hint_range(0, 1) = 0.6;
uniform float arm_width : hint_range(0, 1) = 0.4;

float make_dot(vec2 uv, float r) {
	return step(distance(uv, vec2(0.5)), r);
}

float make_ring(vec2 uv, float r, float w) {
	float d = distance(uv, vec2(0.5));
	return step(d, r + w) - step(d, r);
}

float make_arms(vec2 uv, float gap, float len, float w) {
	float x = abs(uv.x - 0.5);
	float y = abs(uv.y - 0.5);
	float end = gap + len;
	float h = step(gap, x) * step(x, end) * step(y, w);
	float v = step(gap, y) * step(y, end) * step(x, w);
	return max(h, v);
}

void fragment() {
	float dot_r = dot_size * 0.05;
	float ring_r = ring_distance * 0.4;
	float ring_w = ring_width * 0.05;
	float gap = arm_gap * 0.2;
	float len = arm_length * 0.3;
	float w = arm_width * 0.03;
	float mask = make_dot(UV, dot_r);
	mask = max(mask, make_ring(UV, ring_r, ring_w));
	mask = max(mask, make_arms(UV, gap, len, w));
	COLOR = vec4(0.37, 0.64, 0.57, mask);
}

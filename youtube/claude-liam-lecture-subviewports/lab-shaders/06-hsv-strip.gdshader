shader_type canvas_item;

float plateau(float x) {
	return clamp(abs(fract(x) * 6.0 - 3.0) - 1.0, 0.0, 1.0);
}

vec3 hsv_to_rgb(float h, float s, float v) {
	float r = plateau(h);
	float g = plateau(h + 2.0 / 3.0);
	float b = plateau(h + 1.0 / 3.0);
	return v * mix(vec3(1.0), vec3(r, g, b), s);
}

void fragment() {
	COLOR = vec4(hsv_to_rgb(UV.x, 1.0, 1.0), 1.0);
}

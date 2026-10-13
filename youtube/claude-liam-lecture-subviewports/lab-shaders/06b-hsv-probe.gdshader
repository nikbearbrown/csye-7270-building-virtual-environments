shader_type canvas_item;

// Verification copy of 06-hsv-strip.gdshader: the same two functions, hue/saturation/value from uniforms instead of UV.x.
uniform float hue = 0.0;
uniform float saturation = 1.0;
uniform float value = 1.0;

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
	COLOR = vec4(hsv_to_rgb(hue, saturation, value), 1.0);
}

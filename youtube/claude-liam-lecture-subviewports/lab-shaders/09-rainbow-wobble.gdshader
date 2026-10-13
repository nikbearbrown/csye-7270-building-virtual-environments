shader_type canvas_item;
render_mode blend_premul_alpha;

uniform float count = 6.0;
uniform float width = 0.5;
uniform float speed = 0.12;
uniform float amplitude = 16.0;
uniform float frequency = 10.0;
uniform float wobble_speed = 3.0;

float plateau(float x) {
	return clamp(abs(fract(x) * 6.0 - 3.0) - 1.0, 0.0, 1.0);
}

vec3 hsv_to_rgb(float h, float s, float v) {
	float r = plateau(h);
	float g = plateau(h + 2.0 / 3.0);
	float b = plateau(h + 1.0 / 3.0);
	return v * mix(vec3(1.0), vec3(r, g, b), s);
}

void vertex() {
	VERTEX.y += sin(UV.x * frequency + TIME * wobble_speed) * amplitude;
}

void fragment() {
	vec4 picture = texture(TEXTURE, UV);
	float diagonal = UV.x + UV.y - TIME * speed;
	float stripe = 1.0 - step(width, fract(diagonal * count));
	vec4 band = vec4(hsv_to_rgb(diagonal, 1.0, 1.0), 1.0) * picture.a;
	COLOR = mix(picture, band, stripe);
}

shader_type canvas_item;

uniform sampler2D noise_tex;
uniform float threshold : hint_range(0.0, 1.0) = 0.5;

void fragment() {
	float n = texture(noise_tex, UV).r;
	COLOR.a = step(threshold, n);
}

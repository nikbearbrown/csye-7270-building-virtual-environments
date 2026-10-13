shader_type canvas_item;

uniform sampler2D noise_tex;
uniform float progress : hint_range(0.0, 1.0) = 0.0;

void fragment() {
	float n = texture(noise_tex, UV).r;
	if (n < progress) {
		discard;
	}
}

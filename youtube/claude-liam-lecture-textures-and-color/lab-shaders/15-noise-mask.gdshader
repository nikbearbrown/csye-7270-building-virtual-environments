shader_type canvas_item;

uniform sampler2D noise_tex;

void fragment() {
	COLOR.a = texture(noise_tex, UV).r;
}

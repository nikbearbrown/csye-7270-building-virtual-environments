shader_type canvas_item;

uniform sampler2D noise_tex;

void fragment() {
	float n = texture(noise_tex, UV).r;
	COLOR = vec4(vec3(n), 1.0);
}

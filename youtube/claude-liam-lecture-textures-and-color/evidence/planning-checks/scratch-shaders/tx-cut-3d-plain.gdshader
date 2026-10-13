shader_type spatial;
render_mode unshaded;

uniform sampler2D tex;

void fragment() {
	ALBEDO = vec3(step(0.5, texture(tex, UV).r));
}

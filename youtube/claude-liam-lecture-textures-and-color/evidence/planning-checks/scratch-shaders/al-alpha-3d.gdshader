shader_type spatial;
render_mode unshaded;

uniform vec4 a : source_color = vec4(0.0, 0.0, 0.0, 0.5);

void fragment() {
	ALBEDO = vec3(a.a);
}

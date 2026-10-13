shader_type spatial;
render_mode unshaded;

uniform vec4 a : source_color = vec4(0.2, 0.4, 0.6, 1.0);

void fragment() {
	ALBEDO = a.rgb;
}

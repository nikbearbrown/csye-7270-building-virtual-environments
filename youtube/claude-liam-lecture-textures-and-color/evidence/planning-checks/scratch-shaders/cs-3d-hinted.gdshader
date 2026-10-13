shader_type spatial;
render_mode unshaded;

uniform vec4 a : source_color = vec4(0.0, 0.0, 0.0, 1.0);
uniform vec4 b : source_color = vec4(1.0, 1.0, 1.0, 1.0);

void fragment() {
	ALBEDO = mix(a.rgb, b.rgb, UV.x);
}

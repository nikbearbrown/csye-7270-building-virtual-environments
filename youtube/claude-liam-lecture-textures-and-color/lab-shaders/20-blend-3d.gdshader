shader_type spatial;
render_mode unshaded;

uniform vec4 from_color : source_color = vec4(0.2, 0.2, 0.2, 1.0);
uniform vec4 to_color : source_color = vec4(0.8, 0.8, 0.8, 1.0);

void fragment() {
	ALBEDO = mix(from_color.rgb, to_color.rgb, UV.x);
}

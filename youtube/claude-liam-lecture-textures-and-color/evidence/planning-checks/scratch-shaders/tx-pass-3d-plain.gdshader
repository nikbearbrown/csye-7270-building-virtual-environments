shader_type spatial;
render_mode unshaded;

uniform sampler2D tex;

void fragment() {
	ALBEDO = texture(tex, UV).rgb;
}

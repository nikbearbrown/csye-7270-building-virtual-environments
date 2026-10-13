shader_type spatial;
render_mode unshaded;

uniform sampler2D picture;

void fragment() {
	ALBEDO = texture(picture, UV).rgb;
}

shader_type spatial;
render_mode unshaded;

uniform sampler2D source_color_tex : source_color, filter_nearest;
uniform sampler2D plain_tex : filter_nearest;
uniform bool use_source_color = false;

void fragment() {
	if (use_source_color) {
		ALBEDO = texture(source_color_tex, UV).rgb;
	} else {
		ALBEDO = texture(plain_tex, UV).rgb;
	}
}

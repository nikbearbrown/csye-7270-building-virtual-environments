shader_type spatial;
render_mode unshaded;

uniform sampler2D source_color_tex : source_color, filter_nearest;
uniform sampler2D raw_data_tex : filter_nearest;

uniform bool use_source_color = true;

void fragment() {
	if (use_source_color) {
		ALBEDO = texture(source_color_tex, UV).rgb;
	} else {
		ALBEDO = texture(raw_data_tex, UV).rgb;
	}
}
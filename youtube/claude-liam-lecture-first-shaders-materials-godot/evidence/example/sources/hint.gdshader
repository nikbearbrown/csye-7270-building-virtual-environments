shader_type spatial;
render_mode unshaded;
uniform sampler2D as_color : source_color, filter_nearest;
uniform sampler2D as_data : filter_nearest;
uniform bool use_color = true;
// Optional screen-coordinate ruler; off during color measurements.
uniform bool show_screen_grid = false;
void fragment() {
	ALBEDO = use_color ? texture(as_color, UV).rgb : texture(as_data, UV).rgb;
	if (show_screen_grid && mod(FRAGCOORD.x, VIEWPORT_SIZE.x / 8.0) < 2.0) {
		ALBEDO = vec3(1.0, 0.0, 0.0);
	}
}

shader_type spatial;
render_mode unshaded;

void fragment() {
	if (OUTPUT_IS_SRGB) {
		ALBEDO = vec3(1.0, 0.0, 0.0);
	} else {
		ALBEDO = vec3(0.0, 0.0, 1.0);
	}
}

shader_type spatial;
render_mode unshaded;
float helper() {
	mat4 x = INV_PROJECTION_MATRIX;
	return 1.0;
}
void fragment() {
	ALBEDO = vec3(helper());
}

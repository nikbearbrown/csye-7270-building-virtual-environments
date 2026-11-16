shader_type spatial;
render_mode unshaded;
float helper() {
	float x = TAU;
	return 1.0;
}
void fragment() {
	ALBEDO = vec3(helper());
}

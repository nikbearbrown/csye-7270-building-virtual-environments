shader_type spatial;
render_mode unshaded;
float helper() {
	vec3 x = VERTEX;
	return 1.0;
}
void fragment() {
	ALBEDO = vec3(helper());
}

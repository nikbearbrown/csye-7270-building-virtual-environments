shader_type spatial;
render_mode unshaded;
float helper() {
	vec2 x = UV;
	return 1.0;
}
void fragment() {
	ALBEDO = vec3(helper());
}

shader_type spatial;
render_mode unshaded;
float helper() {
	vec2 x = SCREEN_UV;
	return 1.0;
}
void fragment() {
	ALBEDO = vec3(helper());
}

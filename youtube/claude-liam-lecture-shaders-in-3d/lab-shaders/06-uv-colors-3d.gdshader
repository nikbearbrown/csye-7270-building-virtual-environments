shader_type spatial;
render_mode unshaded;

void fragment() {
	ALBEDO = vec3(UV.x, UV.y, 0.0);
}

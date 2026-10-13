shader_type canvas_item;

vec3 soften(vec3 c) {
	return 0.4 + 0.6 * c;
}

void fragment() {
	vec3 c = soften(vec3(UV, 0.5));
	COLOR = vec4(c, 1.0);
}

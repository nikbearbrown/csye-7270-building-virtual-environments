shader_type canvas_item;

vec3 soften(vec3 c) {
	vec3 softer = 0.4 + 0.6 * c;
}

void fragment() {
	COLOR = vec4(soften(vec3(UV, 0.5)), 1.0);
}

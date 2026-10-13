shader_type canvas_item;

void fragment() {
	vec3 c = vec3(0.2, 0.3, 0.4) * vec3(2.0, 1.0, 0.5);
	COLOR = vec4(c, 1.0);
}

shader_type canvas_item;

void fragment() {
	vec3 v = vec3(4, 5, 6) + 2;
	COLOR = vec4(v / 10.0, 1.0);
}

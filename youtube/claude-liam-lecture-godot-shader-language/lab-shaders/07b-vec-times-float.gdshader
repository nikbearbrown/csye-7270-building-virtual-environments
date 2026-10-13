shader_type canvas_item;

void fragment() {
	vec3 c = vec3(0.2, 0.3, 0.4) * 2.0;
	COLOR = vec4(c, 1.0);
}

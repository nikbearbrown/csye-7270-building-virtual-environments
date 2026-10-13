shader_type canvas_item;

void make(out vec3 c) {
	c = vec3(0.1, 0.5, 0.9);
}

void fragment() {
	vec3 c;
	make(c);
	COLOR = vec4(c, 1.0);
}

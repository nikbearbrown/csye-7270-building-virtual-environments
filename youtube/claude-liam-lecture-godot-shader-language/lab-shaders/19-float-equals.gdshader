shader_type canvas_item;

void fragment() {
	vec3 c = vec3(0.95);
	if (UV.x == 0.5) {
		c = vec3(0.37, 0.64, 0.57);
	}
	COLOR = vec4(c, 1.0);
}

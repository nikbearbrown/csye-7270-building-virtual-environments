shader_type canvas_item;

void fragment() {
	vec3 c = vec3(0.95);
	for (int i = 0; i < 5; i++) {
		float y = 0.1 + 0.2 * i;
		if (abs(UV.y - y) < 0.03) {
			c = vec3(0.37, 0.64, 0.57);
		}
	}
	COLOR = vec4(c, 1.0);
}

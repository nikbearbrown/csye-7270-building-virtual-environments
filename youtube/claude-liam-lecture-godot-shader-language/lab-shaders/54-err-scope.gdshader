shader_type canvas_item;

void fragment() {
	if (UV.x < 0.5) {
		vec3 c = vec3(0.37, 0.64, 0.57);
	} else {
		vec3 c = vec3(0.95);
	}
	COLOR = vec4(c, 1.0);
}

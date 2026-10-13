shader_type canvas_item;

void fragment() {
	vec3 c = vec3(0.2);
	if (UV.x) {
		c = vec3(0.8);
	}
	COLOR = vec4(c, 1.0);
}

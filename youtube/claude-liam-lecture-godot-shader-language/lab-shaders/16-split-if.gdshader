shader_type canvas_item;

void fragment() {
	vec3 teal = vec3(0.37, 0.64, 0.57);
	vec3 pale = vec3(0.95);
	vec3 c;
	if (UV.x < 0.5) {
		c = teal;
	} else {
		c = pale;
	}
	COLOR = vec4(c, 1.0);
}

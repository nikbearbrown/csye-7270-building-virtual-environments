shader_type canvas_item;

uniform float a = 0.1;
uniform float b = 0.2;

void fragment() {
	vec3 c = vec3(0.95);
	if (a + b == 0.3) {
		c = vec3(0.37, 0.64, 0.57);
	}
	COLOR = vec4(c, 1.0);
}

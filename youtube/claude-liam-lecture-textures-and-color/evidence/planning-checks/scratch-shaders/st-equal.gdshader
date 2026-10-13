shader_type canvas_item;

uniform float x = 0.5;

void fragment() {
	COLOR = vec4(vec3(step(0.5, x)), 1.0);
}

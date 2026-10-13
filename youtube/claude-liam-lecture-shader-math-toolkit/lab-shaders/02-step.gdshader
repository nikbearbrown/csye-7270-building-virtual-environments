shader_type canvas_item;

uniform float edge = 0.5;

void fragment() {
	float v = step(edge, UV.x);
	COLOR = vec4(vec3(v), 1.0);
}

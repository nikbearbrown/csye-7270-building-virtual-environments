shader_type canvas_item;

uniform float angle = 30.0;

void fragment() {
	vec2 p = UV * 2.0 - 1.0;
	p.y = -p.y;
	float m = tan(angle);
	float v = p.y - m * p.x;
	COLOR = vec4(0.65 + 0.2 * v, 0.65, 0.65 - 0.2 * v, 1.0);
}

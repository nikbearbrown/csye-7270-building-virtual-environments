shader_type canvas_item;

uniform float slope = 0.5;

void fragment() {
	vec2 p = UV * 2.0 - 1.0;
	p.y = -p.y;
	float v = p.y - slope * p.x;
	COLOR = vec4(0.65 + 0.2 * v, 0.65, 0.65 - 0.2 * v, 1.0);
}

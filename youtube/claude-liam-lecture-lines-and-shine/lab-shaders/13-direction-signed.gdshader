shader_type canvas_item;

uniform float angle = 35.0;

void fragment() {
	vec2 p = UV * 2.0 - 1.0;
	p.y = -p.y;
	float a = radians(angle);
	vec2 n = vec2(-sin(a), cos(a));
	float v = dot(p, n);
	COLOR = vec4(0.65 + 0.2 * v, 0.65, 0.65 - 0.2 * v, 1.0);
}

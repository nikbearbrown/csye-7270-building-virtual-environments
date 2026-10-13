shader_type canvas_item;

uniform float angle = 35.0;
uniform float thickness = 0.1;
uniform vec2 center = vec2(0.0);

void fragment() {
	vec2 p = UV * 2.0 - 1.0;
	p.y = -p.y;
	vec2 q = p - center;
	float m = tan(radians(angle));
	float d = abs(q.y - m * q.x) / sqrt(1.0 + m * m);
	COLOR = vec4(vec3(0.5 + 0.5 * step(d, thickness)), 1.0);
}

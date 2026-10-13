shader_type canvas_item;

uniform float angle = 45.0;
uniform float thickness = 0.1;

void fragment() {
	vec2 p = UV * 2.0 - 1.0;
	p.y = -p.y;
	float m = tan(radians(angle));
	float d = abs(p.y - m * p.x) / sqrt(1.0 + m * m);
	COLOR = vec4(vec3(0.5 + 0.5 * step(d, thickness)), 1.0);
}

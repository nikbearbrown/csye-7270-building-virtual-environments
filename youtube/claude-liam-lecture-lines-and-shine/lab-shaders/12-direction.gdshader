shader_type canvas_item;

uniform float angle = 35.0;
uniform float thickness = 0.1;

void fragment() {
	vec2 p = UV * 2.0 - 1.0;
	p.y = -p.y;
	float a = radians(angle);
	vec2 n = vec2(-sin(a), cos(a));
	float d = abs(dot(p, n));
	COLOR = vec4(vec3(0.5 + 0.5 * step(d, thickness)), 1.0);
}

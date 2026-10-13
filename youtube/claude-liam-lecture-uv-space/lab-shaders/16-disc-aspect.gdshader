shader_type canvas_item;

uniform float aspect = 1.7778;
uniform float radius = 0.8;

void fragment() {
	vec2 p = UV * 2.0 - 1.0;
	p.x *= aspect;
	vec4 col = vec4(0.0);
	if (length(p) < radius) col = vec4(0.37, 0.64, 0.57, 1.0);
	COLOR = col;
}

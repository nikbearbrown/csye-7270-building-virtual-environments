shader_type canvas_item;

void fragment() {
	vec2 p = UV * 2.0 - 1.0;
	float t = atan(p.y / p.x) / PI + 0.5;
	vec3 teal = vec3(0.37, 0.64, 0.57);
	vec3 amber = vec3(0.9, 0.65, 0.25);
	COLOR = vec4(mix(teal, amber, t), 1.0);
}

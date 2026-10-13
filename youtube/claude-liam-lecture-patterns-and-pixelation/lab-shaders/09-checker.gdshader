shader_type canvas_item;

void fragment() {
	vec2 cell = floor(UV * 8.0);
	float parity = mod(cell.x + cell.y, 2.0);
	vec3 teal = vec3(0.373, 0.639, 0.569);
	vec3 cream = vec3(0.980, 0.976, 0.961);
	COLOR = vec4(mix(teal, cream, parity), 1.0);
}

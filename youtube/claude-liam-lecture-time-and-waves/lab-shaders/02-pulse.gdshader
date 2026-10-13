shader_type canvas_item;

void fragment() {
	float pulse = 0.5 + 0.5 * sin(TAU * TIME);
	vec3 teal = vec3(0.37, 0.64, 0.57);
	vec3 cream = vec3(0.98, 0.97, 0.96);
	COLOR = vec4(mix(teal, cream, pulse), 1.0);
}

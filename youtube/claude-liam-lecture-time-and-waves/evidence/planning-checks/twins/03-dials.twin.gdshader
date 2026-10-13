shader_type canvas_item;
uniform float tv = 0.0;

uniform float amplitude : hint_range(0.0, 0.5) = 0.5;
uniform float speed = 0.5;
uniform float offset = 0.0;

void fragment() {
	float cycles = tv * speed + offset;
	float pulse = 0.5 + amplitude * sin(TAU * cycles);
	vec3 teal = vec3(0.37, 0.64, 0.57);
	vec3 cream = vec3(0.98, 0.97, 0.96);
	COLOR = vec4(mix(teal, cream, pulse), 1.0);
}

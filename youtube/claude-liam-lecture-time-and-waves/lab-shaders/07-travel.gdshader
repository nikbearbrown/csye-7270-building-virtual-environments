shader_type canvas_item;

uniform float frequency = 3.0;
uniform float speed = 0.5;

void fragment() {
	float cycles = (UV.x - TIME * speed) * frequency;
	float wave = 0.5 + 0.5 * sin(TAU * cycles);
	vec3 teal = vec3(0.37, 0.64, 0.57);
	vec3 cream = vec3(0.98, 0.97, 0.96);
	COLOR = vec4(mix(teal, cream, wave), 1.0);
}

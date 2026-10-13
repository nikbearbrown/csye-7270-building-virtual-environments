shader_type canvas_item;

uniform float cells = 8.0;
uniform float radius = 0.35;

void fragment() {
	vec2 inside = fract(UV * cells) - 0.5;
	float d = length(inside);
	float outside = step(radius, d);
	vec3 teal = vec3(0.373, 0.639, 0.569);
	vec3 cream = vec3(0.980, 0.976, 0.961);
	COLOR = vec4(mix(teal, cream, outside), 1.0);
}

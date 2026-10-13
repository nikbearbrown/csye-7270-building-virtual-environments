shader_type canvas_item;

uniform float radius = 0.3;

void fragment() {
	float d = distance(UV, vec2(0.5));
	float inner = smoothstep(radius - 0.04, radius, d);
	float outer = smoothstep(radius + 0.08, radius + 0.12, d);
	vec3 cream = vec3(0.98, 0.96, 0.92);
	vec3 teal = vec3(0.37, 0.64, 0.57);
	COLOR = vec4(mix(cream, teal, inner - outer), 1.0);
}

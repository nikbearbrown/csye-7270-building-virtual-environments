shader_type canvas_item;

void fragment() {
	float d = distance(UV, vec2(0.5));
	float inner = smoothstep(0.26, 0.30, d);
	float outer = smoothstep(0.38, 0.42, d);
	vec3 cream = vec3(0.98, 0.96, 0.92);
	vec3 teal = vec3(0.37, 0.64, 0.57);
	COLOR = vec4(mix(cream, teal, inner - outer), 1.0);
}

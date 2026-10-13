shader_type canvas_item;

void fragment() {
	float d = distance(UV, vec2(0.5));
	float glow = 1.0 - smoothstep(0.0, 0.5, d);
	COLOR = vec4(vec3(glow), 1.0);
}

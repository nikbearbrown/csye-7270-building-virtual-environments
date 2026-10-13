shader_type canvas_item;

void fragment() {
	float d = distance(UV, vec2(0.5));
	COLOR = vec4(vec3(step(d, 0.3)), 1.0);
}

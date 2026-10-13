shader_type canvas_item;

void fragment() {
	float d = distance(UV, vec2(0.5));
	COLOR = vec4(vec3(d), 1.0);
}

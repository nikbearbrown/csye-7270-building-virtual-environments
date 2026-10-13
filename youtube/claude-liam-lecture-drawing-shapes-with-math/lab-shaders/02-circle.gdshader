shader_type canvas_item;

void fragment() {
	float d = distance(UV, vec2(0.5));
	float inside = step(d, 0.3);
	COLOR = vec4(0.37, 0.64, 0.57, inside);
}

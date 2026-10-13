shader_type canvas_item;

void fragment() {
	float d = distance(UV, vec2(0.5));
	float outer = step(d, 0.35);
	float inner = step(d, 0.3);
	COLOR = vec4(0.37, 0.64, 0.57, outer - inner);
}

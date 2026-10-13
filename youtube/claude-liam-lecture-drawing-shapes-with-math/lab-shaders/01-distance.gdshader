shader_type canvas_item;

void fragment() {
	float d = distance(UV, vec2(0.5));
	COLOR = vec4(0.37, 0.64, 0.57, d);
}

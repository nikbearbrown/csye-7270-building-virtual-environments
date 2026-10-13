shader_type canvas_item;

void fragment() {
	float d = distance(UV, vec2(0.5));
	float body = 1.0 - step(0.4, d);
	COLOR = vec4(0.37, 0.64, 0.57, body);
}

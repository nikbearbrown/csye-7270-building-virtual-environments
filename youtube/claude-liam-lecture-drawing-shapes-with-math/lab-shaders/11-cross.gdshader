shader_type canvas_item;

void fragment() {
	float x = abs(UV.x - 0.5);
	float y = abs(UV.y - 0.5);
	float vertical = step(x, 0.05);
	float horizontal = step(y, 0.05);
	float mask = max(vertical, horizontal);
	COLOR = vec4(0.37, 0.64, 0.57, mask);
}

shader_type canvas_item;

void fragment() {
	float x = abs(UV.x - 0.5);
	float y = abs(UV.y - 0.5);
	float far_enough = step(0.1, y);
	float not_too_far = step(y, 0.35);
	float near_line = step(x, 0.03);
	float mask = far_enough * not_too_far * near_line;
	COLOR = vec4(0.37, 0.64, 0.57, mask);
}

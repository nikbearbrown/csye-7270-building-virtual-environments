shader_type canvas_item;

void fragment() {
	float x = abs(UV.x - 0.5);
	float y = abs(UV.y - 0.5);
	float far_enough = step(0.1, x);
	float not_too_far = step(x, 0.35);
	float thin = step(y, 0.02);
	float mask = far_enough * not_too_far * thin;
	COLOR = vec4(0.37, 0.64, 0.57, mask);
}

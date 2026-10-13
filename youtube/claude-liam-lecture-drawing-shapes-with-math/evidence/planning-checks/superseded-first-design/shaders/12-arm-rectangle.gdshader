shader_type canvas_item;

void fragment() {
	float x = abs(UV.x - 0.5);
	float y = abs(UV.y - 0.5);
	float near_line = step(x, 0.03);
	float in_reach = step(y, 0.3);
	float mask = near_line * in_reach;
	COLOR = vec4(0.37, 0.64, 0.57, mask);
}

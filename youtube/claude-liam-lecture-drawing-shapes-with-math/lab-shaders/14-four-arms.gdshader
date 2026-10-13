shader_type canvas_item;

void fragment() {
	float x = abs(UV.x - 0.5);
	float y = abs(UV.y - 0.5);
	float v = step(0.1, y) * step(y, 0.35) * step(x, 0.03);
	float h = step(0.1, x) * step(x, 0.35) * step(y, 0.03);
	float mask = max(v, h);
	COLOR = vec4(0.37, 0.64, 0.57, mask);
}

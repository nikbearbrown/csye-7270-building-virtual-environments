shader_type canvas_item;

void fragment() {
	float slot = floor((1.0 - UV.y) * 16.0);
	bool lit = TIME >= (slot + 1.0) * 0.25;
	COLOR = lit ? vec4(0.37, 0.64, 0.57, 1.0) : vec4(0.88, 0.88, 0.88, 1.0);
}

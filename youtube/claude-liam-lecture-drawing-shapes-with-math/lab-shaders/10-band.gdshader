shader_type canvas_item;

void fragment() {
	float across = abs(UV.x - 0.5);
	float band = step(across, 0.05);
	COLOR = vec4(0.37, 0.64, 0.57, band);
}

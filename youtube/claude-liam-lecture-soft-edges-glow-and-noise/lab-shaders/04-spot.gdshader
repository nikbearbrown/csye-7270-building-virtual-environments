shader_type canvas_item;

void fragment() {
	float spot = 1.0 - distance(UV, vec2(0.35));
	COLOR = vec4(0.37, 0.64, 0.57, spot);
}

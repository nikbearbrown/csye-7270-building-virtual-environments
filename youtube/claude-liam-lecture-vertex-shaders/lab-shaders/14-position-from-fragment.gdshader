shader_type canvas_item;

void fragment() {
	float across = VERTEX.x / 1280.0;
	COLOR = vec4(across, 0.4, 1.0 - across, 1.0);
}

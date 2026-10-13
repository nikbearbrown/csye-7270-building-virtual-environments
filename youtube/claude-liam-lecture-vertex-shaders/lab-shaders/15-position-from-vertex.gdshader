shader_type canvas_item;

varying float across;

void vertex() {
	across = VERTEX.x / 128.0 + 0.5;
}

void fragment() {
	COLOR = vec4(across, 0.4, 1.0 - across, 1.0);
}

shader_type canvas_item;

void vertex() {
	VERTEX.x += 50.0 * step(0.5, UV.y);
}

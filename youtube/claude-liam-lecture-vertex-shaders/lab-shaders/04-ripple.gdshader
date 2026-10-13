shader_type canvas_item;

void vertex() {
	VERTEX.y += sin(UV.x * 8.0) * 24.0;
}

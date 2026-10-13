// Verification shader (not shown on screen): c2-flag-draft.
shader_type canvas_item;

void vertex() {
	VERTEX.y += sin(UV.x * 9.0 - TIME * 3.0) * 14.0 * UV.x;
}

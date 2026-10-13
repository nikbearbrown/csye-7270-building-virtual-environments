shader_type canvas_item;

// Evidence only (not shown on screen): the "pulse" idea, VERTEX += normalize(VERTEX) * amount, on a node whose origin is its centre
// (Sprite2D, centred) and on one whose origin is its corner (ColorRect). Left out of the film; kept as a note for a vertex-stage film.
void vertex() {
	VERTEX += normalize(VERTEX) * 30.0;
}

void fragment() {
	COLOR = vec4(0.37, 0.64, 0.57, 1.0);
}

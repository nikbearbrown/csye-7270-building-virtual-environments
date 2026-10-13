// Verification shader (not shown on screen): halve the vertex COLOR.
shader_type canvas_item;

void vertex() {
	COLOR.rgb *= 0.5;
}

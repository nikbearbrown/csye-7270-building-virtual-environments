// Verification shader (not shown on screen): is a UV changed in vertex() what fragment() receives?
// vertex() halves the horizontal address, so if it passes through, the red channel reaches only 0.5 at the right edge.
shader_type canvas_item;

void vertex() {
	UV = vec2(UV.x * 0.5, UV.y);
}

void fragment() {
	COLOR = vec4(UV.x, UV.y, 0.0, 1.0);
}

// Verification shader (not shown on screen): the flow runs one way. A varying set in fragment() and read in vertex().
shader_type canvas_item;

varying float v;

void vertex() {
	VERTEX.x += v;
}

void fragment() {
	v = 1.0;
	COLOR = vec4(v);
}

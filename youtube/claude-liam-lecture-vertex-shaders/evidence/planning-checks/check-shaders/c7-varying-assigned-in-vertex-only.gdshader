// Verification shader (not shown on screen): control for c6. The normal direction (assign in vertex(), read in fragment()) compiles.
shader_type canvas_item;

varying float v;

void vertex() {
	v = 0.5;
}

void fragment() {
	COLOR = vec4(v);
}

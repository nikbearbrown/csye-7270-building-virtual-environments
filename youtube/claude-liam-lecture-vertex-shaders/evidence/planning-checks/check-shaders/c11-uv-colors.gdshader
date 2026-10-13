// Verification shader (not shown on screen): UV as colour (red = UV.x, green = UV.y), to see what a node delivers.
shader_type canvas_item;

void fragment() {
	COLOR = vec4(UV.x, UV.y, 0.0, 1.0);
}

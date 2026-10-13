shader_type canvas_item;
// Calculator, not shown in the film: UV as colour (red = UV.x, green = UV.y), to read the corners of a wide view.
void fragment() {
	COLOR = vec4(UV.x, UV.y, 0.0, 1.0);
}

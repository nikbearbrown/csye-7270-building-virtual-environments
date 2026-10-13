shader_type canvas_item;
// check shader: paints UV.x in red and UV.y in green so the range a node's UV covers can be read from pixels
void fragment() {
	COLOR = vec4(UV.x, UV.y, 0.0, 1.0);
}

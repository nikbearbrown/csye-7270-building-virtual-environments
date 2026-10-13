shader_type canvas_item;
// check shader: paints one component of REGION_RECT (chosen by the mask) as grey, so the value can be read from a pixel
uniform vec4 mask = vec4(1.0, 0.0, 0.0, 0.0);
void fragment() {
	COLOR = vec4(vec3(dot(REGION_RECT, mask)), 1.0);
}

shader_type canvas_item;
// Calculator, not shown in the film: UV handed to a user function as an argument. This must compile.
float edge_distance(vec2 uv) {
	return abs(uv.x - 0.5);
}
void fragment() {
	COLOR = vec4(0.37, 0.64, 0.57, step(edge_distance(UV), 0.1));
}

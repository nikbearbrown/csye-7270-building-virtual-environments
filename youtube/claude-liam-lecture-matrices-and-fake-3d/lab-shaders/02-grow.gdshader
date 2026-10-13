shader_type canvas_item;

uniform float grow : hint_range(0.1, 2.0) = 1.0;

void vertex() {
	mat2 scale_table = mat2(vec2(grow, 0.0), vec2(0.0, grow));
	VERTEX = scale_table * VERTEX;
}

shader_type canvas_item;

void fragment() {
	mat2 table = mat2(vec2(1.0, 2.0), vec2(3.0, 4.0));
	vec2 moved = table * vec2(5.0, 6.0);
	if (moved == vec2(23.0, 34.0)) {
		COLOR = vec4(0.37, 0.64, 0.57, 1.0);
	} else {
		COLOR = vec4(0.85, 0.2, 0.2, 1.0);
	}
}

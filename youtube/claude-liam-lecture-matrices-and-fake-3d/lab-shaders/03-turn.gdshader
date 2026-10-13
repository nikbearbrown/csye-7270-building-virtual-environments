shader_type canvas_item;

uniform float angle : hint_range(0.0, 6.2832) = 0.0;

void vertex() {
	vec2 across = vec2(cos(angle), sin(angle));
	vec2 down = vec2(-sin(angle), cos(angle));
	VERTEX = mat2(across, down) * VERTEX;
}

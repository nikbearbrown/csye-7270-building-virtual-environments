shader_type canvas_item;

// red = |centered x|: the left half reads like the right half
void fragment() {
	vec2 p = UV * 2.0 - 1.0;
	COLOR = vec4(abs(p.x), 0.0, 0.5, 1.0);
}

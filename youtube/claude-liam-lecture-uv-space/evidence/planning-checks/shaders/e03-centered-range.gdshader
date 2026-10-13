shader_type canvas_item;

// |centered address|: 0 in the middle, 1 at the edge midpoints and corners
void fragment() {
	vec2 p = UV * 2.0 - 1.0;
	COLOR = vec4(abs(p), 0.5, 1.0);
}

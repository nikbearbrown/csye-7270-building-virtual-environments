shader_type canvas_item;

void fragment() {
	vec2 p = UV * 4.0;
	vec2 inside = fract(p);
	COLOR = vec4(0.2 + inside * 0.7, 0.55, 1.0);
}

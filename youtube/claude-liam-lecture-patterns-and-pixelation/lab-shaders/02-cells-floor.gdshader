shader_type canvas_item;

void fragment() {
	vec2 p = UV * 4.0;
	vec2 cell = floor(p);
	COLOR = vec4(0.25 + cell * 0.25, 0.55, 1.0);
}

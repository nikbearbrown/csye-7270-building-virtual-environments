shader_type canvas_item;

// grey = length of the centered address / 1.5
void fragment() {
	vec2 p = UV * 2.0 - 1.0;
	COLOR = vec4(vec3(length(p) / 1.5), 1.0);
}

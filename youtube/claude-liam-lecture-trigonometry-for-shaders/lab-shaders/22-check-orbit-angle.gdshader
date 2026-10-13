shader_type canvas_item;

// Evidence only (not shown on screen): 01-moon-fixed with the angle as a uniform, so the Lab can place the moon at exact angles.
uniform float angle = 0.0;

void fragment() {
	vec2 p = UV * 2.0 - 1.0;
	vec2 moon = 0.6 * vec2(cos(angle), sin(angle));
	vec3 col = vec3(0.85, 0.84, 0.79);
	if (length(p) < 0.25) col = vec3(0.37, 0.64, 0.57);
	if (distance(p, moon) < 0.08) col = vec3(0.5, 0.6, 0.75);
	COLOR = vec4(col, 1.0);
}

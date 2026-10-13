shader_type canvas_item;

void fragment() {
	vec2 p = UV * 2.0 - 1.0;
	float a = TIME;
	float b = -TIME * 3.0;
	vec2 moon = 0.6 * vec2(cos(a), sin(a));
	vec2 meteor = moon + 0.2 * vec2(cos(b), sin(b));
	vec3 col = vec3(0.85, 0.84, 0.79);
	if (length(p) < 0.25) col = vec3(0.37, 0.64, 0.57);
	if (distance(p, moon) < 0.08) col = vec3(0.5, 0.6, 0.75);
	if (distance(p, meteor) < 0.04) col = vec3(0.9, 0.65, 0.25);
	COLOR = vec4(col, 1.0);
}

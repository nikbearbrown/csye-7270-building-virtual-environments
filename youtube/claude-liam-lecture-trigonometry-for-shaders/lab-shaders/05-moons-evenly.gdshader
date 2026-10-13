shader_type canvas_item;

void fragment() {
	vec2 p = UV * 2.0 - 1.0;
	vec3 col = vec3(0.85, 0.84, 0.79);
	if (length(p) < 0.25) col = vec3(0.37, 0.64, 0.57);
	for (int i = 0; i < 3; i++) {
		float a = TIME + float(i) * TAU / 3.0;
		vec2 moon = 0.6 * vec2(cos(a), sin(a));
		if (distance(p, moon) < 0.08) col = vec3(0.5, 0.6, 0.75);
	}
	COLOR = vec4(col, 1.0);
}

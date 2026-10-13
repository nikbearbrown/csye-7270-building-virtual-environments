shader_type canvas_item;

void fragment() {
	int k = min(int(floor(UV.x * 5.0)), 4);
	vec2 p = vec2(0.0);
	if (k == 0) { p = vec2(0.9, 0.5); } else if (k == 1) { p = vec2(0.5, 0.2); } else if (k == 2) { p = vec2(0.15, 0.85); } else if (k == 3) { p = vec2(0.95, 0.95); } else if (k == 4) { p = vec2(0.55, 0.55); }
	COLOR = vec4(vec3(distance(p, vec2(0.5))), 1.0);
}

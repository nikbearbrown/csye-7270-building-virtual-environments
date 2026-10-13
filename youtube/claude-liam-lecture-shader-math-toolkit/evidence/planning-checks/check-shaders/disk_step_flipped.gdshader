shader_type canvas_item;

void fragment() {
	int k = min(int(floor(UV.x * 5.0)), 4);
	float x = 0.0;
	if (k == 0) { x = 0.2; } else if (k == 1) { x = 0.3; } else if (k == 2) { x = 0.34; } else if (k == 3) { x = 0.38; } else if (k == 4) { x = 0.45; }
	float v = step(x, 0.3);
	COLOR = vec4(vec3(v * 1.0 + 0.0), 1.0);
}

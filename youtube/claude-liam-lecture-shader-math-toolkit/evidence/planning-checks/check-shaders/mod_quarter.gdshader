shader_type canvas_item;

void fragment() {
	int k = min(int(floor(UV.x * 5.0)), 4);
	float x = 0.0;
	if (k == 0) { x = 0.1; } else if (k == 1) { x = 0.3; } else if (k == 2) { x = 0.6; } else if (k == 3) { x = 0.9; } else if (k == 4) { x = 1.0; }
	float v = mod(x, 0.25);
	COLOR = vec4(vec3(v * 4.0 + 0.0), 1.0);
}

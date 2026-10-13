shader_type canvas_item;

void fragment() {
	int k = min(int(floor(UV.x * 5.0)), 4);
	float x = 0.0;
	if (k == 0) { x = 0.75; } else if (k == 1) { x = 0.75; } else if (k == 2) { x = 0.75; } else if (k == 3) { x = 0.75; } else if (k == 4) { x = 0.75; }
	float v = sin(x * 6.28318530718) + 1.0;
	COLOR = vec4(vec3(v * 0.5 + 0.0), 1.0);
}

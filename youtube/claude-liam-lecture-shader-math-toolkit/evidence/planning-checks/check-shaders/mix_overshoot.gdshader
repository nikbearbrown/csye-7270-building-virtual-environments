shader_type canvas_item;

void fragment() {
	int k = min(int(floor(UV.x * 5.0)), 4);
	float x = 0.0;
	if (k == 0) { x = -1.0; } else if (k == 1) { x = 0.0; } else if (k == 2) { x = 1.0; } else if (k == 3) { x = 2.0; } else if (k == 4) { x = 3.0; }
	float v = mix(0.2, 0.9, x);
	COLOR = vec4(vec3(v * 0.25 + 0.25), 1.0);
}

shader_type canvas_item;

void fragment() {
	int k = min(int(floor(UV.x * 5.0)), 4);
	float x = 0.0;
	if (k == 0) { x = -1.0; } else if (k == 1) { x = 0.0; } else if (k == 2) { x = 0.5; } else if (k == 3) { x = 1.0; } else if (k == 4) { x = 2.0; }
	float v = mix(0.2, 0.4, x);
	COLOR = vec4(vec3(v * 1.0 + 0.0), 1.0);
}

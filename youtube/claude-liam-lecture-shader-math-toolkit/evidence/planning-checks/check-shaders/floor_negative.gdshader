shader_type canvas_item;

void fragment() {
	int k = min(int(floor(UV.x * 5.0)), 4);
	float x = 0.0;
	if (k == 0) { x = 2.75; } else if (k == 1) { x = 0.75; } else if (k == 2) { x = -0.25; } else if (k == 3) { x = -1.75; } else if (k == 4) { x = 3.0; }
	float v = floor(x);
	COLOR = vec4(vec3(v * 0.125 + 0.375), 1.0);
}

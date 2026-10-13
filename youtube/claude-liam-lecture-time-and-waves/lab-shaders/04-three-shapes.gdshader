shader_type canvas_item;

void fragment() {
	float cycles = TIME * 0.5;
	float saw = fract(cycles);
	float tri = 1.0 - abs(saw * 2.0 - 1.0);
	float sine = 0.5 + 0.5 * sin(TAU * (cycles - 0.25));
	float value = UV.y < 0.66 ? tri : saw;
	if (UV.y < 0.33) { value = sine; }
	if (fract(UV.y * 3.0) < 0.08) { value = 0.0; }
	vec3 teal = vec3(0.37, 0.64, 0.57);
	vec3 track = vec3(0.93, 0.92, 0.88);
	COLOR = vec4(UV.x < value ? teal : track, 1.0);
}

shader_type canvas_item;

void fragment() {
	float x = UV.x;
	float v = smoothstep(0.26, 0.30, x * 0.7) - smoothstep(0.38, 0.42, x * 0.7);
	COLOR = vec4(vec3(v), 1.0);
}

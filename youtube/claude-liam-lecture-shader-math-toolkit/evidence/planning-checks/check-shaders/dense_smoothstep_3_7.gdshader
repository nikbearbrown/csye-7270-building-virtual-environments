shader_type canvas_item;

void fragment() {
	float x = UV.x;
	float v = smoothstep(0.3, 0.7, x);
	COLOR = vec4(vec3(v), 1.0);
}

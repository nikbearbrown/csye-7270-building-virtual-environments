shader_type canvas_item;

void fragment() {
	float x = UV.x;
	float v = smoothstep(0.0, 10.0, x * 10.0);
	COLOR = vec4(vec3(v), 1.0);
}

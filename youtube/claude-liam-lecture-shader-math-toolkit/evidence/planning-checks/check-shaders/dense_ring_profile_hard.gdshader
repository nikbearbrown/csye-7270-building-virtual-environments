shader_type canvas_item;

void fragment() {
	float x = UV.x;
	float v = step(0.3, x * 0.7) - step(0.38, x * 0.7);
	COLOR = vec4(vec3(v), 1.0);
}

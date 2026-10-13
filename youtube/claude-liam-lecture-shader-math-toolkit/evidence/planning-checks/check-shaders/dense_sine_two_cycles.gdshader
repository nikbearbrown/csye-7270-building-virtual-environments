shader_type canvas_item;

void fragment() {
	float x = UV.x;
	float v = 0.5 + 0.5 * sin(x * 12.5663706144);
	COLOR = vec4(vec3(v), 1.0);
}

shader_type canvas_item;

void fragment() {
	float x = UV.x;
	float v = abs(x * 2.0 - 1.0);
	COLOR = vec4(vec3(v), 1.0);
}

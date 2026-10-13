shader_type canvas_item;

void fragment() {
	float x = UV.x;
	float v = pow(x, 3.0);
	COLOR = vec4(vec3(v), 1.0);
}

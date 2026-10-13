shader_type canvas_item;

void fragment() {
	float x = UV.x;
	float v = 1.0 - x;
	COLOR = vec4(vec3(v), 1.0);
}

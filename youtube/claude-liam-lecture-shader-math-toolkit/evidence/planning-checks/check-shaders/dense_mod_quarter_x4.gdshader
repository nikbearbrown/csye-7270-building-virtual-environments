shader_type canvas_item;

void fragment() {
	float x = UV.x;
	float v = mod(x, 0.25) * 4.0;
	COLOR = vec4(vec3(v), 1.0);
}

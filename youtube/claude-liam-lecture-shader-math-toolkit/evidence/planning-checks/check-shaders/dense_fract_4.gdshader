shader_type canvas_item;

void fragment() {
	float x = UV.x;
	float v = fract(x * 4.0);
	COLOR = vec4(vec3(v), 1.0);
}

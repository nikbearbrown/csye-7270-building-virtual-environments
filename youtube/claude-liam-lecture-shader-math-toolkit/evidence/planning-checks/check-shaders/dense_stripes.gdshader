shader_type canvas_item;

void fragment() {
	float x = UV.x;
	float v = step(0.5, fract(x * 8.0));
	COLOR = vec4(vec3(v), 1.0);
}

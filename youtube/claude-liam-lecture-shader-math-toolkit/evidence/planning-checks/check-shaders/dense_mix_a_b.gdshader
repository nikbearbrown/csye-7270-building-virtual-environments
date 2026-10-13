shader_type canvas_item;

void fragment() {
	float x = UV.x;
	float v = mix(0.2, 0.9, x);
	COLOR = vec4(vec3(v), 1.0);
}

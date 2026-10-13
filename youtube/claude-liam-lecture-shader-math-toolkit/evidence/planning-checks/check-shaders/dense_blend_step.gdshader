shader_type canvas_item;

void fragment() {
	float x = UV.x;
	COLOR = vec4(mix(vec3(0.37, 0.64, 0.57), vec3(0.96, 0.80, 0.45), step(0.5, x)), 1.0);
}

shader_type canvas_item;

void fragment() {
	vec3 c = 0.4 + 0.6 * vec3(UV, 0.5);
	COLOR = c;
}

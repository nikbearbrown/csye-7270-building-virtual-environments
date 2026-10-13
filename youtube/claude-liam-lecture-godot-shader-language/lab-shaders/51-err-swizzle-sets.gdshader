shader_type canvas_item;

void fragment() {
	vec4 c = vec4(0.4, 0.7, 0.6, 1.0);
	COLOR = vec4(c.xg, 0.0, 1.0);
}

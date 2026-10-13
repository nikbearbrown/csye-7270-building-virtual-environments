shader_type canvas_item;

uniform vec4 a : source_color = vec4(0.0, 0.0, 0.0, 0.5);

void fragment() {
	COLOR = vec4(vec3(a.a), 1.0);
}

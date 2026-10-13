shader_type canvas_item;

void fragment() {
	COLOR = vec4(vec3(UV.x), 1.0);
}

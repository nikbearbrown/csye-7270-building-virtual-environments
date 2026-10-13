shader_type canvas_item;

const float LEVEL = 0.5;

void fragment() {
	LEVEL = 0.7;
	COLOR = vec4(vec3(LEVEL), 1.0);
}

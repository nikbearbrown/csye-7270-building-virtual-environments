shader_type canvas_item;

void fragment() {
	COLOR = vec4(vec3(LEVEL), 1.0);
}

const float LEVEL = 0.5;

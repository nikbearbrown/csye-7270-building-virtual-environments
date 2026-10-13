shader_type canvas_item;

void fragment() {
	COLOR = vec4(vec3(level), 1.0);
}

uniform float level = 0.5;

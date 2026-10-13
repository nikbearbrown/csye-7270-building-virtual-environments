shader_type canvas_item;

uniform sampler2D tex;

void fragment() {
	COLOR = vec4(vec3(step(0.5, texture(tex, UV).r)), 1.0);
}

shader_type canvas_item;

uniform sampler2D pic;
uniform float zoom = 1.0;

void fragment() {
	vec2 uv = UV * zoom;
	COLOR = texture(pic, uv);
}

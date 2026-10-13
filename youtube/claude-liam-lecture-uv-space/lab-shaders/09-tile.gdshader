shader_type canvas_item;

uniform sampler2D pic : repeat_enable;
uniform float zoom = 1.0;

void fragment() {
	vec2 uv = UV * zoom;
	COLOR = texture(pic, uv);
}

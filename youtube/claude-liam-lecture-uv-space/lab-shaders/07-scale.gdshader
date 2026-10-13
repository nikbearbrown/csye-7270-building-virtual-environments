shader_type canvas_item;

uniform float zoom = 1.0;

void fragment() {
	vec2 uv = UV * zoom;
	COLOR = texture(TEXTURE, uv);
}

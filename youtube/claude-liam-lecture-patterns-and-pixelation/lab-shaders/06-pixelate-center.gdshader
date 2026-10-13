shader_type canvas_item;

uniform float blocks = 16.0;

void fragment() {
	vec2 uv = (floor(UV * blocks) + 0.5) / blocks;
	COLOR = texture(TEXTURE, uv);
}

shader_type canvas_item;

uniform float zoom = 1.0;

void fragment() {
	vec2 uv = (UV - 0.5) * zoom + 0.5;
	COLOR = texture(TEXTURE, uv);
}

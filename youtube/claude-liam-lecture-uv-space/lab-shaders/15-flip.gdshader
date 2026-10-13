shader_type canvas_item;

uniform float flip = 1.0;

void fragment() {
	vec2 uv = (UV - 0.5) * vec2(1.0, flip) + 0.5;
	COLOR = texture(TEXTURE, uv);
}

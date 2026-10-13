shader_type canvas_item;

uniform float shift_x = 0.0;
uniform float shift_y = 0.0;

void fragment() {
	vec2 uv = UV;
	uv -= vec2(shift_x, shift_y);
	COLOR = texture(TEXTURE, uv);
}

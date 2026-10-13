shader_type canvas_item;

uniform int block : hint_range(1, 32) = 8;

void fragment() {
	vec2 cell = TEXTURE_PIXEL_SIZE * float(block);
	vec2 uv = (floor(UV / cell) + 0.5) * cell;
	COLOR = texture(TEXTURE, uv);
}

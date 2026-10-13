shader_type canvas_item;

void fragment() {
	COLOR.rgb = texture(SCREEN_TEXTURE, SCREEN_UV).rgb;
}

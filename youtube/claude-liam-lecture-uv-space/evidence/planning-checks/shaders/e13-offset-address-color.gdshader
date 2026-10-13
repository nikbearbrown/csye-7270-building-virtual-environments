shader_type canvas_item;

// the picture is the address picture (red = across, green = down), looked up at UV - 0.25
void fragment() {
	COLOR = texture(TEXTURE, UV - vec2(0.25));
}

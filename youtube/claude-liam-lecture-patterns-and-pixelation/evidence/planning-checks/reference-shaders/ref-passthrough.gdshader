shader_type canvas_item;

// Measurement reference only (not shown on screen): draws the texture exactly as it is.
void fragment() {
	COLOR = texture(TEXTURE, UV);
}

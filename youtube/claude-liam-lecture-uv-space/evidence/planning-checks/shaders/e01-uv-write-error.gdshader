shader_type canvas_item;

// EXPECTED TO FAIL: UV is read-only in fragment().
void fragment() {
	UV *= 2.0;
	COLOR = texture(TEXTURE, UV);
}

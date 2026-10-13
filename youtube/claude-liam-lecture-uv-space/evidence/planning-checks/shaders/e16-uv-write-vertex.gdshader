shader_type canvas_item;

// In vertex() UV is inout, so this compiles. The film only teaches the fragment() side, where UV is read-only.
void vertex() {
	UV.x += 0.1;
}

void fragment() {
	COLOR = texture(TEXTURE, UV);
}

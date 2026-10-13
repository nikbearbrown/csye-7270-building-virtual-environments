shader_type canvas_item;

vec4 f() {
	return texture(TEXTURE, vec2(0.5));
}

void fragment() {
	COLOR = f();
}

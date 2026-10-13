shader_type canvas_item;
// compile check: expected to FAIL in Godot 4.7.2 (the film quotes the compiler message). Run: lab/check_shader.sh <this file>
void fragment() {
	float s = 0.0;
	for (int y = -1; y <= 1; y++) {
		for (int x = -1; x <= 1; x++) {
			s += texture(TEXTURE, UV + vec2(x, y) * 0.001).a;
		}
	}
	COLOR = vec4(s / 9.0, 0.0, 0.0, 1.0);
}

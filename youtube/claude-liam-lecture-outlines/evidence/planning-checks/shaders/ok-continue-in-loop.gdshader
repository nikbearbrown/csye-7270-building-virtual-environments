shader_type canvas_item;
// compile check: expected to PASS in Godot 4.7.2 (continue is allowed inside a shader loop)
void fragment() {
	float s = 0.0;
	for (int y = -1; y <= 1; y++) {
		for (int x = -1; x <= 1; x++) {
			if (x == 0 && y == 0) { continue; }
			s += texture(TEXTURE, UV + vec2(float(x), float(y)) * 0.001).a;
		}
	}
	COLOR = vec4(s / 8.0, 0.0, 0.0, 1.0);
}

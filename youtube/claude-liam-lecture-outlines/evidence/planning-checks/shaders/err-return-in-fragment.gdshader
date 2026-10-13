shader_type canvas_item;
// compile check: expected to FAIL in Godot 4.7.2 (the film quotes the compiler message). Run: lab/check_shader.sh <this file>
uniform float thickness = 1.0;
void fragment() {
	COLOR = texture(TEXTURE, UV);
	if (thickness <= 0.0) { return; }
	COLOR.rgb = vec3(1.0);
}

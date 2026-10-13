shader_type canvas_item;
// compile check: expected to FAIL in Godot 4.7.2 (the film quotes the compiler message). Run: lab/check_shader.sh <this file>
void fragment() {
	int x = 1;
	COLOR = vec4(UV * x, 0.0, 1.0);
}

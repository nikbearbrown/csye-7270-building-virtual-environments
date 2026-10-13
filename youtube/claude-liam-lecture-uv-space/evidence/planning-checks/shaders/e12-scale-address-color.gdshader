shader_type canvas_item;

// the address after UV * 2, drawn as a colour: the red-green ramp fills only the top-left quarter, the rest is clamped at 1
void fragment() {
	COLOR = vec4(UV * 2.0, 0.5, 1.0);
}

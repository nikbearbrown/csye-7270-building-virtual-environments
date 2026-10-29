shader_type spatial;

// Broken on purpose: the line in fragment() has no semicolon.
uniform float amount : hint_range(0.0, 1.0) = 0.5;

void fragment() {
	ALBEDO = vec3(amount)
}

shader_type spatial;

// The same shader with its semicolon.
uniform float amount : hint_range(0.0, 1.0) = 0.5;

void fragment() {
	ALBEDO = vec3(amount);
}

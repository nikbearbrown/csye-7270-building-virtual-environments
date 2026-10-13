shader_type canvas_item;

// Evidence only (not shown on screen): shader sin/cos/tan values encoded as colors.
// Left half : R = sin(30 degrees), G = cos(30 degrees), B = 0.5 * tan(45 degrees).
// Right half: the same 30 read as radians -> R = 0.5 + 0.5 * sin(30), G = 0.5 + 0.5 * cos(30), B = (turns in 30 radians) / 8.
// Uniforms keep the values out of compile-time folding.
uniform float deg = 30.0;
uniform float forty_five = 45.0;

void fragment() {
	if (UV.x < 0.5) {
		COLOR = vec4(sin(radians(deg)), cos(radians(deg)), 0.5 * tan(radians(forty_five)), 1.0);
	} else {
		COLOR = vec4(0.5 + 0.5 * sin(deg), 0.5 + 0.5 * cos(deg), (deg / TAU) / 8.0, 1.0);
	}
}

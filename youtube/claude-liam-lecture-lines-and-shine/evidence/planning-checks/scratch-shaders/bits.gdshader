shader_type canvas_item;
// Scratch evidence shader (not shown on screen). Writes the 32 bits of a float into pixel bytes so a Lab probe can read the GPU's own answer.
// Left half carries bits 0..23 (R, G, B = low, middle, high byte of the low 24 bits); right half carries bits 24..31 in R.
uniform float angle = 90.0;
uniform int mode = 0;   // 0: tan(radians(angle)) | 1: tan(angle), no conversion | 2: radians(angle) | 3: sqrt(1.0 + m * m) with m = tan(radians(angle)) | 4: the constant 1.0 (self-test)
void fragment() {
	float x = 1.0;
	if (mode == 0) { x = tan(radians(angle)); }
	else if (mode == 1) { x = tan(angle); }
	else if (mode == 2) { x = radians(angle); }
	else if (mode == 3) { float m = tan(radians(angle)); x = sqrt(1.0 + m * m); }
	uint u = floatBitsToUint(x);
	if (UV.x < 0.5) {
		COLOR = vec4(float(u & 255u) / 255.0, float((u >> 8u) & 255u) / 255.0, float((u >> 16u) & 255u) / 255.0, 1.0);
	} else {
		COLOR = vec4(float((u >> 24u) & 255u) / 255.0, 0.0, 0.0, 1.0);
	}
}

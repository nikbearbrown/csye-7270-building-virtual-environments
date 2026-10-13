// Verification shader (not shown on screen): hide everything whose UV is outside 0 to 1 (four steps on UV).
shader_type canvas_item;

void fragment() {
	COLOR.a *= step(0.0, UV.x) * step(UV.x, 1.0) * step(0.0, UV.y) * step(UV.y, 1.0);
}

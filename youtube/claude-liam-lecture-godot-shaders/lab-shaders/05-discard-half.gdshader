shader_type canvas_item;

void fragment() {
	if (UV.x > 0.5) {
		discard;
	}
	COLOR = vec4(UV.x * 2.0, UV.y, 0.2, 1.0);
}

shader_type canvas_item;

varying float fold;

void vertex() {
	float phase = UV.x * 8.0 - TIME * 3.0;
	VERTEX.y += sin(phase) * 24.0 * UV.x;
	fold = cos(phase) * UV.x;
}

void fragment() {
	COLOR.rgb *= 0.9 + 0.1 * fold;
}

shader_type canvas_item;

// red turns on at U = 0.1, green turns on at V = 0.1: where (in pixels) do those edges sit?
void fragment() {
	COLOR = vec4(step(0.1, UV.x), step(0.1, UV.y), 0.5, 1.0);
}

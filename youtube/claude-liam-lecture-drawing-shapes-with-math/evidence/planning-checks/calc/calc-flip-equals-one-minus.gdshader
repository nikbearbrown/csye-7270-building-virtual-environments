shader_type canvas_item;
// Calculator, not shown in the film: |step(d, r) - (1 - step(r, d))| for every pixel, drawn as red. Any red pixel is a disagreement.
void fragment() {
	float d = distance(UV, vec2(0.5));
	float flipped = step(d, 0.3);
	float one_minus = 1.0 - step(0.3, d);
	COLOR = vec4(abs(flipped - one_minus), 0.0, 0.0, 1.0);
}

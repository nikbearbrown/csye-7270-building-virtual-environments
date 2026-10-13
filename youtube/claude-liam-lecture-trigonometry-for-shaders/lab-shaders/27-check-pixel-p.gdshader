shader_type canvas_item;

// Evidence only (not shown on screen): p = UV * 2.0 - 1.0 at the corners and the middle. R = p.x * 0.5 + 0.5, G = p.y * 0.5 + 0.5 (they must equal UV).
// B = 1.0 where length(p) < 1.0 (inside the unit circle), else 0.0.
void fragment() {
	vec2 p = UV * 2.0 - 1.0;
	COLOR = vec4(p.x * 0.5 + 0.5, p.y * 0.5 + 0.5, length(p) < 1.0 ? 1.0 : 0.0, 1.0);
}

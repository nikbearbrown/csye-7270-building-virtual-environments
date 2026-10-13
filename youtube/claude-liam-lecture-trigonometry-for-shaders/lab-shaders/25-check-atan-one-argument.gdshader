shader_type canvas_item;

// Evidence only (not shown on screen): the one-argument arc tangent. R = atan(p.y / p.x) / PI + 0.5 (same as 09-atan-one-argument).
void fragment() {
	vec2 p = UV * 2.0 - 1.0;
	COLOR = vec4(atan(p.y / p.x) / PI + 0.5, 0.0, 0.0, 1.0);
}

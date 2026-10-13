shader_type canvas_item;

// the centered address: which side of zero is each quadrant on?  red = right of zero, green = below zero, blue held at half
void fragment() {
	vec2 p = UV * 2.0 - 1.0;
	COLOR = vec4(step(0.0, p.x), step(0.0, p.y), 0.5, 1.0);
}

shader_type canvas_item;

// step(edge, x): 0 below the edge, 1 at or above. Left half of the window is x just below the edge, right half is x equal to the edge.
void fragment() {
	float below = step(0.5, 0.4999);
	float equal = step(0.5, 0.5);
	COLOR = vec4(UV.x < 0.5 ? below : equal, 0.0, 0.5, 1.0);
}

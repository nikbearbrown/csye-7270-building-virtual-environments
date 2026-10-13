shader_type canvas_item;

// Evidence only (not shown on screen): a flat colour WITH the source_color hint.
uniform vec4 flat_color : source_color = vec4(0.37, 0.64, 0.57, 1.0);

void fragment() {
	COLOR = flat_color;
}

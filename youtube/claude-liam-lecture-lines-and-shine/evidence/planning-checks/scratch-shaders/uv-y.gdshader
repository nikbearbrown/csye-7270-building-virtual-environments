shader_type canvas_item;
// Scratch evidence shader (not shown on screen): UV.y as the red channel, to read which way the second address number counts.
void fragment() {
	COLOR = vec4(UV.y, 0.0, 0.0, 1.0);
}

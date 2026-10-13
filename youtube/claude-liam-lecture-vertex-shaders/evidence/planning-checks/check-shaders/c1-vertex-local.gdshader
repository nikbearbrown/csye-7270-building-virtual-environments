// Verification shader (not shown on screen): what are VERTEX and UV at the corners, in the vertex stage?
// VERTEX is turned into a colour through a varying: 0 at -64, 0.5 at 0, 1 at +64 (a 128 px node). UV goes into blue/alpha-free green channel.
shader_type canvas_item;

varying vec2 corner;
varying vec2 vuv;

void vertex() {
	corner = VERTEX;
	vuv = UV;
}

void fragment() {
	// red/green: VERTEX/128 + 0.5 ; blue: UV.x (vertex-stage UV, blended) so that a mismatch with the vertex values would show
	COLOR = vec4(corner / 128.0 + 0.5, vuv.x, 1.0);
}

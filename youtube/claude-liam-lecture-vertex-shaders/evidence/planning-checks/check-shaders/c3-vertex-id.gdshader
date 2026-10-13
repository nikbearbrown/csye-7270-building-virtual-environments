// Verification shader (not shown on screen): what does VERTEX_ID give for the nodes we use?
// VERTEX_ID / id_scale goes into the red channel, blended across the shape by the varying, so the colour next to a corner reads that corner's id.
shader_type canvas_item;

uniform float id_scale = 16.0;
varying float vid;

void vertex() {
	vid = float(VERTEX_ID);
}

void fragment() {
	COLOR = vec4(vid / id_scale, 0.0, 0.0, 1.0);
}

shader_type canvas_item;
uniform vec2 hole_center = vec2(640.0, 360.0);
uniform float hole_radius = 60.0;
varying vec2 world_position;

void vertex() {
	world_position = (MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)).xy;
}

void fragment() {
	if (distance(world_position, hole_center) < hole_radius) {
		discard;
	}
}

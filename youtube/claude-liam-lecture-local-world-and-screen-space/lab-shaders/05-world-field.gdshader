shader_type canvas_item;

varying vec2 world_position;

void vertex() {
	world_position = (MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)).xy;
}

void fragment() {
	COLOR.rgb = vec3(world_position / vec2(1280.0, 720.0), 0.8);
}

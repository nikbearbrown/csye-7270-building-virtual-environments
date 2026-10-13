shader_type canvas_item;

varying vec2 screen_position;

void vertex() {
	screen_position = (MODEL_MATRIX * CANVAS_MATRIX * vec4(VERTEX, 0.0, 1.0)).xy;
}

void fragment() {
	COLOR.rgb = vec3(screen_position * SCREEN_PIXEL_SIZE, 0.8);
}

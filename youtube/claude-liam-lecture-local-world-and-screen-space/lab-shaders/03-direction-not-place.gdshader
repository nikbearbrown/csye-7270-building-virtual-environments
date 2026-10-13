shader_type canvas_item;

varying vec2 offset;

void vertex() {
	offset = (MODEL_MATRIX * vec4(VERTEX, 0.0, 0.0)).xy;
}

void fragment() {
	COLOR.rgb = vec3(offset / 128.0 + 0.5, 0.8);
}

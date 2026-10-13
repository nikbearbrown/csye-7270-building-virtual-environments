shader_type canvas_item;

varying vec2 position;

void vertex() {
	position = (MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)).xy;
}

void fragment() {
	float stripe = step(0.5, fract(position.x / 64.0));
	COLOR.rgb = mix(COLOR.rgb, vec3(1.0), stripe);
}

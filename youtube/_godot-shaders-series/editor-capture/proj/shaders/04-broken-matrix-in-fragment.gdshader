shader_type canvas_item;

void fragment() {
	vec2 world = (MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)).xy;
	COLOR.rgb = vec3(world / vec2(1280.0, 720.0), 0.8);
}

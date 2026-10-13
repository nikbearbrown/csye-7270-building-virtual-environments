shader_type canvas_item;

uniform sampler2D pattern : repeat_enable;

varying vec2 position;

void vertex() {
	position = (MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)).xy;
}

void fragment() {
	COLOR.rgb = texture(pattern, position * TEXTURE_PIXEL_SIZE).rgb;
}
